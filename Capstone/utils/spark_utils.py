import findspark
findspark.init()
from pyspark.sql import SparkSession, DataFrame
import os

class EasySpark:

    """
    
    The EasySpark class acts as a much simpler connector to a SparkSession. This class contains the basic features required to perform ETL processes
    on the data in this application.
    
    """

    def __init__(self, *, app_name: str, log: str, pyspark_python: str, mysql_jar: str) -> None:

        # Ensure that the environment variable is set to Python 3.10.0
        os.environ["PYSPARK_PYTHON"] = pyspark_python

        # Create a Spark session
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.jars", mysql_jar) \
            .getOrCreate()

        # Save log level and set into effect
        self.log_level = log.upper()
        self.spark.sparkContext.setLogLevel(log.upper())

        # Initialize MySQL variables as None
        self.mysql_url = None
        self.mysql_props = None

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

    # This method takes any number of filepaths, converts each to a dataframe, and returns each dataframe
    def load_files(self, *filepaths: str) -> list[DataFrame]:
        
        dataframes = []

        for fp in filepaths:
            df = self.json_to_df(fp)
            dataframes.append(df)

        print(f"{len(dataframes)} files loaded.")

        return dataframes
    
    # Set the MySQL jdbc url and properties
    def mysql_config(self, mysql_url: str, mysql_props: dict) -> None:
        self.mysql_url = mysql_url
        self.mysql_props = mysql_props
        print("MySQL Configurations set.")

    # Write a DataFrame to a MySQL table
    def mysql_write(self, table: str, df: DataFrame, mode: str) -> None:

        # First check if the configurations are set
        if not (self.mysql_url and self.mysql_props):
            raise Exception("Attempting to write to MySQL without configurations.")
        
        # Then write the DataFrame to the specified table with the passed mode        
        df.write \
            .format("jdbc") \
            .option("url", self.mysql_url) \
            .option("driver", self.mysql_props["driver"]) \
            .option("dbtable", table) \
            .option("user", self.mysql_props["user"]) \
            .option("password", self.mysql_props["password"]) \
            .mode(mode) \
            .save()
        
        print("MySQL table written.")

    # Read MySQL table and return the data in a DataFrame
    def mysql_read(self, table: str) -> DataFrame:

        # First check if the configurations are set
        if not (self.mysql_url and self.mysql_props):
            raise Exception("Attempting to read from MySQL without configurations.")

        # Then read and return the specified MySQL table data
        df = self.spark.read \
            .format("jdbc") \
            .option("url", self.mysql_url) \
            .option("driver", self.mysql_props["driver"]) \
            .option("dbtable", table) \
            .option("user", self.mysql_props["user"]) \
            .option("password", self.mysql_props["password"]) \
            .load()
        
        print("MySQL Table read.")
        
        return df
    
    def stop(self) -> None:
        self.spark.stop()