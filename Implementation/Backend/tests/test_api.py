"""Integration tests for the REST API."""
from pytest import fixture
from evaluation_infrastructure.api.rest_api import RestService
from fastapi.testclient import TestClient

test_client = TestClient(RestService().app)


@fixture(scope="function")
def rest_service_empty():
    """Fixture for a RestService with an empty evaluation system."""
    yield RestService()


@fixture(scope="function")
def rest_service_with_evaluation_system():
    pass


class TestGetList:
    def test_get_list_of_courses():
        """Test the get list of courses endpoint."""
        response = test_client.get("/courses/")
        assert response.status_code == 200
        assert response.json() == [
            "Introduction to Programming",
            "Algorithms and Data Structures",
        ]
