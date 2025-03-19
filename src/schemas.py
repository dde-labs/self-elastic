# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class SynonymDeleteResp:
    acknowledged: bool


@dataclass
class SynonymGetResp:
    count: int
    # NOTE: List of `{"id": "1", "synonyms": "..."}`
    synonyms_set: list


@dataclass
class SynonymPutResp:
    result: Literal["updated", "created"]
    # NOTE: {'_shards': {'total': 577, 'successful': 313, 'failed': 0}, 'reload_details': []}
    reload_analyzers_details: dict[str, Any]


@dataclass
class SynonymRuleGetResp:
    id: str
    synonyms: str


@dataclass
class SynonymRulePutResp:
    result: Literal["updated", "created"]
    # NOTE: {'_shards': {'total': 577, 'successful': 313, 'failed': 0}, 'reload_details': []}
    reload_analyzers_details: dict[str, Any]


@dataclass
class SynonymRuleDeleteResp:
    result: Literal["deleted"]
    # NOTE: {'_shards': {'total': 577, 'successful': 313, 'failed': 0}, 'reload_details': []}
    reload_analyzers_details: dict[str, Any]
