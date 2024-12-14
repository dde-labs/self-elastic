import os

import pytest

from src.wrapper import ES


@pytest.fixture(scope='module')
def es():
    return ES(
        cloud_id=os.getenv('ES_CLOUD_ID'),
        api_key=os.getenv('ES_API_KEY'),
    )


def test_cat_health(es: ES):
    rs = es.cat_health()
    print(type(rs))
    print(rs)
    print(rs.body)

    rs = es.cat_health(verbose=True)
    print(type(rs))
    print(rs)
    print(rs.body)
