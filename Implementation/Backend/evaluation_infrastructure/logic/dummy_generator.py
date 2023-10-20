"""Script to generate dummy data for the evaluation system.""" ""
import random
import typing

from lorem_text import lorem

from evaluation_infrastructure.logic.evaluation_system import EvaluationSystem
from evaluation_infrastructure.logic.evaluation import Evaluation
from evaluation_infrastructure.logic.result import Result, ResultType

faculties = [
    "Informatics",
    "Business Administration",
    "Applied Chemistry",
    "Biotechnology",
    "Tourism and Management",
]
courses = [
    "Introduction to Programming",
    "Financial Accounting",
    "Organic Chemistry",
    "Genetic Engineering",
    "Hospitality Management",
    "Data Structures",
    "Marketing Management",
    "Analytical Chemistry",
    "Bioinformatics",
    "Tourism Marketing",
    "Web Development",
    "Strategic Management",
    "Physical Chemistry",
    "Microbiology",
    "Event Planning",
    "Database Design",
    "Human Resource Management",
    "Inorganic Chemistry",
    "Bioprocess Engineering",
    "Hospitality Operations",
]
cohorts = [
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
]
semesters = [
    "WS19/20",
    "SS20",
    "WS20/21",
    "SS21",
    "WS21/22",
    "SS22",
    "WS22/23",
    "SS23",
]
lecturers = [
    "Deepak Dhungana",
    "Roger Hage",
    "Alesio Gambi",
    "Ruben Ruiz Torrubiano",
    "Danilo Valerio",
    "Sarita Paudel",
    "Johanna Schmitt",
]
topics = [
    "Topic 1",
    "Topic 2",
    "Topic 3",
    "Topic 4",
    "Topic 5",
    "Topic 6",
    "Topic 7",
    "Topic 8",
    "Topic 9",
]


def generate_evaluation() -> typing.List[str]:
    """
    Generates a list of evaluations.

    Returns:
        typing.List[str]: List of evaluations.
    """
    return [
        "\n".join([lorem.paragraph() for _ in range(random.randint(1, 5))])
        for _ in range(random.randint(1, 50))
    ]


def generate_result() -> typing.List[ResultType]:
    """Dummy result generator"""
    results = []
    for semester in semesters:
        result_topics = random.sample(topics, random.randint(3, len(topics)))
        topics_distribution = {}
        total_weight = 0
        for topic in result_topics:
            weight = random.uniform(0, 1 - total_weight)
            topics_distribution[topic] = weight
            total_weight += weight

        if total_weight < 1:
            remaining_topic = random.choice(result_topics)
            topics_distribution[remaining_topic] += 1 - total_weight
        topics_distribution = dict(sorted(topics_distribution.items()))

        results.append(
            ResultType(
                semester=semester,
                topics_distribution=topics_distribution,
            )
        )
    return results


def generate_dummy_data(evaluation_system: EvaluationSystem):
    """
    Generates dummy data for the evaluation system.
    """

    for _ in range(300):
        evaluation = Evaluation(
            semester=random.choice(semesters),
            cohort=random.choice(cohorts),
            faculty=random.choice(faculties),
            course=random.choice(courses),
            lecturer=random.choice(lecturers),
            evaluations=generate_evaluation(),
        )
        evaluation_system._add_new_evaluation(
            evaluation
        )  # pylint: disable=protected-access

    for course in evaluation_system.get_all_courses():
        result = Result(
            faculty=random.choice(faculties),
            course=course,
            lecturer=random.choice(lecturers),
            results=generate_result(),
        )
        # generate a dummy result
        evaluation_system._add_result(result)
