from pyspark.sql.functions import col, lower, concat, lit, substring, lpad
from pyspark.sql import DataFrame
from utils.spark_utils import EasySpark
from utils.sql_utils import SafeSQL
import json

class Application:

    def __init__(self, app_name: str, *, log: str) -> None:

        # Load the config file
        self.load_config()

        # Initialize and configure an EasySpark instance
        self.sparkup(app_name, log)
        
        # Initialize database tables
        self.init_tables()

        # Load the customer data
        self.load_cust_data()

    # Create an EasySpark instance and set the sql configurations
    def sparkup(self, app_name: str, log: str) -> None:

        # Create an EasySpark Session, load and transform the data as dataframes
        self.espark = EasySpark(
            app_name=app_name,
            log=log,
            pyspark_python=self.config["pyspark_python"],
            mysql_jar=self.config["mysql_jar"]
        )
        
        # Configure the MySQL connection properties for the current EasySpark Session
        self.espark.mysql_config(
            self.config["jdbc_url"],
            {
                "user" : self.config["user"],
                "password": self.config["password"],
                "driver": self.config["jdbc_driver"]
            }
        )

    # Takes a properties dictionary and uses the values to establish a SafeSQL connection and configure the EasySpark sql properties
    def load_config(self) -> None:
        # Load the config file
        with open("config.json") as f:
            self.config = json.load(f)
        
    # Write data to a MySQL table from a PySpark DataFrame
    def sql_write(self, table_name: str, df: DataFrame) -> None:
        try:
            self.espark.mysql_write(table_name, df, "append")
        except Exception as err:
            print(f"Exception Occurred while writing to table: {table_name}")
            print(f"{type(err).__name__}: {err}")

    # Read data from a MySQL table into a PySpark DataFrame
    def sql_read(self, table_name: str) -> DataFrame:
        try:
            return self.espark.mysql_read(table_name)
        except Exception as err:
            print(f"Exception Occurred while reading table: {table_name}")
            print(f"{type(err).__name__}: {err}")

    # Read data from json into a dataframe
    def json_read(self, json_file: str) -> DataFrame:
        return self.espark.json_to_df(json_file)

    # Loads the customer data from json format into PySpark DataFrames, formats the data, and returns each DataFrame
    def load_cust_data(self) -> None:

        # Convert each file into a dataframe and show each dataframe
        branch, credit, customer = self.espark.load_files(
            r"data/cdw_sapp_branch.json",
            r"data/cdw_sapp_credit.json",
            r"data/cdw_sapp_customer.json"
        )

        # Transform Customer DataFrame

        # MIDDLE_NAME -> lowercase
        # FULL_STREET_ADDRESS -> <STREET_NAME>, <APT_NO>
        # CUST_PHONE -> (XXX)XXX-XXXX
        # APT_NO -> drop
        # STREET_NAME -> drop

        customer = customer.withColumn("MIDDLE_NAME", lower("MIDDLE_NAME")) \
            .withColumn("FULL_STREET_ADDRESS", concat(
                col("STREET_NAME"),
                lit(", "),
                col("APT_NO").cast("string")
            )) \
            .withColumn("CUST_PHONE", concat(
                lit("(XXX)"),
                substring(col("CUST_PHONE").cast("string"), 1, 3),
                lit("-"),
                substring(col("CUST_PHONE").cast("string"), 4, 4)
            )) \
            .drop("APT_NO") \
            .drop("STREET_NAME") 

        # Transform Branch DataFrame

        # BRANCH_ZIP -> default=999999
        # BRANCH_PHONE -> (XXX)XXX-XXXX

        branch = branch.fillna({"BRANCH_ZIP": "999999"}) \
            .withColumn("BRANCH_PHONE", concat(
                lit("("),
                substring(col("BRANCH_PHONE").cast("string"), 1, 3),
                lit(")"), substring(col("BRANCH_PHONE").cast("string"), 4, 3),
                lit("-"), substring(col("BRANCH_PHONE").cast("string"), 7, 4)
            ))

        # Transform Card DataFrame

        # CREDIT_CARD_NO -> rename CUST_CC_NO
        # TIMEID -> YYYYMMDD
        # YEAR -> drop
        # MONTH -> drop
        # DAY -> drop

        credit = credit.withColumnRenamed("CREDIT_CARD_NO", "CUST_CC_NO") \
            .withColumn("TIMEID", concat(
                col("YEAR").cast("string"),
                lpad(col("MONTH").cast("string"), 2, "0"),
                lpad(col("DAY").cast("string"), 2, "0")
            )) \
            .drop("YEAR") \
            .drop("MONTH") \
            .drop("DAY")
        
        # Save the transformed data
        self.data = {
            "customer": customer,
            "branch": branch,
            "credit": credit
        }

    # Intializes each table if they do not already exist
    def init_tables(self) -> None:

        # Establish a SafeSQL connection
        ssql = SafeSQL(user=self.config["user"],
                            password=self.config["password"],
                            host=self.config["host"],
                            database=self.config["database"])

        ssql.run_file("init.sql")

        # Commit the changes and close connection
        ssql.commit()
        ssql.close()

if __name__ == "__main__":

    app = Application("Credit Card Application", log="FATAL")
    # app.run()