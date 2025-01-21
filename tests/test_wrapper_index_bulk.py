from typing import Any

import pytest

from src.wrapper import Es, Index
from src.exceptions import DocumentParsingException


def actions(index_name: str, data: list[dict[str, Any]]):
    for d in data:
        yield {
            "_op_type": "index",
            "_index": index_name,
            "_id": d.pop('es_id'),
            **d,
        }


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
    print(rs)


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