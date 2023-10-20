"""Generates dummy data and stores it in the database.""" ""
from evaluation_infrastructure.config.config_database import ConfigDatabase
from evaluation_infrastructure.logic.evaluation_system import EvaluationSystem
from evaluation_infrastructure.database_access.mongo_interface import MongoInterface
from evaluation_infrastructure.logic.dummy_generator import generate_dummy_data

mongo_interface = MongoInterface(ConfigDatabase.host)
evaluation_system = EvaluationSystem(mongo_interface)
generate_dummy_data(evaluation_system=evaluation_system)
# quit()
evaluation_system.backup_to_database()
