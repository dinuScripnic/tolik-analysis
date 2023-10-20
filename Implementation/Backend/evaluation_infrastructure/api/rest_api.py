"""Rest API for the evaluation system."""
import json

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn
import pydantic

from evaluation_infrastructure import errors as custom_errors
from evaluation_infrastructure.models.evaluations import (
    SingleEvaluation,
    MultipleEvaluations,
)
from evaluation_infrastructure.logic.evaluation import Evaluation
from evaluation_infrastructure.logic.evaluation_system import EvaluationSystem
from evaluation_infrastructure.scheduler.backup_scheduler import Scheduler


class RestService:
    """Rest API for the evaluation system."""

    def __init__(self, evaluation_system: EvaluationSystem):
        """Initializes the RestService."""

        self.app = FastAPI(title="Student Evaluation API")

        self.evaluation_system = evaluation_system

        self.declare_endpoints()
        self.declare_exception_handlers()
        self.configure_middlewares()

    def configure_middlewares(self):
        """
        Configures the middlewares for the FastAPI application.
        In the current configuration, all origins are allowed.
        """
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allow requests from all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allow all HTTP methods
            allow_headers=["*"],  # Allow all headers
        )

    def declare_endpoints(self):
        """
        Declares the endpoints for the FastAPI application.
        """

        @self.app.post("/evaluation/single", status_code=201)
        async def single_evaluation(evaluation: SingleEvaluation) -> None:
            """_summary_

            Args:
                evaluation (SingleEvaluation): _description_

            Returns:
                _type_: _description_
            """
            evaluation.evaluations = [evaluation.evaluations]
            response = self.evaluation_system.add_or_update_evaluation(
                Evaluation(**evaluation.model_dump())
            )
            return {"detail": response}

        @self.app.post("/evaluation/multiple", status_code=201)
        async def multiple_evaluations(evaluations: MultipleEvaluations):
            """_summary_

            Args:
                evaluations (MultipleEvaluations): _description_

            Returns:
                _type_: _description_
            """
            response = self.evaluation_system.add_or_update_evaluation(
                Evaluation(**evaluations.model_dump())
            )
            return {"detail": response}

        @self.app.post("/evaluation/file", status_code=201)
        async def file_evaluation(file: UploadFile):
            """_summary_

            Args:
                file (UploadFile): File containing the evaluations.

            Returns:

            """
            contents = await file.read()
            if file.content_type != "application/json":
                return HTTPException(
                    status_code=422,
                    detail="Invalid file format. Only JSON files are allowed.",
                )
            try:
                data = json.loads(contents)
                try:
                    data = MultipleEvaluations(**data)
                except pydantic.ValidationError as exc:
                    raise HTTPException(
                        status_code=422,
                        detail=f"Invalid file format. {exc.json()}",
                    ) from exc
                data = MultipleEvaluations(**json.loads(contents))
                response = self.evaluation_system.add_or_update_evaluation(
                    Evaluation(**data.model_dump())
                )
                return {"detail": response}
            except pydantic.ValidationError:
                return HTTPException(status_code=422, detail="Invalid file format.")

        @self.app.get("/evaluations/course/{course}", status_code=200)
        async def get_evaluations_by_course(course: str):
            """_summary_

            Args:
                course (str): _description_

            Raises:
                HTTPException: _description_

            Returns:
                _type_: _description_
            """
            try:
                evaluation = self.evaluation_system.get_evaluations_by_course(course)
            except custom_errors.CourseNotFoundError as exc:
                raise HTTPException(
                    status_code=404, detail="Evaluation not found."
                ) from exc
            return evaluation

        @self.app.get("/evaluations/cohort/{cohort}", status_code=200)
        async def get_evaluations_by_cohort(cohort: str):
            """_summary_

            Args:
                cohort (str): _description_

            Raises:
                HTTPException: _description_

            Returns:
                _type_: _description_
            """
            try:
                evaluation = self.evaluation_system.get_evaluations_by_cohort(cohort)
            except custom_errors.CohortNotFoundError as exc:
                raise HTTPException(
                    status_code=404, detail="Evaluation not found."
                ) from exc
            return evaluation

        @self.app.get("/courses/list", status_code=200)
        async def get_courses_list():
            """_summary_

            Returns:
                _type_: _description_
            """
            return self.evaluation_system.get_all_courses()

        @self.app.get("/cohorts/list", status_code=200)
        async def get_cohorts_list():
            """_summary_

            Returns:
                _type_: _description_
            """
            return self.evaluation_system.get_all_cohorts()

        @self.app.get("/faculties/list", status_code=200)
        async def get_faculties_list():
            """_summary_

            Returns:
                _type_: _description_
            """
            return self.evaluation_system.get_faculty_course_map()

        @self.app.get("/results/course/{course}", status_code=200)
        async def get_results_by_course(course: str):
            return self.evaluation_system.return_results(course)

    def declare_exception_handlers(self) -> None:
        """
        Rewrites the default exception handlers for the FastAPI application.
        """

        @self.app.exception_handler(RequestValidationError)
        async def custom_validation_exception_handler(
            request, exc: RequestValidationError
        ):
            """Returns a custom response for validation errors."""
            error_message = (
                exc.errors()[0]["msg"] if exc.errors() else "Invalid request."
            )
            return JSONResponse(
                status_code=422,
                content={"detail": error_message},
            )

    def run(self, host: str = "127.0.0.1", port: int = 8000):
        """Runs the FastAPI application."""
        self.evaluation_system.create_from_database()
        backup_scheduler = Scheduler()
        backup_scheduler.add_task(self.evaluation_system.backup_to_database, 60)
        backup_scheduler.start()

        uvicorn.run(self.app, host=host, port=port)
