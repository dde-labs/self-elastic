# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
import time
from pathlib import Path
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from typing import Any

import polars as pl
from azure.identity import InteractiveBrowserCredential
from elasticsearch import helpers
from elastic_transport import TlsError

from ..wrapper import Es, Index
from .__conf import FRAMEWORK_SCD1_COLS, Metadata


def extract_delta_from_az(
    container: str,
    name: str,
    st_name: str,
    dest: Path,
):
    token = InteractiveBrowserCredential(
        authority="login.microsoftonline.com"
    ).get_token("https://storage.azure.com/.default").token

    lf: pl.LazyFrame = pl.scan_delta(
        f"az://{container}/{name}",
        storage_options={"account_name": st_name, "token": token},
    )

    print(
        f"Start extract data from '{container}/{name}' on {st_name!r} "
        f"with {lf.select(pl.len()).collect()} records"
    )

    lf.collect().write_delta(
        dest,
        mode="overwrite",
        delta_write_options={"schema_mode": "overwrite"},
    )


def prepare_row(row):
    return row


def create_actions(df: pl.DataFrame, id_col: str, index_name: str):

    for row in df.iter_rows(named=True):

        if row.pop('@updated', False):
            pass

        yield {
            "_op_type": "index",
            "_index": index_name,
            '_id': row.pop(id_col),
            **prepare_row(row),
        }


def bulk_load_task(
    df: pl.DataFrame,
    id_col: str,
    index_name: str,
    *,
    es: Es,
    request_timeout: int = 3800,
    retry_limit: int = 20,
) -> tuple[int, list]:
    """Bulk load task for chucking of dataframe that has size limit with the
    bulk function.

    :rtype: tuple[int, list]
    """

    first_bulk_flag: bool = True
    retry_count: int = 0

    while first_bulk_flag or (retry_count > 0):
        print(
            f"({retry_count:02d}) Start running bulk load task ... ({len(df)})"
        )

        if retry_count > 0:
            time.sleep(60)

        if retry_count >= retry_limit:
            df.write_delta(
                f'../../data/issues/{index_name}-{uuid4()}',
                mode='overwrite',
            )
            print(
                "issue dataframe that retry reach limit the maximum value."
            )
            return 0, []

        first_bulk_flag: bool = False

        try:
            success, failed = helpers.bulk(
                es.client.options(request_timeout=request_timeout),
                actions=create_actions(
                    df,
                    id_col=id_col,
                    index_name=index_name,
                ),
                stats_only=False,
                refresh=False,
                raise_on_exception=False,
                raise_on_error=False,
            )
            print(
                f"[INFO]: ... Loading to {index_name} with status success: "
                f"{success} failed: {failed}"
            )
            return success, failed

        except helpers.BulkIndexError:
            retry_count += 1
        except TlsError as err:
            print(f"TlsError: {err}")
            retry_count += 1
        except Exception as err:
            df.write_delta(
                f'../../data/issues/{index_name}-{uuid4()}',
                mode='overwrite',
            )
            print(f"{type(err)}: {err}")
            raise


def pl_asat_dt_to_datetime():
    return (
        pl.col("asat_dt")
        .cast(pl.String)
        .str
        .to_datetime("%Y%m%d", time_zone='UTC')
    )


def dump_delta_to_es(es: Es, metadata: Metadata):
    lf: pl.LazyFrame = (
        pl.scan_delta(metadata.source)
        .select(
            pl.all().exclude(FRAMEWORK_SCD1_COLS).name.map(str.lower),
            pl.lit(False).alias('@updated'),
            (
                pl.lit(metadata.asat_dt)
                .cast(pl.String)
                .str
                .to_datetime("%Y%m%d", time_zone='UTC')
                .alias('@upload_date')
            ),
            pl.lit(metadata.prcess_nm).alias("@upload_prcs_nm"),
            (
                pl.when(pl.col("delete_f") == 1)
                .then(True)
                .otherwise(False)
                .alias("@deleted")
            ),
        )
    )
    success_total: int = 0
    failed_total: int = 0

    for main_lf in lf.collect(streaming=False).iter_slices(n_rows=metadata.limit_rows):

        with ThreadPoolExecutor(max_workers=metadata.limit_workers) as executor:

            futures: list[Future] = []

            for frame in main_lf.iter_slices(n_rows=metadata.limit_slice_rows):
                futures.append(
                    executor.submit(
                        bulk_load_task,
                        df=frame,
                        id_col='es_id',
                        index_name=metadata.index_nm,
                        es=es,
                    )
                )

                time.sleep(5)

            for future in as_completed(futures):
                success, failed = future.result()

                success_total += success

                if (num_failed := len(failed)) > 0:
                    print(failed)

                failed_total += num_failed

    print(success_total, failed_total)

    # NOTE: Remove all data that does not dump
    index: Index = es.index(name=metadata.index_nm)
    rs = index.search_by_query(
        query={
            "bool": {
                "must_not": [
                    {
                        "bool": {"filter":
                            [
                                {"term": {"@upload_prcs_nm": metadata.prcess_nm}},
                                {"range": {"@upload_date": {
                                    "gte": metadata.asat_dt_dash,
                                    "lte": metadata.asat_dt_dash,
                                    "format": "yyyy-MM-dd"
                                }}},
                            ],
                        },
                    },
                ],
            },
        },
    )
    hits: list[Any] = rs.body['hits']['hits']
    print(len(hits))
