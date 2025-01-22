# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
import os
import time
from uuid import uuid4
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

import polars as pl
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
from elastic_transport import TlsError
from zoneinfo import ZoneInfo


load_dotenv('../.env')

# NOTE: Connection config
CLOUD_ID: str = os.getenv('ES_CLOUD_ID')
API_KEY: str = os.getenv('ES_API_KEY')

# NOTE: Function Config
LIMIT_ROWS: int = 750
LIMIT_WORKERS: int = 1
LIMIT_SLICE_ROWS: int = 250

# NOTE: Data Config
DATA_NAME: str = "home-content-article"
INDEX_NAME: str = "home-content-article"
PRCS_NM: str = "P_CAP_ES_HOME_CONTENT_ARTICLE_D_10"
ASAT_DT: str = "20241117"
ASAT_DT_DASH: str = "2024-11-17"
DEFAULT_DT: datetime = datetime(1990, 1, 1, tzinfo=ZoneInfo('UTC'))
FRAMEWORK_SCD_COLS: tuple[str, ...] = (
    'start_dt',
    'end_dt',
    'delete_f',
    'prcs_nm',
    'prcs_ld_id',
    'asat_dt',
    'updt_prcs_nm',
    'updt_prcs_ld_id',
    'updt_asat_dt',
)


pl.Config.set_streaming_chunk_size = 1000


def prepare_row(row):
    return row


def create_actions(df: pl.DataFrame, id_col: str, index_name: str):

    for row in df.iter_rows(named=True):

        if row.pop('@updated', False):
            yield {
                "_op_type": "update",
                "_index": index_name,
                '_id': row.pop(id_col),
                'doc': prepare_row(row),
                'doc_as_upsert': True,
            }
        else:
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
    client: Elasticsearch,
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
                client.options(request_timeout=request_timeout),
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


def scan_delta_local_iter():
    client = Elasticsearch(cloud_id=CLOUD_ID, api_key=API_KEY)

    # NOTE: Extract data from the Delta Table.
    df: pl.LazyFrame = (
        pl.scan_delta(f'../../data/{DATA_NAME}')
        .select(
            pl.all().exclude(FRAMEWORK_SCD_COLS).name.map(str.lower),
            pl.when(
                pl.col("updt_asat_dt").is_null()
            ).then(True).otherwise(False).alias("@updated"),
            pl.concat_list(
                (
                    pl_asat_dt_to_datetime(),
                    pl.coalesce(pl.col("updt_asat_dt"), DEFAULT_DT)
                ),
            ).list.max().dt.date().alias("@upload_date"),
            pl.lit(PRCS_NM).alias("@upload_prcs_nm"),
            # pl.lit(False).alias("@deleted"),
            (
                pl.when(pl.col("delete_f") == 1)
                .then(True)
                .otherwise(False)
                .alias("@deleted")
            ),
        )
        .filter(pl.col('@upload_date') >= pl.lit(ASAT_DT_DASH).str.to_date())
    )

    success_total: int = 0
    failed_total: int = 0

    for parent_df in df.collect(streaming=False).iter_slices(n_rows=LIMIT_ROWS):

        with ThreadPoolExecutor(max_workers=LIMIT_WORKERS) as executor:

            futures: list[Future] = []

            for frame in parent_df.iter_slices(n_rows=LIMIT_SLICE_ROWS):
                futures.append(
                    executor.submit(
                        bulk_load_task,
                        df=frame,
                        id_col='es_id',
                        index_name=INDEX_NAME,
                        client=client,
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


if __name__ == '__main__':
    scan_delta_local_iter()
