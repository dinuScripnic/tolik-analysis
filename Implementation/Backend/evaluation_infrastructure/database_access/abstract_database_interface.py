"""Abstract Database Interface"""
from abc import ABC, abstractmethod
import typing


class AbstractDatabaseInterface(ABC):
    """Abstract Database Interface"""

    @abstractmethod
    def __init__(self, host: str) -> None:
        """Abstract Database Interface initializer"""

    @abstractmethod
    def connect(self) -> None:
        """Abstract Database Interface connect method"""

    @abstractmethod
    def disconnect(self) -> None:
        """Abstract Database Interface disconnect method"""

    @abstractmethod
    def query(self, query: dict, table) -> typing.List[dict]:
        """Abstract Database Interface query method"""

    @abstractmethod
    def fetch(self, table) -> typing.List[dict]:
        """Gets all the data from the database"""

    @abstractmethod
    def insert(self, data, table):
        """Abstract Database Interface insert method"""

    @abstractmethod
    def save(self, data, table):
        """Abstract Database Interface save method"""

    @abstractmethod
    def update(self, data, table, query):
        """Abstract Database Interface update method"""

    @abstractmethod
    def delete(self, query, table):
        """Abstract Database Interface delete method"""
