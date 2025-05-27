import os
import json
import glob
from collections.abc import Iterable

import requests
from pyspark.sql import SparkSession, DataFrame
from utils.sql import SafeSQL, unpacked

from constants import LOAN_API_URL, SUPPORTED_EXTENSIONS
from components.transformers import transformers_map


# Exception for missing MySQL Configurations
class MissingMySQLConfig(Exception):
    def __init__(self, action: str):
        message = f"Exception occured while {action}"
        super().__init__(message)


class DataClient:

    """
    This is my detailed description.

    The DataClient class acts as a much simpler connector to a SparkSession.
    This class contains the basic features required to perform ETL processes
    on the data in this application.
    """

    def __init__(
        self,
        spark: SparkSession,
        sql: SafeSQL,
        config: dict
    ) -> None:

        # Save the SparkSession as an attribute
        self.spark = spark
        self.sql = sql
        self.config = config

    # Perform ETL on the json files and endpoint, saving output into MySQL
    def pipeline(self) -> None:

        """
        Functional Requirement 1.1

        Extracts, transforms, and loads data from json files and an api
        into Pyspark DataFrames.
        """

        # Initialize database tables and commit
        query_output = self.sql.run("sql/init.sql")
        self.sql.commit()

        # If the last query returned any rows, terminate the pipeline
        if query_output[-1]:
            return

        # Gather all data files of the supported file extensions
        data_files = [
            file
            for ext in SUPPORTED_EXTENSIONS
            for file in glob.glob(f"application_data/*{ext}")
        ]

        # Read each file into a DataFrame, save each in a dictionary
        df_map = self.load_files(*data_files)

        # For each DataFrame, retrieve and call the corresponding transformer
        for filename in df_map.keys():
            transformer = transformers_map[filename]
            df_map[filename] = transformer(df_map[filename])

        # Make a get request to the loan endpoint and save as DataFrame
        loan_df = self.get(LOAN_API_URL)

        # Add the loan DataFrame to the df_map
        df_map.update({'cdw_sapp_loan_application': loan_df})

        # Write each DataFrame to the mysql table that matches the filename
        for name, df in df_map.items():
            self.mysql_write(name, df)

    # Retrieve JSON from an api endpoint and return it as a DataFrame
    def get(self, api: str) -> DataFrame:

        # Ping the api and save the json response
        response = requests.get(api)
        data = response.json()

        # Convert JSON data to RDD and create DataFrame from RDD
        rdd = self.spark.sparkContext.parallelize([json.dumps(data)])
        df = self.spark.read.json(rdd)

        return df

    def query(self, flag: str, params: tuple) -> None:

        """
        The DataClient.query method parses the cli_script.sql file using
        the flag passed and inserts the parameters passed into the query.
        After running and committing, the query results are unpacked and
        returned.
        """

        # Run the appropriate query and save the data
        data = self.sql.parse_file(
            'sql/cli_script.sql',
            flag=flag,
            params=params
        )

        # Commit the query to the database
        self.sql.commit()

        # Unpack the data, removing empty iterables
        data = unpacked(data, remove_empty=True)

        return data

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

    def load_files(self, *filepaths: str) -> Iterable[DataFrame]:

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
        output = dict(zip(filenames, dataframes))

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
    dc = DataClient(
        app_name="SBA345",
        log="FATAL",
        config=config
    )
