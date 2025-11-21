# Blog Backend Project

## About

A RESTful API backend using FastAPI for managing Users and Content (Blog/Articles). It includes authentication using JWT, authorization, CRUD operations, database migrations, and automated testing.

## Tech Stack

- FastAPI
- Alembic
- SQLAlchemy
- PostgreSQL
- Docker
- pytest

## How To Run

### 1. Clone this repository

```console
git clone https://github.com/meymeiziagaltiady/blog-backend.git
```

### 2. Create .env file

Copy and/or rename `.env.example` to `.env`

### 3. Run in Docker

```console
docker-compose up --build
```

The following services will start:
| Service | URL |
| -------- | ------- |
| Backend | http://localhost:8000 |
| PostgreSQL | localhost:54321 |

### 4. Migrate Database

Inside the backend Docker container, run:

```console
cd app
alembic upgrade head
```

### 5. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Use `Authorize` button and put token from `/token` response.

Example account:
| Username | Password | Role |
| -------- | ------- | ------- |
| admin | admin123 | admin |
| user | user123 | user |

## Running Tests

Inside the backend Docker container, run:

```console
PYTHONPATH=. pytest -vv
```

## Project Strcuture

```
app/
 ├── src/
 │    ├── config/
 │    ├── db/
 │    ├── exception/
 │    ├── jwt/
 │    ├── middleware/
 │    ├── route/
 │    ├── schema/
 │    ├── service/
 │    ├── utils/
 │    ├── main.py
 ├── alembic/
 ├── test/
.env
docker-compose.yml
Dockerfile
requirements.txt
```
