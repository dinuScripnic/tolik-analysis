"""Initializes the REST API and starts the server."""

import uvicorn
from evaluation_infrastructure.api.rest_api import RestService

if __name__ == "__main__":
    RestService().run(host="0.0.0.0", port=8000)
