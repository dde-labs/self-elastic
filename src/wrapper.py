# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import json
import logging
from datetime import datetime

from pathlib import Path
from typing import Any

from elasticsearch import Elasticsearch, helpers
from elastic_transport import ListApiResponse, ObjectApiResponse

from .exceptions import (
    ExceptionResult, BulkException, ResourceNotFoundException, IndexExists,
    DocumentParsingException, RateLimitException,
)
from .schemas import (
    SynonymGetResp, SynonymPutResp, SynonymDeleteResp, SynonymRuleGetResp,
    SynonymRulePutResp, SynonymRuleDeleteResp,
)


def extract_exception(exceptions: dict[str, Any]) -> None:
    """Extract exception result from the bulk load API."""
    action: str = next(iter(exceptions))
    rs: ExceptionResult = ExceptionResult(**exceptions[action])

    if rs.error['type'] == 'resource_not_found_exception':
        raise ResourceNotFoundException(rs.error['reason'])

    elif rs.error['type'] == 'document_parsing_exception':
        raise DocumentParsingException(rs.error['reason'])

    elif rs.error['type'] == 'exception':
        if (
            'caused_by' in rs.error
            and all(s in rs.error['caused_by']['reason'] for s in (
                'Received a rate limit status code',
                'exceeded call rate limit',
                'Please retry after',
            ))
        ):
            raise RateLimitException(
                rs.error['caused_by']['reason']
            )

    raise BulkException(
        f"It has some error while bulk data to the elastic cloud: {exceptions}."
    )


class Index:
    """Elastic cloud index interface object."""

    def __init__(self, client: Elasticsearch, name: str):
        self.client: Elasticsearch = client
        self.name: str = name
        self.exists: bool = client.indices.exists(index=name)

    def create(
        self,
        mapping: dict[str, Any],
        setting: dict[str, Any] | None = None,
        force_create: bool = False,
    ) -> ObjectApiResponse:
        """Create index with mapping and setting values."""
        if self.exists:
            logging.warning("This index already exists.")
            if not force_create:
                raise IndexExists(f"The {self.name} index already exists.")

            self.client.indices.delete(index=self.name)

        rs: ObjectApiResponse = self.client.indices.create(
            index=self.name,
            mappings=mapping,
            settings=setting or {},
        )
        return rs

    def rename(self, name: str):
        self.client.reindex(
            source={"index": self.name},
            dest={"index": name},
        )

    def count(self, query: Any | None = None) -> int:
        """Return the document count from this index. It will return 0 if this
        index does not exist in the target Elastic.

        :param query: A query that want to filter before counting.
        """
        if not self.exists:
            return 0

        rs: ObjectApiResponse = self.client.count(index=self.name, query=query)
        return rs['count']

    def get_mapping(
        self, output: str | Path | None = None
    ) -> ObjectApiResponse:
        """Get mapping of this index."""
        rs = self.client.indices.get_mapping(index=self.name)
        if output is None:
            return rs

        with open(output, mode='w', encoding='utf-8') as f:
            # noinspection PyTypeChecker
            json.dump(rs.body, f, indent=4)
        return rs

    def get_setting(
        self, output: str | Path | None = None
    ) -> ObjectApiResponse:
        """Get setting"""
        rs = self.client.indices.get_settings(index=self.name)
        if output is None:
            return rs

        with open(output, mode='w', encoding='utf-8') as f:
            # noinspection PyTypeChecker
            json.dump(rs.body, f, indent=4)
        return rs

    def refresh(self) -> None:
        """Refresh this index."""
        self.client.indices.refresh(index=self.name)

    def truncate(self, auto_refresh: bool = True) -> ObjectApiResponse:
        """Truncate data in this index and then refresh it or not with passing
        an input refresh flag.
        """
        rs: ObjectApiResponse = self.client.delete_by_query(
            index=self.name, query={"match_all": {}}
        )

        if auto_refresh:
            print("Already refresh index after delete all documents.")
            self.refresh()

        return rs

    def get_id(self, _id: str) -> ObjectApiResponse:
        """Get document with specific document ID."""
        rs: ObjectApiResponse = self.client.get(index=self.name, id=_id)
        return rs

    def search_by_query(
        self,
        query: dict[str, Any],
        output: str | Path = None,
        size: int = 1000,
        **kwargs,
    ) -> ObjectApiResponse:
        """Search by query.

        :param query:
        :param output:
        :param size:

        NOTE:
            It has a lot of keys in the query syntax like `must`, `filter`,
        `should` that should to know before passing query to the Elastic.

        Compound Filter:
            - `must` clauses are required (and)
            - `should` clauses are optional (or)
        """
        rs: ObjectApiResponse = self.client.search(
            index=self.name, query=query, size=size, **kwargs
        )
        if output:
            with open(output, mode='w', encoding='utf-8') as f:
                # noinspection PyTypeChecker
                json.dump(rs.body['hits']['hits'], f)
        return rs

    def delete(self): ...

    def delete_by_query(self, query: Any) -> ObjectApiResponse:
        """Delete document that match with an input query.

        :rtype: ObjectApiResponse
        """
        rs: ObjectApiResponse = self.client.delete_by_query(
            index=self.name, query=query
        )
        return rs

    def mark_delete(self, src: str, dt: datetime):
        """Mark delete flag on this index documents that match with source
        system name and have updated date more than an dt value.
        """
        return self.client.update_by_query(
            index=self.name,
            script={
                "source": """
                    if (ctx._source.get('@deleted') != null) {
                        ctx._source.remove('@deleted');
                        ctx._source.put('@deleted', true);
                    } else {
                        ctx._source.put('@deleted', true);
                    }
                """,
                # "source": "ctx._source.put('@deleted', true)",
                "lang": "painless"
            },
            query={
                "bool": {
                    "filter": [
                        {"term": {"@src_name": src}},
                        {"range": {"@upload_date": {"gte": f'{dt:%Y-%m-%d}'}}},
                    ]
                }
            },
        )

    def index(self, _id: str, doc: Any):
        return self.client.index(
            index=self.name,
            id=_id,
            document=doc,
        )

    def bulk(self, actions: Any, request_timeout: int = 60 * 15) -> int:
        """Bulk load data to this index.

        :rtype: int
        """
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

            # NOTE: Get the first exception.
            first_fail: dict[str, Any] = failed[0]
            extract_exception(first_fail)

        return success


class Synonym:

    def __init__(self, client: Elasticsearch, name: str):
        self.client: Elasticsearch = client
        self.name = name

    def get(self) -> SynonymGetResp:
        resp: ObjectApiResponse = self.client.synonyms.get_synonym(
            id=self.name,
        )
        return SynonymGetResp(**resp.body)

    def put(self, synonyms_set: list[dict]) -> SynonymPutResp:
        resp: ObjectApiResponse = self.client.synonyms.put_synonym(
            id=self.name,
            synonyms_set=synonyms_set
        )
        return SynonymPutResp(**resp.body)


    def delete(self) -> SynonymDeleteResp:
        resp: ObjectApiResponse = self.client.synonyms.delete_synonym(
            id=self.name,
        )
        return SynonymDeleteResp(**resp.body)

    def get_rule(self, rule_id: str) -> SynonymRuleGetResp:
        resp: ObjectApiResponse = self.client.synonyms.get_synonym_rule(
            set_id=self.name,
            rule_id=rule_id,
        )
        return SynonymRuleGetResp(**resp.body)

    def put_rule(self, rule_id: str, synonyms: str) -> SynonymRulePutResp:
        resp: ObjectApiResponse = self.client.synonyms.put_synonym_rule(
            set_id=self.name,
            rule_id=rule_id,
            synonyms=synonyms,
        )
        return SynonymRulePutResp(**resp.body)

    def delete_rule(self, rule_id: str) -> SynonymRuleDeleteResp:
        resp: ObjectApiResponse = self.client.synonyms.delete_synonym_rule(
            set_id=self.name,
            rule_id=rule_id,
        )
        return SynonymRuleDeleteResp(**resp.body)


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

    def list_synonyms(self):
        return self.client.synonyms.get_synonyms_sets()


    def synonym(self, name) -> Synonym:
        """Get synonym interface object.

        :param name: A synonym ID.
        """
        return Synonym(self.client, name=name)
