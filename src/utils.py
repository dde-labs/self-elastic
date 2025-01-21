# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from typing import Any


# NOTE:
#   IMAGE_EXT: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".bmp")
IMAGE_EXT: tuple[str, ...] = ('png', 'jpeg', 'jpg')


def is_image(filename) -> bool:
    return any(filename.endswith(ext) for ext in IMAGE_EXT)


def actions(index_name: str, data: list[dict[str, Any]]):
    """Bulk action for any list of documents."""
    for d in data:
        if d.pop('@updated', False):
            yield {
                "_op_type": "update",
                "_index": index_name,
                '_id': d.pop("es_id"),
                'doc': d,
                'doc_as_upsert': True,
            }
        else:
            yield {
                "_op_type": "index",
                "_index": index_name,
                "_id": d.pop('es_id'),
                **d,
            }