from typing import Any

import pytest

from src.wrapper import Es, Index
from src.exceptions import DocumentParsingException
from src.utils import actions


def test_bulk(es: Es):
    index: Index = es.index("tmp-korawica-home-product")
    rs: int = index.bulk(
        actions=actions(
            index.name,
            data=[
                {
                    'es_id': '1',
                    'barcode': '10001',
                    'cms_id': 'cms10001',
                    'height_number': 1.12,
                    'article_id': 1,
                    'upload_date': '2025-01-01',
                },
            ]
        )
    )
    assert rs == 1


def test_bulk_upsert(es: Es):
    index: Index = es.index("tmp-korawica-home-product")
    rs: int = index.bulk(
        actions=actions(
            index.name,
            data=[
                {
                    'es_id': '1',
                    'barcode': '10001',
                    'cms_id': 'cms10001',
                    'height_number': 5,
                    'article_id': 1,
                    'upload_date': '2025-01-02',
                    '@updated': True,
                },
            ]
        )
    )
    assert rs == 1

    rs_get = index.get_id('1')

    assert rs_get['_version'] > 1
    assert rs_get['_source']['height_number'] == 5


def test_bulk_raise_data_type(es: Es):
    index: Index = es.index("tmp-korawica-home-product")

    with pytest.raises(DocumentParsingException):
        index.bulk(
            actions=actions(
                index.name,
                data=[
                    {
                        'es_id': '1',
                        'barcode': '10001',
                        'cms_id': 'cms10001',
                        'height_number': 'very height',
                        'article_id': 1,
                        'upload_date': '2025-01-01',
                    },
                ]
            )
        )