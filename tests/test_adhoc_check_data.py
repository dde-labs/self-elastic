import os
from pathlib import Path
from datetime import datetime

import pytest
import polars as pl

from src.adhoc.__conf import FRAMEWORK_SCD1_COLS, DEFAULT_DT
from src.adhoc.es_dump import extract_delta_from_az


@pytest.fixture(scope='module')
def st_name() -> str:
    return os.getenv('AZ_ST_NAME')


@pytest.fixture(scope='module')
def container() -> str:
    return os.getenv('AZ_CONTAINER_NAME')


def pl_asat_dt_to_datetime():
    return (
        pl.col("asat_dt")
        .cast(pl.String)
        .str
        .to_datetime("%Y%m%d", time_zone='UTC')
    )


def test_check_home_product(test_path: Path, st_name, container):
    dest: Path = test_path.parent / f'data/dump/{datetime.now():%Y%m%d}'

    # extract_delta_from_az(
    #     container=container,
    #     name='home_product',
    #     st_name=st_name,
    #     dest=dest / 'home_product'
    # )


    asat_dt_dash = '2025-01-30'
    prcs_nm: str = 'P_CAP_ES_HOME_PRODUCT_D_10'

    lf: pl.LazyFrame = (
        pl.scan_delta(str(dest / 'home_product'))
        .select(
            pl.all().exclude(FRAMEWORK_SCD1_COLS).name.map(str.lower),
            pl.when(
                pl.col("updt_asat_dt").is_null()
            ).then(True).otherwise(False).alias("@updated"),
            pl.concat_list(
                (
                    pl_asat_dt_to_datetime(),
                    pl.coalesce(pl.col("updt_asat_dt"), DEFAULT_DT)
                ),
            ).list.max().dt.date().alias("@upload_date"),
            pl.lit(prcs_nm).alias("@upload_prcs_nm"),
            (
                pl.when(pl.col("delete_f") == 1)
                .then(True)
                .otherwise(False)
                .alias("@deleted")
            ),
            'display_name_th', 'asat_dt', 'updt_asat_dt', 'es_id',
            pl.lit('2025-01-30').str.to_date().alias('mock'),
        )
        .filter(pl.col('@upload_date') >= pl.lit(asat_dt_dash).str.to_date())
        .filter(
            pl.col('asat_dt') == 20250112
            # pl.col('updt_asat_dt') == pl.lit('2025-01-30')
            # pl.col('updt_asat_dt').is_not_null()
        )
        .select(
            'display_name_th', 'asat_dt', 'updt_asat_dt', 'es_id',
            pl.lit('2025-01-30').str.to_date().alias('mock'),
        )
    )

    print(lf.collect())
    #
    # lf_filter = (
    #     lf.filter(
    #         pl.col('updt_asat_dt') == pl.lit('2025-01-30').str.to_date()
    #     )
    # )
    #
    # print(lf_filter.collect())
