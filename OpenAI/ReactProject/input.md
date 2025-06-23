File Structure:

```json
{
  "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject",
  "subpaths": [
    {
      "contents": "[actual JSON data truncated for brevity]",
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\cdw_sapp_customer.json"
    },
    {
      "contents": "import click\nfrom db import get_db_connection, setup_database\n\n@click.group()\ndef cli():\n    pass\n\n@cli.command()\ndef show_tables():\n    conn = get_db_connection()\n    cursor = conn.cursor()\n    cursor.execute('SHOW TABLES')\n    for table in cursor.fetchall():\n        print(table)\n    cursor.close()\n    conn.close()\n\nif __name__ == '__main__':\n    setup_database()\n    cli()\n",
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\cli.py"
    },
    {
      "contents": "{ \"mysql\": { \"host\": \"localhost\", \"user\": \"root\", \"password\": \"password\", \"database\": \"etl_project\" }, \"data_path\": \"C:\\\\Users\\\\kenneth.copas\\\\OneDrive - PeopleShores PBC\\\\Desktop\\\\Projects\\\\OpenAI\\\\ETLProject\\\\cdw_sapp_customer.json\" }",
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\config.json"
    },
    {
      "contents": "import mysql.connector\nimport os\nimport json\n\ndef get_db_connection():\n    config_path = os.path.join(os.path.dirname(__file__), 'config.json')\n    with open(config_path) as config_file:\n        config = json.load(config_file)\n    try:\n        connection = mysql.connector.connect(\n            host=config['mysql']['host'],\n            user=config['mysql']['user'],\n            password=config['mysql']['password'],\n            database=config['mysql']['database']\n        )\n        return connection\n    except mysql.connector.Error as err:\n        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:\n            print('Database does not exist. Attempting to create it...')\n            create_database()\n        else:\n            print(f'Error connecting to the database: {err}')\n            exit(1)\n\ndef create_database():\n    config_path = os.path.join(os.path.dirname(__file__), 'config.json')\n    with open(config_path) as config_file:\n        config = json.load(config_file)\n    connection = mysql.connector.connect(\n        host=config['mysql']['host'],\n        user=config['mysql']['user'],\n        password=config['mysql']['password']\n    )\n    cursor = connection.cursor()\n    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {config['mysql']['database']}')\n    connection.commit()\n    cursor.close()\n    connection.close()\n    setup_database()\n\n\ndef setup_database():\n    conn = get_db_connection()\n    cursor = conn.cursor()\n    with open('C:\\\\Users\\\\kenneth.copas\\\\OneDrive - PeopleShores PBC\\\\Desktop\\\\Projects\\\\OpenAI\\\\ETLProject\\\\setup.sql', 'r') as sql_file:\n        sql_commands = sql_file.read()\n        for command in sql_commands.split(';'):\n            if command.strip():  # Only execute non-empty commands\n                cursor.execute(command)\n    conn.commit()\n    cursor.close()\n    conn.close()\n",
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\db.py"
    },
    {
      "contents": "from extract import extract_data\nfrom transform import transform_data\nfrom load import load_data\n\ndef run_etl():\n    data = extract_data()\n    if data is not None:\n        transformed_data = transform_data(data)\n        load_data(transformed_data)\n    else:\n        print('Failed to extract data.')\n",
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\etl.py"
    },
    {
      "contents": "from pyspark.sql import SparkSession\nimport json\nimport os\n\ndef extract_data():\n    spark = SparkSession.builder.appName('ETLProject').getOrCreate()\n    spark.sparkContext.setLogLevel('ERROR')\n    config_path = os.path.join(os.path.dirname(__file__), 'config.json')\n    with open(config_path) as config_file:\n        config = json.load(config_file)\n    data_path = config['data_path']\n    try:\n        df = spark.read.json(data_path)\n        return df\n    except Exception as e:\n        print(f'Error reading JSON file: {e}')\n        return None\n",
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\extract.py"
    },
    {
      "contents": "from pyspark.sql import DataFrame\nfrom db import get_db_connection\n\n\ndef load_data(df: DataFrame):\n    conn = get_db_connection()\n    try:\n        for row in df.collect():\n            cursor = conn.cursor()\n            cursor.execute('INSERT INTO customers (FIRST_NAME, LAST_NAME, EMAIL) VALUES (%s, %s, %s)', (row['FIRST_NAME'], row['LAST_NAME'], row['CUST_EMAIL']))\n            conn.commit()\n            cursor.close()\n    except Exception as e:\n        print(f'Error writing to the database: {e}')\n        conn.rollback()\n    finally:\n        conn.close()\n",
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\load.py"
    },
    {
      "contents": "from etl import run_etl\n\nif __name__ == '__main__':\n    run_etl()\n",
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\main.py"
    },
    {
      "contents": "pyspark\nmysql-connector-python\nclick\npython-dotenv\n",
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\requirements.txt"
    },
    {
      "contents": "CREATE DATABASE IF NOT EXISTS etl_project;\nUSE etl_project;\n\nCREATE TABLE IF NOT EXISTS customers (\n    FIRST_NAME VARCHAR(255),\n    LAST_NAME VARCHAR(255),\n    EMAIL VARCHAR(255),\n    PRIMARY KEY (EMAIL)\n);\n",
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\setup.sql"
    },
    {
      "contents": "def transform_data(df):\n    return df\n",
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\transform.py"
    },
    {
      "path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\__pycache__",
      "subpaths": []
    }
  ]
}
```

**STDOUT:**
```
SUCCESS: Specified value was saved.

SUCCESS: Specified value was saved.
Database does not exist. Attempting to create it...
Error writing to the database: Since Spark 2.3, the queries from raw JSON/CSV files are disallowed when the
referenced columns only include the internal corrupt record column
(named _corrupt_record by default). For example:
spark.read.schema(schema).csv(file).filter($"_corrupt_record".isNotNull).count()
and spark.read.schema(schema).csv(file).select("_corrupt_record").show().
Instead, you can cache or save the parsed results and then send the same query.
For example, val df = spark.read.schema(schema).csv(file).cache() and then
df.filter($"_corrupt_record".isNotNull).count().

SUCCESS: Specified value was saved.
SUCCESS: The process with PID 28432 (child process of PID 24544) has been terminated.
SUCCESS: The process with PID 24544 (child process of PID 21048) has been terminated.
SUCCESS: The process with PID 21048 (child process of PID 25024) has been terminated.
```

**STDERR:**
```
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
25/06/23 15:23:43 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable

[Stage 0:>                                                          (0 + 1) / 1]

                                                                                
Traceback (most recent call last):
  File "C:\Users\kenneth.copas\OneDrive - PeopleShores PBC\Desktop\Projects\OpenAI\ETLProject\load.py", line 8, in load_data
    for row in df.collect():
               ^^^^^^^^^^^^
  File "C:\Users\kenneth.copas\AppData\Local\Programs\Python\Python312\Lib\site-packages\pyspark\sql\dataframe.py", line 1263, in collect
    sock_info = self._jdf.collectToPython()
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\kenneth.copas\AppData\Local\Programs\Python\Python312\Lib\site-packages\py4j\java_gateway.py", line 1322, in __call__
    return_value = get_return_value(
                   ^^^^^^^^^^^^^^^^^
  File "C:\Users\kenneth.copas\AppData\Local\Programs\Python\Python312\Lib\site-packages\pyspark\errors\exceptions\captured.py", line 185, in deco
    raise converted from None
pyspark.errors.exceptions.captured.AnalysisException: Since Spark 2.3, the queries from raw JSON/CSV files are disallowed when the
referenced columns only include the internal corrupt record column
(named _corrupt_record by default). For example:
spark.read.schema(schema).csv(file).filter($"_corrupt_record".isNotNull).count()
and spark.read.schema(schema).csv(file).select("_corrupt_record").show().
Instead, you can cache or save the parsed results and then send the same query.
For example, val df = spark.read.schema(schema).csv(file).cache() and then
df.filter($"_corrupt_record".isNotNull).count().

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\kenneth.copas\OneDrive - PeopleShores PBC\Desktop\Projects\OpenAI\ETLProject\load.py", line 15, in load_data
    conn.rollback()
    ^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'rollback'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\main.py", line 4, in <module>
    run_etl()
  File "C:\Users\kenneth.copas\OneDrive - PeopleShores PBC\Desktop\Projects\OpenAI\ETLProject\etl.py", line 9, in run_etl
    load_data(transformed_data)
  File "C:\Users\kenneth.copas\OneDrive - PeopleShores PBC\Desktop\Projects\OpenAI\ETLProject\load.py", line 17, in load_data
    conn.close()
    ^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'close'
```