from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExceptionResult:
    _index: str
    _id: str
    status: int
    error: dict[str, Any]


class IndexExists(FileExistsError): ...


class BulkException(Exception):

    def __init__(self, *args, raw: dict[str, Any] = None, **kwargs):
        self._raw = raw
        super().__init__(*args, **kwargs)

class RateLimitException(BulkException): ...


class ResourceNotFoundException(BulkException): ...
