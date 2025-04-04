import json

import polars as pl

from .__conf import FRAMEWORK_SCD1_COLS, Metadata, DEFAULT_DT
from ..wrapper import Es


def pl_asat_dt_to_datetime():
    return (
        pl.col("asat_dt")
        .cast(pl.String)
        .str
        .to_datetime("%Y%m%d", time_zone='UTC')
    )


def select_env(lf: pl.LazyFrame, metadata: Metadata, dev_env_flag: bool = True):
    if dev_env_flag:
        return (
            lf
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
    else:
        return (
            lf
            .select(
                pl.all().exclude(FRAMEWORK_SCD1_COLS).name.map(str.lower),
                (
                    pl.when(pl.col("updt_asat_dt").is_null())
                    .then(True)
                    .otherwise(False)
                    .alias("@updated")
                ),
                (
                    pl.concat_list(
                        (
                            pl_asat_dt_to_datetime(),
                            pl.coalesce(pl.col("updt_asat_dt"), DEFAULT_DT)
                        ),
                    ).list.max()
                    .dt.date()
                    .alias("@upload_date")
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


def upsert_synonym(es: Es, metadata: Metadata, dev: bool = True):
    lf: pl.LazyFrame = (
        pl.scan_delta(metadata.source)
        .pipe(select_env, metadata=metadata, dev_env_flag=dev)
    )

    if metadata.where_cond:
        lf: pl.LazyFrame = lf.filter(pl.col("src") == "product")

    print(lf.collect())

