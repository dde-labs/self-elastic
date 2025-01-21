from pathlib import Path
from pprint import pprint
from typing import Any

from src.wrapper import Es, Index


def test_get_mapping(es: Es, test_path: Path):
    index: Index = es.index(name='home-product')
    rs = index.get_mapping()
    print(type(rs))
    print(rs)
    print(rs.body)

    test_file: Path = test_path / 'test_mapping_home_product.json'
    index.get_mapping(output=test_file)

    # test_file.unlink(missing_ok=True)


def test_get_setting(es: Es, test_path: Path):
    index: Index = es.index(name='home-product')
    rs = index.get_setting()
    print(type(rs))
    print(rs)
    print(rs.body)

    test_file: Path = test_path / 'test_setting_home_product.json'
    index.get_setting(output=test_file)

    # test_file.unlink(missing_ok=True)


def test_count(es: Es):
    index: Index = es.index(name='home-product')
    rs: int = index.count()
    assert rs >= 0
    assert isinstance(rs, int)


def test_search_by_query(es: Es):
    index: Index = es.index(name='home-product')
    rs = index.search_by_query(
        query={"bool": {"filter": {"term": {"cms_id": "307720"}}}}
    )
    hits: list[Any] = rs.body['hits']['hits']
    for hit in hits:
        body = {
            k: hit['_source'][k]
            for k in hit['_source']
            if (
                any(
                    k.startswith(_)
                    for _ in ('weight', 'width', 'length', 'height')
                )
            )
        }
        pprint(body, indent=2)
        print('-' * 100)


def test_search_by_query_limit(es: Es):
    index: Index = es.index(name='home-store')
    rs = index.search_by_query(
        query={
            "bool": {"must": [{"match_all": {}}], "must_not": [], "should": []}
        },
        size=1,
    )
    hits: list[Any] = rs.body['hits']['hits']
    print(hits)


def test_delete_by_query(es: Es):
    index: Index = es.index(name='home-product')
    rs = index.search_by_query(query={"match": {"barcode": "8852402136755"}})
    total: dict = rs['hits']['total']

    if total['value'] == 1:
        rs = index.delete_by_query(query={"match": {"barcode": "8852402136755"}})
        assert rs['deleted'] == 1
