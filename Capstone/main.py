import json
import os
import sys
import subprocess

from pyspark.sql import SparkSession

from utils.sql import SafeSQL
from app.menu import CLIManager
from app.data_client import DataClient


class Application:
    """
    Manages the ETL process for a bank dataset using PySpark, MySQL,
    and a CLI interface.

    This class initializes a SparkSession, sets up secure SQL access, runs an
    ETL pipeline, and launches a command-line interface for user interaction.
    It also verifies Python version compatibility between the application and
    PySpark environment.

    Methods:
        load_config():
            Loads configuration from a JSON file into the application.

        verify_version(pyspark_python: str):
            Verifies the application and PySpark Python versions are compatible
    """

    def __init__(self, app_name: str, *, log: str) -> None:

        # Load the configuration file and verify the python version
        config = self.load_config()
        self.verify_version()

        # Create the SparkSession
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.jars", config['mysql_jar']) \
            .config("spark.driver.bindAddress", "127.0.0.1") \
            .config("spark.driver.host", "127.0.0.1") \
            .config("spark.driver.port", "4041") \
            .config("spark.hadoop.io.native.lib.available", "false") \
            .getOrCreate()

        # Set the log level
        self.spark.sparkContext.setLogLevel(log.upper())

        # Initialize SafeSQL connection
        self.sql = SafeSQL(
            user=config["user"],
            password=config["password"],
            host=config["host"]
        )

        # Initialize the DataClient and run the pipeline
        self.dc = DataClient(self.spark, self.sql, config)
        self.dc.pipeline()

        # Initialize and run the CLIManager
        self.cli = CLIManager(self.dc)
        self.cli.run()

    # Print a warning if the python version being run is not 3.8-3.11
    def verify_version(self) -> None:

        # Set the environment variable to the pyspark python version specified
        pyspark_python = self.config['pyspark_python']
        os.environ['PYSPARK_PYTHON'] = pyspark_python

        # Retrieve the version running the script
        full_app_version = sys.version[:6]

        # Retrieve the version running the SparkSession
        completed_process = subprocess.run(
            [pyspark_python, '--version'],
            stdout=subprocess.PIPE,
            text=True
        )
        full_pyspark_version = completed_process.stdout[-7:]

        # Extract the version number from the full versions
        app_ver = int(full_app_version[2:4])
        pyspark_ver = int(full_pyspark_version[2:4])

        # Check if either version is not fully compatible
        if not (8 <= app_ver <= 11 and 8 <= pyspark_ver <= 11):
            ans = input(
                "\nOne or more incompatible Python versions:" +
                f"\nApplication Version: {full_app_version}" +
                f"\nPySpark Version: {full_pyspark_version}" +
                "\nReccomended Versions: 3.8-3.11" +
                "\nWould you like to continue? Y | N\n"
            )
            if ans.lower().strip() == "n":
                exit(0)

    # Loads the config.json file into the config attribute
    def load_config(self) -> dict:
        with open("config/config.json") as f:
            self.config = json.load(f)
        return self.config


if __name__ == "__main__":

    myapp = Application("Capstone ETL Manager", log="OFF")
