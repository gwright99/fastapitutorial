#! /usr/bin/env bash

# Executes a SQL SELECT 1 query to check that DB is working
python ./app/backend_pre_start.py

# Run migrations
alembic upgrade head   # <---- ALEMBIC MIGRATION COMMAND

# Create initial data in DB
python ./app/initial_data.py
