from dataclasses import dataclass
from datetime import datetime, date
import typing

import pydantic
from evaluation_infrastructure.logic.my_abstract_dataclass import (
    AbstractDataclass,
)
from evaluation_infrastructure.database_access.abstract_database_interface import (
    AbstractDatabaseInterface,
)


def semester_to_end_date(semester_label: str) -> datetime:
    """
    Converts a semester label to the end date of the semester

    Args:
        semester_label (str): Semester label to be converted

    Returns:
        datetime: End date of the semester
    """
    if semester_label.startswith("WS"):
        parts = semester_label.split("/")
        year_end = int(parts[1]) + 2000
        return datetime(year_end, 1, 31).date()
    elif semester_label.startswith("SS"):
        year_end = int(semester_label[2:]) + 2000
        return datetime(year_end, 6, 30).date()
    # have to add an regex to check if the semester label is valid
    # that must be done at input validation
    else:
        return None


class ResultOutputDashboard(pydantic.BaseModel):
    """
    Result type for a course for all semesters
    To be used for the dashboard
    """

    faculty: str
    course: str
    lecturer: str
    semesters: typing.List[date]
    topics: typing.Dict[str, typing.List[float]]


@dataclass
class ResultType:
    """Resilt type for a course for a semester"""

    semester: str
    topics_distribution: typing.Dict[str, float]


@dataclass
class Result(AbstractDataclass):
    """result for a course"""

    faculty: str
    course: str
    lecturer: str
    results: typing.List[ResultType]

    def return_results(self) -> ResultOutputDashboard:
        """
        Returns the results for a course for all semesters

        Returns:
            ResultOutputDashboard: Result type for a course for all semesters
        """
        topic_list = set()
        for result in self.results:
            for topic in result.topics_distribution.keys():
                topic_list.add(topic)
        semesters = []
        topic_dict: dict[str, list[int]] = {topic: [] for topic in topic_list}
        for result in self.results:
            semesters.append(semester_to_end_date(result.semester))
            for topic in topic_list:
                topic_dict[topic].append(result.topics_distribution.get(topic, 0))
        return ResultOutputDashboard(
            faculty=self.faculty,
            course=self.course,
            lecturer=self.lecturer,
            semesters=semesters,
            topics=topic_dict,
        )

    @property
    def query(self) -> typing.Dict[str, str]:
        """Creates a query for the database"""
        return {
            "faculty": self.faculty,
            "course": self.course,
            "lecturer": self.lecturer,
        }

    @property
    def dict(self) -> dict:
        """Converts the dataclass to a dictionary"""
        return {
            "faculty": self.faculty,
            "course": self.course,
            "lecturer": self.lecturer,
            "results": [result.__dict__ for result in self.results],
        }

    def save_to_database(self, database: AbstractDatabaseInterface) -> None:
        """
        Saves the result to the database.

        Args:
            database (AbstractDatabaseInterface): Database to save the result to.
        """
        if database.query(self.query, table="results"):
            database.update(data=self.dict, table="results", query=self.query)
        else:
            database.insert(data=self.dict, table="results")
