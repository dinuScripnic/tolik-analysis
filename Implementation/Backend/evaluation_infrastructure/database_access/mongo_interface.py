"""Script for the MongoDB interface.""" ""
import typing
from pymongo import MongoClient

from evaluation_infrastructure.database_access.abstract_database_interface import (
    DBInterface, Connection
)


class MongoInterface(DBInterface):
    """Interface for the MongoDB database."""

    def __init__(self, host: str) -> None:
        """
        Initializes the MongoDB interface.

        Args:
            host (str): Host of the MongoDB database.
        """
        self.host = host
        self.connect()

    def connect(self) -> None:
        """Connects to the MongoDB database."""
        self.client = MongoClient(self.host)

    def disconnect(self) -> None:
        """Closes the connection to the MongoDB database."""
        self.client.close()

    def fetch(self, table: str) -> typing.List[dict]:
        """Fetches all evaluations from the MongoDB database."""
        return list(self.client["evaluation_system"][table].find({}, {"_id": 0}))

    def query(self, query: dict, table: str) -> typing.List[dict]:
        """Fetches all evaluations from the MongoDB database."""
        return list(self.client["evaluation_system"][table].find(query))

    def update(self, data: dict, table: str, query: dict) -> None:
        """
        Updates the given data in the MongoDB database.

        Args:
            data (dict): Data to be updated.
        """
        data = {"$set": data}
        self.client["evaluation_system"][table].update_one(query, data)

    def insert(self, data: dict, table: str) -> None:
        """
        Inserts the given data into the MongoDB database.

        Args:
            data (dict): Data to be inserted.
        """
        self.client["evaluation_system"][table].insert_one(data)

    def save(self, data: list[dict], table: str) -> None:
        """
        Save multiple data entries into the MongoDB database.

        Args:
            data (list[dict]): Data to be saved.
        """
        self.client["evaluation_system"][table].insert_many(data)

    def delete(self, query: dict, table: str) -> None:
        """
        Deletes the given data from the MongoDB database.

        Args:
            query (dict): Query to be deleted.
            table (str): Table to be deleted from.
        """
        return self.client["evaluation_system"][table].delete_one(query)


mi: DBInterface = MongoInterface("G")
