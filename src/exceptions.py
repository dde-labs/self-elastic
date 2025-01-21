# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExceptionResult:
    _index: str
    _id: str
    status: int
    error: dict[str, Any]


class IndexExists(FileExistsError): ...


class BulkException(Exception): ...


class RateLimitException(BulkException): ...


class ResourceNotFoundException(BulkException): ...


class DocumentParsingException(BulkException): ...
