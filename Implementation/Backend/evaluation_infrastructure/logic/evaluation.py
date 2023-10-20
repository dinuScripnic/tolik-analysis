"""Evaluation class for the evaluation infrastructure.""" ""
import typing
from dataclasses import dataclass, field
from evaluation_infrastructure.logic.my_abstract_dataclass import AbstractDataclass

from evaluation_infrastructure.database_access.abstract_database_interface import (
    AbstractDatabaseInterface,
)


@dataclass
class Evaluation(AbstractDataclass):
    """Represents an evaluation for a course."""

    semester: str
    cohort: str
    faculty: str
    course: str
    lecturer: str
    evaluations: typing.List[str] = field(default_factory=list)

    def add_evaluations(self, new_evaluations: typing.List[str]) -> None:
        """
        Adds multiple evaluations to the existing evaluations.

        Args:
            new_evaluations (List[str]): List of evaluations to be added.
        """
        self.evaluations.extend(new_evaluations)

    def save_to_database(self, database: AbstractDatabaseInterface):
        """
        Saves the evaluation to the database.

        Args:
            database (AbstractDatabaseInterface): Database to save the evaluation to.
        """
        if database.query(self.query, table="evaluations"):
            database.update(data=self.dict, table="evaluations", query=self.query)
        else:
            database.insert(data=self.dict, table="evaluations")

    @property
    def query(self) -> typing.Dict[str, str]:
        """
        Returns the query for the evaluation.

        Returns:
            dict: Query for the evaluation.
        """
        return {
            "semester": self.semester,
            "cohort": self.cohort,
            "faculty": self.faculty,
            "course": self.course,
            "lecturer": self.lecturer,
        }

    @property
    def dict(self) -> typing.Dict[str, typing.Union[str, typing.List[str]]]:
        """Converts the dataclass to a dictionary"""
        return {
            "semester": self.semester,
            "cohort": self.cohort,
            "faculty": self.faculty,
            "course": self.course,
            "lecturer": self.lecturer,
            "evaluations": self.evaluations,
        }
