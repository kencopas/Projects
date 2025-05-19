# This file is a short summary for scanning the project

## main.py

application, integrates utilities, config.json, init.sql, data.

## utils

holds PySpark and MySQL connector utilities

### spark_utils.py - EasySpark Class
        
- simplifies spark session connection
- handles configuration
- handles try-except clauses
- simplifies MySQL operations through spark

### sql_utils.py - SafeSQL Class

- simplifies MySQL operations
- eliminates the need for a cursor
- parses and runs multi-line queries
- handles safe committing and closing with error and query counting

## config.json

holds configurations for pyspark, jdbc, and mysql (created because of overlapping and confusing configurations)

## init.sql

holds sql queries for table initializations if they don't exist

## data

holds json files
