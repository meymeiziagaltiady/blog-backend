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

This will also include the database migration. For manual migration, run the following command in the docker container:
   ```console
   alembic upgrade head
   ```

### 4. Access API Documentation
Swagger UI:
   ```console
   http://localhost:8000/docs
   ```
ReDoc
   ```console
   http://localhost:8000/redoc
   ```

Use `Authorize` button and put token from `/token` response

## Running Tests
Inside Docker container, run:
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