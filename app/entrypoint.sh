#!/bin/sh

echo "Running Alembic migrations..."
alembic -c app/alembic.ini upgrade head

echo "Starting FastAPI server..."
uvicorn app.src.main:app --host 0.0.0.0 --port 8000 --reload