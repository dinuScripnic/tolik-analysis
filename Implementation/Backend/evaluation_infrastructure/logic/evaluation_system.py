"""Implementation of the Evaluation System."""

import typing
from collections import defaultdict
from evaluation_infrastructure.logic.result import (
    Result,
    ResultOutputDashboard,
    ResultType,
)
from evaluation_infrastructure.database_access.abstract_database_interface import (
    AbstractDatabaseInterface,
)

from evaluation_infrastructure.logic.evaluation import Evaluation
from evaluation_infrastructure.logger import logger
import evaluation_infrastructure.errors as custom_errors


class EvaluationSystem:
    """
    Evaluation system for the courses.
    Holds the evaluations and results for the courses.
    """

    def __init__(self, database_interface: AbstractDatabaseInterface):
        """
        Initializes the evaluation system.
        Evaluations are stored in a list of Evaluation objects.
        The Evauation System is backed up to the database every [Backup Interval] Minutes.
        """
        self.database_interface = database_interface

        self.evaluations: typing.List[Evaluation] = []
        self.results: typing.List[Result] = []
        self.faculty_course_map: typing.Dict[str, typing.Set[str]] = defaultdict(set)
        self.course_map: typing.Dict[str, typing.List[Evaluation]] = defaultdict(list)
        self.cohort_map: typing.Dict[str, typing.List[Evaluation]] = defaultdict(list)

    def get_evaluations_by_course(
        self, course: str
    ) -> typing.Optional[typing.List[Evaluation]]:
        """
        Returns the evaluation for the given course if it exists, otherwise returns None.

        Args:
            course (str): Course for which the evaluation is to be retrieved.

        Returns:
            typing.Optional[Evaluation]: Evaluation for the given course if it exists, otherwise None.
        """
        if output := self.course_map.get(course):
            return output
        raise custom_errors.CourseNotFoundError

    def get_evaluations_by_cohort(
        self, cohort_name: str
    ) -> typing.Optional[typing.List[Evaluation]]:
        """
        Returns the evaluations for the given cohort if it exists, otherwise returns None.

        Args:
            cohort_name (str): Cohort for which the evaluations are to be retrieved.

        Returns:
            typing.List[Evaluation]: Evaluations for the given cohort if it exists, otherwise None.
        """
        if output := self.cohort_map.get(cohort_name):
            return output
        raise custom_errors.CohortNotFoundError

    def get_evaluation(
        self,
        semester_name: str,
        cohort_name: str,
        faculty_name: str,
        course_name: str,
        lecturer_name: str,
    ) -> typing.Optional[Evaluation]:
        """
        Returns the evaluation for the given course if it exists, otherwise returns None.

        Args:
            semester_name (str): Semester for which the evaluation is to be retrieved.
            cohort_name (str): Cohort for which the evaluation is to be retrieved.
            faculty_name (str): Faculty for which the evaluation is to be retrieved.
            course_name (str): Course for which the evaluation is to be retrieved.
            lecturer_name (str): Lecturer for which the evaluation is to be retrieved.

        Returns:
            typing.Optional[Evaluation]: Evaluation, if it exists, otherwise error.
        """
        for single_evaluation in self.evaluations:
            if (
                single_evaluation.semester == semester_name
                and single_evaluation.cohort == cohort_name
                and single_evaluation.faculty == faculty_name
                and single_evaluation.course == course_name
                and single_evaluation.lecturer == lecturer_name
            ):
                return single_evaluation
        raise custom_errors.EvaluationNotFoundError

    def return_results(self, course: str) -> ResultOutputDashboard:
        """
        Returns the results for a course for all semesters

        Args:
            course (str): Course for which the results are to be retrieved.

        Returns:
            ResultOutputDashboard: Result type for a course for all semesters
        """
        for result in self.results:
            if result.course == course:
                return result.return_results()

    def _add_result(self, result: Result) -> None:
        self.results.append(result)

    def add_or_update_evaluation(self, new_evaluation: Evaluation) -> str:
        """
        If the course is already in the system, then the evaluation is added to the existing evaluation.

        Args:
            evaluation (Evaluation): Evaluation to be added or updated.

        Returns:
            str: Updated or added successfully.
        """
        try:
            check_evaluation = self.get_evaluation(
                new_evaluation.semester,
                new_evaluation.cohort,
                new_evaluation.faculty,
                new_evaluation.course,
                new_evaluation.lecturer,
            )
            check_evaluation.add_evaluations(new_evaluation.evaluations)
            return "Evaluation updated successfully."
        except custom_errors.EvaluationNotFoundError:
            self._add_new_evaluation(new_evaluation)
            return "Evaluation added successfully."

    def _add_new_evaluation(self, new_evaluation: Evaluation) -> None:
        """
        Adds a new evaluation to the system.

        Args:
            new_evaluation (Evaluation): Evaluation to be added.
        """
        self.evaluations.append(new_evaluation)
        self.faculty_course_map[new_evaluation.faculty].add(new_evaluation.course)
        self.course_map[new_evaluation.course].append(new_evaluation)
        self.cohort_map[new_evaluation.cohort].append(new_evaluation)

    def get_faculty_course_map(self) -> typing.Dict[str, typing.Set[str]]:
        """
        Returns the faculty course map.

        Returns:
            typing.Dict[str, typing.Set[str]]: Faculty course map.
        """
        return self.faculty_course_map

    def get_all_courses(self) -> typing.List[str]:
        """
        Returns a list of all courses.

        Returns:
            typing.List[str]: List of all courses.
        """
        return list(self.course_map.keys())

    def get_all_cohorts(self) -> typing.List[str]:
        """
        Returns a list of all cohorts.

        Returns:
            typing.List[str]: List of all cohorts.
        """
        return list(self.cohort_map.keys())

    def _initialize_evaluations(self):
        """Initializes the evaluations from the database."""
        for evaluation in self.database_interface.fetch(table="evaluations"):
            self._add_new_evaluation(Evaluation(**evaluation))
        logger.info("Evaluations initialized.")

    def _initialize_results(self):
        """Initializes the results from the database."""
        for result in self.database_interface.fetch(table="results"):
            self.results.append(
                Result(
                    course=result["course"],
                    lecturer=result["lecturer"],
                    faculty=result["faculty"],
                    results=[
                        ResultType(**single_result)
                        for single_result in result["results"]
                    ],
                )
            )
        logger.info("Results initialized.")

    def create_from_database(self):
        """Creates the evaluation system from fetched data."""
        self._initialize_evaluations()
        self._initialize_results()
        logger.info("Evaluation system created from database.")

    def _backup_evaluation(self):
        """Backs up the evaluations to the database."""
        for evaluation in self.evaluations:
            evaluation.save_to_database(self.database_interface)

    def _backup_result(self):
        """Backs up the results to the database."""
        for result in self.results:
            result.save_to_database(self.database_interface)

    def backup_to_database(self):
        """Saves the evaluations to the database."""
        self._backup_evaluation()
        self._backup_result()
        logger.info("Evaluation system backed up to database.")
