"""Unit tests for the evaluation system."""
import pytest

from evaluation_infrastructure.logic.evaluation_system import EvaluationSystem
from evaluation_infrastructure.logic.evaluation import Evaluation
from evaluation_infrastructure import errors as custom_errors


@pytest.fixture
def empty_evaluation_system():
    """Fixture for an empty evaluation system."""
    yield EvaluationSystem()


@pytest.fixture
def evaluation_system_with_evaluations():
    """Fixture for an evaluation system with evaluations."""
    evaluation_system = EvaluationSystem()
    evaluation_programming_1 = Evaluation(
        semester="WS20/21",
        cohort="1",
        faculty="Computer Science",
        course="Introduction to Programming",
        lecturer="Dr. John Doe",
        evaluations=["bad", "bad", "good"],
    )
    evaluation_programming_2 = Evaluation(
        semester="WS21/22",
        cohort="1",
        faculty="Computer Science",
        course="Introduction to Programming",
        lecturer="Dr. John Doe",
        evaluations=["good", "good", "good"],
    )
    evaluation_system.add_or_update_evaluation(evaluation_programming_1)
    evaluation_system.add_or_update_evaluation(evaluation_programming_2)

    evaluation_data_science_1 = Evaluation(
        semester="WS20/21",
        cohort="2",
        faculty="Computer Science",
        course="Data Science",
        lecturer="Dipl. Ing. Jane Jane",
        evaluations=["good", "good", "good"],
    )

    evaluation_data_science_2 = Evaluation(
        semester="WS21/22",
        cohort="2",
        faculty="Computer Science",
        course="Data Science",
        lecturer="Dipl. Ing. Jane Jane",
        evaluations=["good", "good", "good"],
    )
    evaluation_system.add_or_update_evaluation(evaluation_data_science_1)
    evaluation_system.add_or_update_evaluation(evaluation_data_science_2)

    yield evaluation_system


class TestEvaluationSystem:
    """Test the evaluation system."""

    def test_create_evaluation_system(self, empty_evaluation_system: EvaluationSystem):
        """
        Test creating an evaluation system.
        Tests if the evaluation system is created with the correct values.

        Args:
            evaluation_system (EvaluationSystem): Evaluation system to be tested.
        """

        assert empty_evaluation_system
        assert empty_evaluation_system.evaluations == []
        assert empty_evaluation_system.cohort_map == {}
        assert empty_evaluation_system.course_map == {}

    def test_get_missing_evaluation_by_course(
        self, evaluation_system_with_evaluations: EvaluationSystem
    ):
        """
        Test getting an evaluation that does not exist.
        Tests if the evaluation system returns None when getting an evaluation that does not exist.

        Args:
            evaluation_system (EvaluationSystem): Evaluation system to be tested.
        """
        with pytest.raises(custom_errors.CourseNotFoundError):
            evaluation_system_with_evaluations.get_evaluations_by_course(
                "Not Existing Course"
            )

    def test_get_evaluation_by_course(
        self, evaluation_system_with_evaluations: EvaluationSystem
    ):
        """
        Test getting an evaluation that does exist.
        Tests if the evaluation system returns the correct evaluation when getting an evaluation that does exist.

        Args:
            evaluation_system (EvaluationSystem): Evaluation system to be tested.
        """
        evaluation = evaluation_system_with_evaluations.get_evaluations_by_course(
            "Introduction to Programming"
        )
        for eval in evaluation:
            assert eval.course == "Introduction to Programming"

    def test_get_missing_evaluation_by_cohort(
        self, evaluation_system_with_evaluations: EvaluationSystem
    ):
        """
        Test getting an evaluation that does not exist.
        Tests if the evaluation system returns None when getting an evaluation that does not exist.

        Args:
            evaluation_system (EvaluationSystem): Evaluation system to be tested.
        """
        with pytest.raises(custom_errors.CohortNotFoundError):
            evaluation_system_with_evaluations.get_evaluations_by_cohort(
                "Not Existing Cohort"
            )

    def test_get_evaluation_by_cohort(
        self, evaluation_system_with_evaluations: EvaluationSystem
    ):
        """
        Test getting an evaluation that does exist.
        Tests if the evaluation system returns the correct evaluation when getting an evaluation that does exist.

        Args:
            evaluation_system (EvaluationSystem): Evaluation system to be tested.
        """
        evaluation = evaluation_system_with_evaluations.get_evaluations_by_cohort("1")

        for eval in evaluation:
            assert eval.cohort == "1"

        evaluation = evaluation_system_with_evaluations.get_evaluations_by_cohort("2")

        for eval in evaluation:
            assert eval.cohort == "2"


class TestAddAndUpdateEvaluation:
    """Test adding and updating evaluations."""

    def test_add_evaluation(self, empty_evaluation_system: EvaluationSystem):
        """
        Test adding an evaluation.
        Tests if the evaluation system adds the evaluation correctly.

        Args:
            evaluation_system (EvaluationSystem): Evaluation system to be tested.
        """
        evaluation = Evaluation(
            semester="WS20/21",
            cohort="1",
            faculty="Computer Science",
            course="Introduction to Programming",
            lecturer="Dr. John Doe",
            evaluations=["bad", "bad", "good"],
        )

        empty_evaluation_system.add_or_update_evaluation(evaluation)

        assert empty_evaluation_system.evaluations == [evaluation]

    def test_update_evaluation(
        self, evaluation_system_with_evaluations: EvaluationSystem
    ):
        """
        Test updating an evaluation.
        Tests if the evaluation system updates the evaluation correctly.

        Args:
            evaluation_system (EvaluationSystem): Evaluation system to be tested.
        """
        new_evaluation = Evaluation(
            semester="WS20/21",
            cohort="1",
            faculty="Computer Science",
            course="Introduction to Programming",
            lecturer="Dr. John Doe",
            evaluations=["good", "good", "good", "cock"],
        )
        new_evaluation_text = list(new_evaluation.evaluations)
        initial_length = len(evaluation_system_with_evaluations.evaluations)
        inintial_evaluation = list(
            evaluation_system_with_evaluations.evaluations[0].evaluations
        )
        evaluation_system_with_evaluations.add_or_update_evaluation(new_evaluation)
        assert (
            len(evaluation_system_with_evaluations.evaluations) == initial_length
        )  # no new evaluation was added
        assert (
            evaluation_system_with_evaluations.evaluations[0].evaluations
            != inintial_evaluation
        )
        print(evaluation_system_with_evaluations.evaluations[0])
        print(inintial_evaluation.extend(new_evaluation_text))
        assert sorted(
            evaluation_system_with_evaluations.evaluations[0].evaluations
        ) == sorted(inintial_evaluation.extend(new_evaluation_text))
