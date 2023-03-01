#!/bin/bash

[ ! -e test_database.db ] && { exit 2; } # Skip if test file does not exist

uni_lines="$(sqlite3 'test_database.db' <<< 'SELECT * FROM University;' | wc -l)"

[ "$uni_lines" -eq "5" ] || { echo "Wrong number of rows in University table"; \
    exit 1 ; }

