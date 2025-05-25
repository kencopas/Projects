# Capstone Project: Credit Card Data Engineering Pipeline

## Overview

This capstone project implements an end-to-end data engineering pipeline using PySpark and MySQL. The pipeline processes, transforms, and loads credit card data from various sources into a MySQL database for analysis and reporting. The project includes CLI-based interaction, modular transformation logic, and structured SQL scripts.

---

## Project Structure

```
Capstone/
├── application_data/            # Input data files (e.g., CSV, JSON)
├── cli_manager.py               # Command-line interface logic
├── config.json                  # Configuration for Spark and MySQL
├── main.py                      # Main application entry point
├── mapping/                     # Entity relationship mapping images
├── mysql-connector-j-9.3.0.jar  # JDBC driver for MySQL
├── sql_scripts/                 # SQL files for table creation and queries
├── transformers.py              # Custom transformation functions
└── utils/                       # Utility modules
    ├── cli_utils.py
    ├── spark_utils.py
    └── sql_utils.py
```

---

## Core Components

### 1. `main.py`

Initializes the application, Spark session, and database connection using:

- `EasySpark`: PySpark setup with external config.
- `SafeSQL`: MySQL interface with query execution.
- CLI and pipeline management through `CLIManager`.

### 2. `config.json`

Contains configuration settings including:

- JDBC connection details
- Path to MySQL driver
- PySpark Python path

### 3. `cli_manager.py`

Provides a CLI interface for interacting with the application, running workflows, and selecting data operations.

### 4. `transformers.py`

Houses transformation logic mapped to keys, with a dispatcher pattern. Includes supported file extensions and source API URLs.

### 5. `sql_scripts/`

Holds SQL files such as `init.sql` for creating necessary MySQL tables and schemas.

---

## How to Run

### Requirements

- Python 3.10+
- PySpark
- MySQL server
- Pandas
- JDBC connector

### Steps

1. Configure `config.json` with your environment paths and DB credentials.
2. Run the main application:
   ```bash
   python main.py
   ```
3. Use the CLI menu to run transformations, inspect data, and push results to MySQL.

---

## Notes

- Ensure that `mysql-connector-j-9.3.0.jar` is referenced correctly in your Spark session.
- The `application_data/` folder supports multiple file types defined in `SUPPORTED_EXTENSIONS`.

---

## License

This project is part of a data engineering capstone and is intended for educational use.
