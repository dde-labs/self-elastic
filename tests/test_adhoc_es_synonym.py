import os
from pathlib import Path
from datetime import datetime

import pytest
from deltalake import DeltaTable
from deltalake.exceptions import TableNotFoundError

from src.adhoc.__conf import Metadata
from src.adhoc.es_dump import extract_delta_from_az
from src.adhoc.es_synonym import upsert_synonym
from src.wrapper import Es


@pytest.fixture(scope='module')
def st_name() -> str:
    return os.getenv('AZ_ST_NAME')


@pytest.fixture(scope='module')
def container() -> str:
    return os.getenv('AZ_CONTAINER_NAME')


def test_es_synonym_sl_product(es: Es, test_path: Path, st_name: str, container: str):
    """Test Dump data from PROD to DEV on index, smartliving-product-synonym.

    CMD:
    pytest -vv -s tests/test_adhoc_es_synonym.py::test_es_synonym_sl_product -p no:faulthandler
    """

    # dest: Path = test_path.parent / f'data/dump/{datetime.now():%Y%m%d}'
    dest: Path = test_path.parent / f'data/dump/20250404'
    # if dest.exists():
    #     dest.mkdir(exist_ok=True)
    #
    # try:
    #     DeltaTable(str(dest / 'sl_synonym'))
    # except TableNotFoundError:
    #     extract_delta_from_az(
    #         container=container,
    #         name='sl_synonym',
    #         st_name=st_name,
    #         dest=dest / 'sl_synonym'
    #     )

    upsert_synonym(
        es=es,
        metadata=Metadata(
            source=str(dest / 'sl_synonym'),
            index_nm='smartliving-product-synonym',
            asat_dt="20250404",
            prcess_nm="P_CAP_ES_SL_SYNONYM_PRODUCT_D_99",
            where_cond="src = 'product'",
            limit_workers=2,
        ),
    )
