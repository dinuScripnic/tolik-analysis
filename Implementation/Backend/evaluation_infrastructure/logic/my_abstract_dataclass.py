"""Abstract class for a course"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from evaluation_infrastructure.database_access.abstract_database_interface import (
    AbstractDatabaseInterface,
)


@dataclass
class AbstractDataclass(ABC):
    """Abstract class for a course"""

    faculty: str
    course: str
    lecturer: str

    @property
    @abstractmethod
    def query(self):
        """Creates a query for the database"""

    @property
    def dict(self) -> dict:
        """Creates a dict for the database"""

    @abstractmethod
    def save_to_database(self, database: AbstractDatabaseInterface):
        """Saves the dataclass to the database"""
