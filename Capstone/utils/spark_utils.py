import os
import sys
import json
import subprocess
from collections.abc import Iterable

import requests
from pyspark.sql import SparkSession, DataFrame


# Exception for missing MySQL Configurations
class MissingMySQLConfig(Exception):
    def __init__(self, action: str):
        message = f"Exception occured while {action}"
        super().__init__(message)


class EasySpark:

    """

    This is my detailed description.

    The EasySpark class acts as a much simpler connector to a SparkSession.
    This class contains the basic features required to perform ETL processes
    on the data in this application.

    """

    def __init__(self, *, app_name: str, log: str, config: dict) -> None:

        # Ensure that the environment variable is set to Python 3.10.0
        os.environ["PYSPARK_PYTHON"] = config['pyspark_python']
        self.verify_version(config['pyspark_python'])

        # Create the SparkSession builder
        builder = SparkSession.builder.appName(app_name)

        # Configure the builder with mysql if provided
        if config.get('mysql_jar'):
            builder.config("spark.jars", config['mysql_jar'])

        # Create the SparkSession
        self.spark = builder.getOrCreate()

        # Set the log level
        self.spark.sparkContext.setLogLevel(log.upper())

        # Save the configurations
        self.config = config

    # Print a warning if the python version being run is not 3.8-3.11
    def verify_version(self, pyspark_python: str) -> None:

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

    # Retrieve JSON from an api endpoint and return it as a DataFrame
    def api_to_df(self, api: str) -> DataFrame:

        # Ping the api and save the json response
        response = requests.get(api)
        data = response.json()

        # Convert JSON data to RDD and create DataFrame from RDD
        rdd = self.spark.sparkContext.parallelize([json.dumps(data)])
        df = self.spark.read.json(rdd)

        return df

    # Safely read data from a json file or python object into a dataframe
    def file_to_df(self, fp: str) -> DataFrame:

        ext = os.path.splitext(fp)[1][1:]
        converter = getattr(self.spark.read, ext)

        options = {"multiLine": True}
        if ext == 'csv':
            options.update({"header": True})
        try:
            data = converter(fp, **options)
            return data
        except Exception as err:
            print(f"Error occured while reading file: {fp}")
            print(f"{type(err).__name__}: {err}")

    def load_files(self, *filepaths: str, rtype: type) -> Iterable[DataFrame]:

        """

        This method takes any number of filepaths, converts each to a
        dataframe, and returns each dataframe in the form of a specified
        Iterable object.

        """

        dataframes, filenames = [], []

        # For each file, read into a dataframe and save the filename
        for fp in filepaths:
            df = self.file_to_df(fp)
            dataframes.append(df)
            filenames.append(os.path.basename(fp).split('.')[0])

        print(f"{len(dataframes)} files loaded.")

        # Return a dictionary in the format: {filename: df}
        if rtype == dict:
            output = dict(zip(filenames, dataframes))
        # Return the df list as any other Iterable
        elif rtype in (list, tuple, set):
            output = rtype(dataframes)
        else:
            print(f"EasySpark.load_files() | Incompatible data type: {rtype}")
            return

        return output

    # Write a DataFrame to a MySQL table
    def mysql_write(
        self,
        table: str,
        df: DataFrame,
        mode: str = "append"
    ) -> None:

        try:
            # First check if the configurations are set
            if not self.config:
                raise MissingMySQLConfig("writing to table.")

            # Then write the DataFrame to the specified table
            df.write \
                .format("jdbc") \
                .option("url", self.config['jdbc_url']) \
                .option("driver", self.config["jdbc_driver"]) \
                .option("dbtable", table) \
                .option("user", self.config["user"]) \
                .option("password", self.config["password"]) \
                .mode(mode) \
                .save()

            print(f"pyspark.sql | Saved data to table {table}.")

        except Exception as err:
            print(f"pyspark.sql | Exception occurred writing to table {table}")
            print(f"{type(err).__name__}: {err}")

    # Read MySQL table and return the data in a DataFrame
    def mysql_read(self, table: str) -> DataFrame:

        try:
            # First check if the configurations are set
            if not self.config:
                raise MissingMySQLConfig("reading table.")

            # Then read and return the specified MySQL table data
            df = self.spark.read \
                .format("jdbc") \
                .option("url", self.config['jdbc_url']) \
                .option("driver", self.config["jdbc_driver"]) \
                .option("dbtable", table) \
                .option("user", self.config["user"]) \
                .option("password", self.config["password"]) \
                .load()

            print("MySQL Table read.")

            return df

        except Exception as err:
            print(f"Exception occurred while reading table: {table}")
            print(f"{type(err).__name__}: {err}")

    def stop(self) -> None:
        self.spark.stop()


if __name__ == "__main__":

    # Load the config file
    with open('macconfig.json', 'r') as f:
        config = json.load(f)

    # Create an EasySpark Session
    espark = EasySpark(
        app_name="SBA345",
        log="FATAL",
        config=config
    )
