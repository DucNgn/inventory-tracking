# Inventory Management API

Interactive deployed API at: www.inventoryapi.ducnguyen.dev/docs

<p align="center">
    <img src="./docs/demo_swaggerUI.png" />
</p>

## Tech Stack
+ FastAPI (with Swagger UI)
+ MongoDB
+ Python
+ Docker and Compose

## Setup

### .env
+ `cp example.env .env` to create environment file.
+ Change the content of the `.env` file to the local environment. For example:
    ```
    APP_NAME="Inventory Tracking API"
    MONGO_URI=mongodb://localhost:27017
    ```
    is a valid configuration for the default MongoDB.

### Build using docker and docker-compose (recommended):

+ `docker-compose up --build -d` to start building the containers in the background.
+ Go to `localhost:8000/docs` to access the interactive Swagger UI of the API.

### Build without Docker:

+ Install [poetry](https://python-poetry.org/) - the Python dependency management
+ `poetry shell` to create a virtual environment of the project.
+ `poetry install` to install dependencies.
+ `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload` to start the API service in development mode (hot reload).
+ Go to `localhost:8000/docs` to access the interactive Swagger UI of the API.

## Features:

### For clients:
+ [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) Functionality. Users are able to:
  + Create new item in the inventory
  + View item by ID
  + View all items in the inventory
  + Delete item by ID
  + Update item by ID
+ Export all products in the inventory to a CSV file.

### For developers:
+ [Swagger UI](https://swagger.io/tools/swagger-ui), allows visualizing and interacting with the API without a front-end. It was auto generated from OpenAPI from FastAPI.
+ Async functionalities.
+ Easy, extendable models and schemas.
+ Schemas are validated by [Pydantic](https://pydantic-docs.helpmanual.io/).
+ Wrapped `ObjectID` (`_id` field) from MongoDB by a custom field, compatible with openapi standard. More information [here](https://github.com/tiangolo/fastapi/issues/1515).
+ Environment file is parsed by `.env`, validated by [Pydantic](https://pydantic-docs.helpmanual.io/)
+ Containerized with [Docker](https://www.docker.com/) and [Compose](https://docs.docker.com/compose/) for easy deployment.
+ [pre-commit hook](https://pre-commit.com/) for auto linting before git commit.


## Code Organization:


## Deployment:
The project is containerized with docker-compose and deployed with docker-compose on my personal [Digital Ocean](https://www.digitalocean.com/) VM.
