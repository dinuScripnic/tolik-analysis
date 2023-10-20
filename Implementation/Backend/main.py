"""File to start the backend server for development purposes."""
from evaluation_infrastructure.logic.evaluation_system import EvaluationSystem
from evaluation_infrastructure.database_access.mongo_interface import MongoInterface
from evaluation_infrastructure.api.rest_api import RestService
from evaluation_infrastructure.config.config_database import ConfigDatabase

mongo_interface = MongoInterface(ConfigDatabase.host)
evaluation_system = EvaluationSystem(mongo_interface)
RestService(evaluation_system).run()
