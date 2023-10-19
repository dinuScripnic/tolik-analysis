"""Abstract Database Interface"""
from __future__ import annotations

from typing import Protocol, TypeVar, Mapping, Self

QK = TypeVar("QK")
QV = TypeVar("QV", contravariant=True)


class DBInterface(Protocol[QK, QV]):
    def __init__(self, host: str) -> None: ...
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def find(self, query: Mapping[QK, QV], table: str) -> list[object]: ...
    def find_first(self, query: Mapping[QK, QV], table: str) -> object: ...
    def find_unique(self, query: Mapping[QK, QV], table: str) -> object: ...
    def find_all(self, table: str) -> list[object]: ...
    def update(self, data: Mapping[QK, QV], table: str, query: Mapping[QK, QV]) -> object: ...
    def insert(self, data: Mapping[QK, QV], table: str) -> None: ...
    def delete(self, query: Mapping[QK, QV], table: str) -> None: ...
    def transaction(self) -> Connection: ...


class Connection:
    def __init__(self, caller: DBInterface) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
    def commit(self) -> None: ...
