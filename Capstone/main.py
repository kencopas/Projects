from pyspark.sql.functions import col, lower, concat, lit, substring, lpad, regexp_replace, concat_ws
from pyspark.sql import DataFrame
from utils.spark_utils import EasySpark
from utils.sql_utils import SafeSQL
from navigation import CLIManager
import json
import sys

class Application:

    """
    
    app
    
    """

    def __init__(self, app_name: str, *, log: str) -> None:

        # Verify that the python version is compatible and load the configuration file
        self.verify_version()
        self.load_config()

        # Initialize EasySpark connection
        self.espark = EasySpark(
            app_name=app_name,
            log=log,
            config=self.config
        )

        # Initialize SafeSQL connection
        self.ssql = SafeSQL(
            user=self.config["user"],
            password=self.config["password"],
            host=self.config["host"]
        )

        # Initialize database tables and commit
        self.ssql.run("sql_scripts/init.sql")
        self.ssql.commit()
        self.ssql.close()

        # Extract, transform, and load the customer data into the database
        self.pipeline()

        # Initialize and run the CLIManager
        self.run_cli()

    def run_cli(self):
        self.cli = CLIManager(self.ssql)
        self.cli.run()

    # Print a warning if the python version being run is not between versions 3.8 and 3.11
    def verify_version(self) -> None:
        if not 8 <= sys.version_info[1] <= 11:
            ans = input(
                f"\nIncompatible Python version: {sys.version[:6]}" +
                "\nReccomended Versions: 3.8-3.11" +
                "\nWould you like to continue? Y | N\n"
            )
            if ans.lower().strip() == "n":
                exit(0)

    # Loads the config.json file into the config attribute
    def load_config(self) -> None:
        with open("config.json") as f:
            self.config = json.load(f)

    # Read data from json into a dataframe
    def json_read(self, json_file: str) -> DataFrame:
        return self.espark.json_to_df(json_file)

    def pipeline(self) -> None:

        """
        
        Functional Requirement 1.1
        Loads, transforms, and saves data from json format into Pyspark DataFrames

        Customer DataFrame - 

            MIDDLE_NAME -> lowercase
            FULL_STREET_ADDRESS -> <STREET_NAME>, <APT_NO>
            CUST_PHONE -> (XXX)XXX-XXXX
            APT_NO -> drop
            STREET_NAME -> drop

        Branch DataFrame -

            BRANCH_ZIP -> default=999999
            BRANCH_PHONE -> (XXX)XXX-XXXX

        Credit Card DataFrame - 

            CREDIT_CARD_NO -> rename CUST_CC_NO
            TIMEID -> YYYYMMDD
            YEAR -> drop
            MONTH -> drop
            DAY -> drop
        
        """

        # Convert each file into a dataframe and save the output as a dictioanry
        df_map = self.espark.load_files(
            r"data/cdw_sapp_branch.json",
            r"data/cdw_sapp_credit_card.json",
            r"data/cdw_sapp_customer.json",
            rtype=dict
        )

        # Transform Customer DataFrame
        df_map['cdw_sapp_customer'] = df_map['cdw_sapp_customer'] \
            .withColumn("MIDDLE_NAME", lower("MIDDLE_NAME")) \
            .withColumn("FULL_STREET_ADDRESS", concat(
                col("STREET_NAME"), lit(", "), col("APT_NO").cast("string")
            )) \
            .withColumn("CUST_PHONE", concat(
                lit("(XXX)"), substring(col("CUST_PHONE").cast("string"), 1, 3),
                lit("-"), substring(col("CUST_PHONE").cast("string"), 4, 4)
            )) \
            .drop("APT_NO").drop("STREET_NAME")
        
        # Transform Branch DataFrame
        df_map['cdw_sapp_branch'] = df_map['cdw_sapp_branch'] \
            .fillna({"BRANCH_ZIP": "999999"}) \
            .withColumn("BRANCH_PHONE", concat(
                lit("("), substring(col("BRANCH_PHONE").cast("string"), 1, 3), lit(")"),
                substring(col("BRANCH_PHONE").cast("string"), 4, 3), lit("-"),
                substring(col("BRANCH_PHONE").cast("string"), 7, 4)
            ))

        # Transform Credit Card DataFrame
        df_map['cdw_sapp_credit_card'] = df_map['cdw_sapp_credit_card'] \
            .withColumnRenamed("CREDIT_CARD_NO", "CUST_CC_NO") \
            .withColumn("TIMEID", concat(
                col("YEAR").cast("string"),
                lpad(col("MONTH").cast("string"), 2, "0"),
                lpad(col("DAY").cast("string"), 2, "0")
            )) \
            .drop("YEAR").drop("MONTH").drop("DAY")
        
        # This works because the filenames directly correspond to the MySQL table names
        for name, df in df_map.items():
            self.espark.mysql_write(name, df)

        # Save the transformed data in memory
        self.df_map = df_map

if __name__ == "__main__":

    myapp = Application("Hello World!", log="OFF")