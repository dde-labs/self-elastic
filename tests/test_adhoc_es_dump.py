import os
from pathlib import Path
from datetime import datetime

import pytest
from deltalake import DeltaTable
from deltalake.exceptions import TableNotFoundError

from src.adhoc.__conf import Metadata
from src.adhoc.es_dump import extract_delta_from_az, dump_delta_to_es
from src.wrapper import Es


@pytest.fixture(scope='module')
def st_name() -> str:
    return os.getenv('AZ_ST_NAME')


@pytest.fixture(scope='module')
def container() -> str:
    return os.getenv('AZ_CONTAINER_NAME')


def test_es_dump_home_product(es: Es, test_path: Path, st_name: str, container: str):
    """Test Dump data from PROD to DEV on index, home-product.

    CMD:
    pytest -vv -s tests/test_adhoc_es_dump.py::test_es_dump_home_product -p no:faulthandler
    """

    dest: Path = test_path.parent / f'data/dump/{datetime.now():%Y%m%d}'
    if dest.exists():
        dest.mkdir(exist_ok=True)

    try:
        DeltaTable(str(dest / 'home_product'))
    except TableNotFoundError:
        extract_delta_from_az(
            container=container,
            name='home_product',
            st_name=st_name,
            dest=dest / 'home_product'
        )

    dump_delta_to_es(
        es=es, metadata=Metadata(
            source=str(dest / 'home_product'),
            index_nm='home-product',
            asat_dt=f"{datetime.now():%Y%m%d}",
            prcess_nm="P_CAP_ES_HOME_PRODUCT_D_10",
            limit_workers=2,
        )
    )

    index = es.index('home-product')
    index.refresh()

    rows: int = index.count()
    print(rows)


def test_es_dump_home_store(es: Es, test_path: Path, st_name: str, container: str):
    """pytest -vv tests/test_adhoc_es_dump.py::test_es_dump_home_store -p no:faulthandler"""
    dest: Path = test_path.parent / f'data/dump/{datetime.now():%Y%m%d}'
    if dest.exists():
        dest.mkdir(exist_ok=True)

    try:
        DeltaTable(str(dest / 'home_store'))
    except TableNotFoundError:
        extract_delta_from_az(
            container=container,
            name='home_store',
            st_name=st_name,
            dest=dest / 'home_store'
        )

    dump_delta_to_es(
        es=es, metadata=Metadata(
            source=str(dest / 'home_store'),
            index_nm='home-store',
            asat_dt=f"{datetime.now():%Y%m%d}",
            prcess_nm="P_CAP_ES_HOME_STORE_D_10",
        )
    )

    index = es.index('home-store')
    index.refresh()

    rows: int = index.count()
    print(rows)


def test_es_dump_home_solution(es: Es, test_path: Path, st_name: str, container: str):
    """Test Dump data from PROD to DEV on index, home-solution.

    CMD:
    pytest -vv -s tests/test_adhoc_es_dump.py::test_es_dump_home_solution -p no:faulthandler
    """
    dest_name: str = 'home_solution'
    index_name: str = 'home-solution'

    dest: Path = test_path.parent / f'data/dump/{datetime.now():%Y%m%d}'
    if dest.exists():
        dest.mkdir(exist_ok=True)

    try:
        DeltaTable(str(dest / dest_name))
    except TableNotFoundError:
        extract_delta_from_az(
            container=container,
            name=dest_name,
            st_name=st_name,
            dest=dest / dest_name
        )

    dump_delta_to_es(
        es=es,
        metadata=Metadata(
            source=str(dest / dest_name),
            index_nm=index_name,
            asat_dt=f"{datetime.now():%Y%m%d}",
            prcess_nm="P_CAP_ES_HOME_SOLUTION_D_10",
            limit_workers=3,
        ),
    )

    index = es.index(index_name)
    index.refresh()

    rows: int = index.count()
    print("Rows count from index:", rows)


def test_es_dump_home_solution_provider(es: Es, test_path: Path, st_name: str, container: str):
    """pytest -vv tests/test_adhoc_es_dump.py::test_es_dump_home_solution_provider -p no:faulthandler"""
    dest_name: str = 'home_solution_provider'
    index_name: str = 'home-solution-provider'

    dest: Path = test_path.parent / f'data/dump/{datetime.now():%Y%m%d}'
    if dest.exists():
        dest.mkdir(exist_ok=True)

    try:
        DeltaTable(str(dest / dest_name))
    except TableNotFoundError:
        extract_delta_from_az(
            container=container,
            name=dest_name,
            st_name=st_name,
            dest=dest / dest_name
        )

    dump_delta_to_es(
        es=es, metadata=Metadata(
            source=str(dest / dest_name),
            index_nm=index_name,
            asat_dt=f"{datetime.now():%Y%m%d}",
            prcess_nm="P_CAP_ES_HOME_SOLUTION_PROVIDER_D_10",
            limit_workers=3,
        )
    )

    index = es.index(index_name)
    index.refresh()

    rows: int = index.count()
    print(rows)


def test_es_dump_home_content_article(es: Es, test_path: Path, st_name: str, container: str):
    """pytest -vv -s ./tests/test_adhoc_es_dump.py::test_es_dump_home_content_article
    """
    dest_name: str = 'home_content_article'
    index_name: str = 'home-content-article'

    dest: Path = test_path.parent / f'data/dump/{datetime.now():%Y%m%d}'
    if dest.exists():
        dest.mkdir(exist_ok=True)

    try:
        DeltaTable(str(dest / dest_name))
    except TableNotFoundError:
        extract_delta_from_az(
            container=container,
            name=dest_name,
            st_name=st_name,
            dest=dest / dest_name
        )

    dump_delta_to_es(
        es=es, metadata=Metadata(
            source=str(dest / dest_name),
            index_nm=index_name,
            asat_dt=f"{datetime.now():%Y%m%d}",
            prcess_nm="P_CAP_ES_HOME_CONTENT_ARTICLE_D_10",
            limit_rows=300,
            limit_slice_rows=50,
        )
    )

    index = es.index(index_name)
    index.refresh()

    rows: int = index.count()
    print(rows)
