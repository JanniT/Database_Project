#!/bin/bash

[ -e test_database.db ] && { exit 2; } # Skip if test file exists

sqlite3 "test_database.db" < "../db/create_table.sql"

[ -e test_database.db ] || { echo "Failed to create database file"; exit 1 ; }

