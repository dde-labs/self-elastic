# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from elasticsearch import Elasticsearch, helpers
from elastic_transport import ListApiResponse, ObjectApiResponse

from .exceptions import BulkException


class Index:
    """Elastic cloud index interface object."""

    def __init__(self, client: Elasticsearch, name: str):
        self.client: Elasticsearch = client
        self.name: str = name
        self.exists: bool = client.indices.exists(index=name)

    def create(self, setting: dict[str, Any], mapping: dict[str, Any]) -> None:
        if self.exists:
            logging.warning("This index already exists.")

    def count(self) -> int:
        if not self.exists:
            return 0

        rs: ObjectApiResponse = self.client.count(index=self.name)
        return rs['count']

    def get_mapping(
        self, output: str | Path | None = None
    ) -> ObjectApiResponse:
        rs = self.client.indices.get_mapping(index=self.name)
        if output is None:
            return rs

        with open(output, mode='w', encoding='utf-8') as f:
            json.dump(rs.body, f)
        return rs

    def get_setting(
        self, output: str | Path | None = None
    ) -> ObjectApiResponse:
        rs = self.client.indices.get_settings(index=self.name)
        if output is None:
            return rs

        with open(output, mode='w', encoding='utf-8') as f:
            json.dump(rs.body, f)
        return rs

    def refresh(self) -> None:
        self.client.indices.refresh(index=self.name)

    def truncate(self, auto_refresh: bool = True):
        rs = self.client.delete_by_query(
            index=self.name, query={"match_all": {}}
        )
        if auto_refresh:
            self.refresh()

    def delete(self, query: Any, script: Any): ...

    def update(self, query: Any, script: Any): ...

    def index(self, _id: str, doc: Any): ...

    def bulk(self, actions: Any, request_timeout: int = 60 * 15) -> int:
        success, failed = helpers.bulk(
            self.client.options(
                request_timeout=request_timeout,
                retry_on_timeout=True,
            ),
            actions=actions,
            raise_on_exception=False,
            raise_on_error=False,
        )
        if len(failed) > 0:
            raise BulkException(
                "It has some error while bulk data to the elastic cloud."
            )

        return success


class Es:
    """Elastic cloud interface object."""

    def __init__(self, cloud_id: str, api_key: str):
        self.client = Elasticsearch(cloud_id=cloud_id, api_key=api_key)

    def cat_health(self, verbose: bool = True) -> ListApiResponse:
        """Cat the health status on the target elastic cloud service.

        :param verbose: A verbose flag that pass to ``.cat.health`` method.

        :rtype: ListApiResponse
        """
        return self.client.cat.health(format='json', v=verbose)

    def indices(self, name: str, verbose: bool = False) -> ListApiResponse:
        """Get the indices with name pattern string on the target elastic cloud
        service.

        :param name: A pattern name of index.
        :param verbose: A verbose flag that pass to ``.cat.health`` method.

        :rtype: ListApiResponse
        """
        return self.client.cat.indices(
            index=name, v=verbose, s="index", format='json'
        )

    def index(self, name: str) -> Index:
        """Get index interface object.

        :param name:

        :rtype: Index
        :return:
        """
        return Index(self.client, name=name)
