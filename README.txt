User Management API Microservice (Powered by Flask + PostgreSQL + Docker)

Overview
This project implements a containerized microservice for user management. The API is built with Flask and Flask-SQLAlchemy and uses PostgreSQL as the database. The application and database are orchestrated using Docker Compose.

The service exposes REST endpoints to create, retrieve, update, and delete users. All data is stored in a PostgreSQL container.

Technologies Used
Python
Flask
Flask-SQLAlchemy
PostgreSQL
Docker
Docker Compose

Project Files
app.py – Flask API with all routes and database models
requirements.txt – Python dependencies
Dockerfile – Container build instructions for the Flask API
docker-compose.yml – Multi-container configuration for the API and PostgreSQL database

Prerequisites
Docker Desktop installed and running
Docker Compose available (included with Docker Desktop)
Git installed (optional if cloning the repository)

Setup Instructions

Clone the Repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

cd YOUR_REPO_NAME

If downloading manually, extract the project and navigate to the project directory.

Verify Docker is Running

docker version

If Docker is running correctly, version information will be displayed.

Build and Start the Containers

From the root of the project directory (where docker-compose.yml is located):

docker compose up --build

This command will:

Build the Flask application image from the Dockerfile
Pull the PostgreSQL image
Create a shared network for the containers
Start the API container and the PostgreSQL container

The API container will start on port 4000.

Verify the Containers

Open a new terminal and run:

docker compose ps

You should see both containers running:

nov_microservice
flask_db

Test the API

Open a browser or use curl to verify the service is running.

Test endpoint:

http://localhost:4000/test

Expected response:

{"message":"API is working!"}

API Endpoints

Create User

POST /users

Example request:

curl -X POST http://localhost:4000/users

-H "Content-Type: application/json"
-d '{"username":"john","email":"john@example.com
"}'

Get All Users

GET /users

Example:

curl http://localhost:4000/users

Get User by ID

GET /users/{id}

Example:

curl http://localhost:4000/users/1

Update User

PUT /users/{id}

Example:

curl -X PUT http://localhost:4000/users/1

-H "Content-Type: application/json"
-d '{"username":"john_updated","email":"john_updated@example.com
"}'

Delete User

DELETE /users/{id}

Example:

curl -X DELETE http://localhost:4000/users/1

Stopping the Application

To stop the containers:

docker compose down

To stop and remove database data volumes:

docker compose down -v

Viewing Logs

To view application logs:

docker compose logs -f flask_app

To view database logs:

docker compose logs -f flask_db

Database Configuration

The Flask application reads the database connection string from the environment variable DB_URL.

In docker-compose.yml it is configured as:

postgresql+psycopg://postgres:postgres@flask_db:5432/postgres

The hostname flask_db works because Docker Compose automatically creates a shared network between services.

Notes

The database tables are created automatically when the application starts.
All services run inside containers and do not require local Python installation.
The API is accessible from the host machine through port 4000.

End of README.
