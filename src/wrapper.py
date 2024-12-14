# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from typing import Any

from elasticsearch import Elasticsearch, helpers
from elastic_transport import ListApiResponse


class Index:
    """Elastic cloud index wrapper object."""

    def __init__(self, client: Elasticsearch, name: str):
        self.client: Elasticsearch = client
        self.name: str = name
        self.exists: bool = client.indices.exists(index=name)

    def create(self, setting: dict[str, Any], mapping: dict[str, Any]) -> None:
        ...

    def get_mapping(self):
        return self.client.indices.get_mapping(index=self.name)

    def get_setting(self):
        return self.client.indices.get_settings(index=self.name)

    def refresh(self): ...

    def truncate(self): ...

    def delete(self): ...

    def update(self): ...

    def index(self): ...

    def bulk(self, data: Any, *, updated_by: str): ...


class ES:
    def __init__(self, cloud_id: str, api_key: str):
        self.client = Elasticsearch(cloud_id=cloud_id, api_key=api_key)

    def cat_health(self, verbose: bool = False) -> ListApiResponse:
        """Cat the health status on the target elastic cloud service."""
        return self.client.cat.health(format='json', v=verbose)

    def indices(self, name: str):
        return self.client.cat.indices(index=name, v=True, s="index")

    def index(self, name: str) -> Index:
        return Index(self.client, name=name)
