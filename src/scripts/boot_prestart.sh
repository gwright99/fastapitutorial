#! /usr/bin/env bash

# Assume this script is invoked from the parent src/ directory.

# Executes a SQL SELECT 1 query to check that DB is working
python app/boot_backend_pre_start.py

# Run migrations
alembic upgrade head   # <---- ALEMBIC MIGRATION COMMAND

# Create initial data in DB
python app/boot_initial_data.py
