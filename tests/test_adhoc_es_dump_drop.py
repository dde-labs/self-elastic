"""
Example for running single test.

```shell
$ pytest -vv tests/test_adhoc_es_dump.py::test_es_dump_home_product -p no:faulthandler
```
"""
from datetime import datetime

from src.wrapper import Es, Index


def test_es_dump_drop_home_product(es: Es):
    index: Index = es.index(name='home-product')
    asat_dt_dash: str = datetime.now().strftime('%Y-%m-%d')
    rs = index.search_by_query(
        query={
            "bool": {
                "must_not": [
                    {
                        "bool": {"filter":
                            [
                                {"term": {
                                    "@upload_prcs_nm": 'P_CAP_ES_HOME_PRODUCT_D_10'}},
                                {"range": {"@upload_date": {
                                    "gte": asat_dt_dash,
                                    "lte": asat_dt_dash,
                                    "format": "yyyy-MM-dd"
                                }}},
                            ],
                        },
                    },
                ],
            },
        },
    )
    hits: list = rs.body['hits']['hits']
    records: int = len(hits)
    print(records)
    if records > 0:
        print("Start delete doc that is not exists on the production.")
        rs = index.delete_by_query(
            query={
                "bool": {
                    "must_not": [
                        {
                            "bool": {"filter":
                                [
                                    {"term": {
                                        "@upload_prcs_nm": 'P_CAP_ES_HOME_PRODUCT_D_10'}},
                                    {"range": {"@upload_date": {
                                        "gte": asat_dt_dash,
                                        "lte": asat_dt_dash,
                                        "format": "yyyy-MM-dd"
                                    }}},
                                ],
                            },
                        },
                    ],
                },
            },
        )
        print(rs)


def test_es_dump_drop_home_solution_provider(es: Es):
    index: Index = es.index(name='home-solution-provider')
    asat_dt_dash: str = datetime.now().strftime('%Y-%m-%d')
    rs = index.search_by_query(
        query={
            "bool": {
                "must_not": [
                    {
                        "bool": {"filter":
                            [
                                {"term": {
                                    "@upload_prcs_nm": 'P_CAP_ES_HOME_SOLUTION_PROVIDER_D_10'}},
                                {"range": {"@upload_date": {
                                    "gte": asat_dt_dash,
                                    "lte": asat_dt_dash,
                                    "format": "yyyy-MM-dd"
                                }}},
                            ],
                        },
                    },
                ],
            },
        },
    )
    hits: list = rs.body['hits']['hits']
    records: int = len(hits)
    print(records)
    if records > 0:
        print("Start delete doc that is not exists on the production.")
        rs = index.delete_by_query(
            query={
                "bool": {
                    "must_not": [
                        {
                            "bool": {"filter":
                                [
                                    {"term": {
                                        "@upload_prcs_nm": 'P_CAP_ES_HOME_SOLUTION_PROVIDER_D_10'}},
                                    {"range": {"@upload_date": {
                                        "gte": asat_dt_dash,
                                        "lte": asat_dt_dash,
                                        "format": "yyyy-MM-dd"
                                    }}},
                                ],
                            },
                        },
                    ],
                },
            },
        )
        print(rs)
