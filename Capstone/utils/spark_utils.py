import findspark
findspark.init()
from pyspark.sql import SparkSession, DataFrame
import os
from collections.abc import Iterable
import json

class EasySpark:

    """
    
    The EasySpark class acts as a much simpler connector to a SparkSession. This class contains the basic features required to perform ETL processes
    on the data in this application.
    
    """

    def __init__(self, *, app_name: str, log: str, config: dict) -> None:

        # Ensure that the environment variable is set to Python 3.10.0
        os.environ["PYSPARK_PYTHON"] = config['pyspark_python']

        print(config['mysql_jar'])

        # Create a Spark session
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.jars", config['mysql_jar']) \
            .getOrCreate()

        # Save log level and set into effect
        self.log_level = log.upper()
        self.spark.sparkContext.setLogLevel(log.upper())

        # Save the configurations
        self.config = config

    # Safely read data from a json file or python object into a dataframe and return it
    def json_to_df(self, json_data: str | list | dict) -> DataFrame:
        try:
            # Read data as filepath
            if type(json_data) == str:
                data = self.spark.read.option("multiline", "true").json(json_data)
            # Read data as python object, parellelizing before converting to a DataFrame
            elif type(json_data) in (list, dict):
                parallel = self.spark.sparkContext.parallelize(json_data)
                data = self.spark.createDataFrame(parallel)
            else:
                raise Exception(f"Unable to convert datatype {type(json_data)} to dataframe with json_to_df function.")
            
            return data
        
        except Exception as err:
            print(f"Error occured while reading file: {json_data}")
            print(f"{type(err).__name__}: {err}")

    # This method takes any number of filepaths, converts each to a dataframe, and returns each dataframe in the form of a specified Iterable object
    def load_files(self, *filepaths: str, rtype: type) -> Iterable[DataFrame]:
        
        dataframes, filenames = [], []

        # For each filepath, convert the file contents to a dataframe and save the filename
        for fp in filepaths:
            df = self.json_to_df(fp)
            dataframes.append(df)
            filenames.append(os.path.basename(fp).split('.')[0])

        print(f"{len(dataframes)} files loaded.")

        # If the specified return type is a dict, construct a dict using the filenames as keys
        if rtype == dict:
            output = dict(zip(filenames, dataframes))
        # If the return type is any other iterable, cast to that type
        elif rtype in (list, tuple, set):
            output = rtype(dataframes)
        else:
            print(f"EasySpark.load_files() | Incompatible data type: {rtype}")
            return

        return output

    # Write a DataFrame to a MySQL table
    def mysql_write(self, table: str, df: DataFrame, mode: str = "append") -> None:

        try:
            # First check if the configurations are set
            if not self.config:
                raise Exception("Attempting to write to MySQL without configurations.")
            
            # Then write the DataFrame to the specified table with the passed mode  
            print(self.config)      
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
            print(f"pyspark.sql | Exception occurred while writing to table: {table}")
            print(f"{type(err).__name__}: {err}")

    # Read MySQL table and return the data in a DataFrame
    def mysql_read(self, table: str) -> DataFrame:

        try:
            # First check if the configurations are set
            if not self.config:
                raise Exception("Attempting to read from MySQL without configurations.")

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
    pass