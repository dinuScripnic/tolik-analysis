"""File for testing the Evaluation class."""
import pytest

from evaluation_infrastructure.logic.evaluation import Evaluation


@pytest.fixture
def evaluation():
    """Fixture for an evaluation."""
    yield Evaluation(
        semester="WS20/21",
        cohort="1",
        faculty="Computer Science",
        course="Introduction to Programming",
        lecturer="Dr. John Doe",
        evaluations=["bad", "bad", "good"],
    )


class TestEvaluation:
    """Test class for the Evaluation class."""

    def test_create_evaluation(self, evaluation: Evaluation):
        """Test creating an evaluation."""

        assert evaluation.semester == "WS20/21"
        assert evaluation.cohort == "1"
        assert evaluation.faculty == "Computer Science"
        assert evaluation.course == "Introduction to Programming"
        assert evaluation.lecturer == "Dr. John Doe"
        assert sorted(evaluation.evaluations) == sorted(["good", "bad", "bad"])

    def test_add_multiple_evaluations(self, evaluation: Evaluation):
        """Test adding multiple evaluations to an existing evaluation."""

        evaluation.add_multiple_evaluations(["good", "good", "good"])

        assert sorted(evaluation.evaluations) == sorted(
            ["bad", "bad", "good", "good", "good", "good"]
        )
