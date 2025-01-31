from pathlib import Path
from pprint import pprint
from typing import Any

from src.wrapper import Es, Index


def test_get_mapping(es: Es, test_path: Path):
    index_name: str = "home-content-article-test-thaishingle"
    index: Index = es.index(name=index_name)
    rs = index.get_mapping()
    print(type(rs))
    print(rs)
    print(rs.body)

    test_file: Path = test_path / f'test-mapping-{index_name}.json'
    index.get_mapping(output=test_file)


def test_get_setting(es: Es, test_path: Path):
    index_name: str = 'home-product'
    index: Index = es.index(name=index_name)
    rs = index.get_setting()
    print(type(rs))
    print(rs)
    print(rs.body)

    test_file: Path = test_path / f'test-setting-{index_name}.json'
    index.get_setting(output=test_file)


def test_create_index(es: Es):
    index: Index = es.index(name='tmp-korawica-home-product')
    assert not index.exists

    rs = index.create(
        setting={
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        mapping={
            "properties": {
                "barcode": {"type": "keyword"},
                "brand": {"type": "text", "analyzer": "icu_analyzer"},
                "cms_id": {"type": "keyword"},
                "height_number": {"type": "float"},
                "article_id": {"type": "integer"},
                "upload_date": {"type": "date"},
            }
        }
    )
    assert rs.body == {
        'acknowledged': True,
        'shards_acknowledged': True,
        'index': 'tmp-korawica-home-product',
    }


def test_count(es: Es):
    index: Index = es.index(name='home-product')
    # index: Index = es.index(name='home-solution')
    rs: int = index.count()
    assert rs >= 0
    assert isinstance(rs, int)
    print(rs)


def test_truncate(es: Es):
    index: Index = es.index('tmp-korawica-home-product')
    rs = index.truncate(auto_refresh=True)
    print(type(rs))
    print(rs)


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


def test_search_by_query_multi_condition(es: Es):
    index: Index = es.index(name='home-product')
    rs = index.search_by_query(
        query={"bool": {"filter":
            [
                {"term": {"@upload_prcs_nm": "P_CAP_ES_HOME_PRODUCT_D_10"}},
                {"range": {"@upload_date": {"gte": "2025-01-27"}}},
            ]
        }}
    )
    hits: list[Any] = rs.body['hits']['hits']
    for hit in hits:
        body = {
            k: hit['_source'][k]
            for k in hit['_source']
            if (
                any(
                    k.startswith(_)
                    for _ in ('@upload_prcs_nm', '@upload_date', 'cmd_id')
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
        size=33,
    )
    hits: list[Any] = rs.body['hits']['hits']
    print(hits)


def test_search_by_query_not_match(es: Es):
    index: Index = es.index(name='home-store')
    rs = index.search_by_query(
        query={
            "bool": {
                "must_not": [
                    {
                        "bool": {"filter":
                            [
                                {"term": {"@upload_prcs_nm": 'P_CAP_ES_HOME_STORE_D_10'}},
                                {"range": {"@upload_date": {
                                    "gte": '2025-01-31',
                                    "lte": '2025-01-31',
                                    "format": "yyyy-MM-dd"
                                }}},
                            ],
                        },
                    }
                ]
            }
        }
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


def test_get_id(es: Es):
    # index: Index = es.index(name='home-solution')
    # rs = index.get_id('2f06e2ffc54234439bbed00ce84d265a')
    # print(rs)

    index: Index = es.index(name='home-product')
    rs = index.get_id('cc87dbcebfb02f17b539068b4df1e287')
    rs_prepare = {
        r: rs['_source'][r]
        for r in rs['_source'] if r in (
            'display_name_th', '@upload_date', '@upload_prcs_nm', '@delete_f'
        )
    }
    print(rs_prepare)
