"""Models for the backend."""
import typing

import pydantic


class BaseEvaluation(pydantic.BaseModel):
    """
    Base model for an evaluation.
    """

    semester: str = pydantic.Field(examples=["WS22/23"])
    cohort: str = pydantic.Field(examples=["BSc"])
    faculty: str = pydantic.Field(examples=["Informatics"])
    course: str = pydantic.Field(examples=["Programming"])
    lecturer: str = pydantic.Field(examples=["Deepak Dhungana"])
    evaluations: typing.Union[str, typing.List[str]]


class SingleEvaluation(BaseEvaluation):
    """
    Base model for an evaluation with a single evaluation.
    """

    evaluations: str = pydantic.Field(examples=["Some evaluation how the course went."])


class MultipleEvaluations(BaseEvaluation):
    """
    Base model for an evaluation with multiple evaluations.
    """

    evaluations: typing.List[str] = pydantic.Field(
        examples=[
            [
                "Some evaluation how the course went.",
                "Some other evaluation how the course went.",
                "Yet another evaluation how the course went.",
            ]
        ]
    )
