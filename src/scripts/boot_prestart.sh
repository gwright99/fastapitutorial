#! /usr/bin/env bash

# Assume this script is invoked from the parent src/ directory.

# Executes a SQL SELECT 1 query to check that DB is working
python boot/01_backend_pre_start.py

# Run migrations
# This assumes that you have initialized Alembic and created at least 1 migration.
alembic upgrade head

# Create initial data in DB
python boot/02_load_initial_data.py
