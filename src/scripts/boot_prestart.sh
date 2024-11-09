#! /usr/bin/env bash

# Assume this script is invoked from the parent project root directory.

# Executes a SQL SELECT 1 query to check that DB is working
python src/boot/01_backend_pre_start.py

# Run migrations
# This assumes that you have initialized Alembic and created at least 1 migration.
alembic -c src/alembic.ini upgrade head

# Create initial data in DB
python src/boot/02_load_initial_data.py
