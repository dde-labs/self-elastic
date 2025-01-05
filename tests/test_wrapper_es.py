import os

import pytest

from src.wrapper import Es


@pytest.fixture(scope='module')
def es():
    return Es(
        cloud_id=os.getenv('ES_CLOUD_ID'),
        api_key=os.getenv('ES_API_KEY'),
    )


def test_cat_health(es: Es):
    rs = es.cat_health()
    print(type(rs))
    print(rs)
    print(rs.body)

    rs = es.cat_health(verbose=True)
    print(type(rs))
    print(rs)
    print(rs.body)
