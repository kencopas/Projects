import json
import glob

import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lower, concat, lit, substring, lpad

from utils.spark_utils import EasySpark
from utils.sql_utils import SafeSQL, unpacked
from cli_manager import CLIManager
from constants import LOAN_API_URL, SUPPORTED_EXTENSIONS


class Application:

    """

    app

    """

    def __init__(self, app_name: str, *, log: str) -> None:

        # Load the configuration file
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
        query_output = self.ssql.run("sql_scripts/init.sql")
        self.ssql.commit()

        # If the last sql query did not return any rows, run the pipeline
        if not query_output[-1]:
            self.pipeline()

        # Initialize and run the CLIManager
        self.run_cli()

    # Initialize and run the CLIManager
    def run_cli(self):
        self.cli = CLIManager(self)
        self.cli.run()

    def cli_query(self, path: tuple) -> None:

        """

        The CLI-query method takes the CLI path and tracks where the user
        navigated to in the menu, determining which flag to use to correspond
        to the correct sql query in the cli_script.sql file. Once the
        navigation has been tracked, the user's choices and inputs are
        extracted from the path and used to construct the parameters for the
        query. After the query is run, the output is saved and displayed in
        a DataFrame.

        """

        # Extract the component id and remaining selections
        component_id, selections = list(path.items())[0]

        # Route to the correct component
        match component_id:
            case 'view_transactions':

                cust_zip = selections['zip']
                mm, yyyy = selections['date'].split('-')

                params = (cust_zip, f'{yyyy}{mm}')

            case 'customers_nav':
                component_id, selections = list(selections.items())[0]

                # Route to the correct query within the customers component
                match component_id:
                    case "view_account":

                        SSN = selections['SSN']

                        params = (SSN,)

                    case "modify_account":

                        SSN = selections['SSN']
                        attr = selections['attribute']
                        new_val = selections['new_value']

                        params = (attr, new_val, SSN, SSN)

                    case 'generate_bill':

                        ccn = selections['CCN']
                        mm, yyyy = selections['date'].split('-')

                        params = (ccn, f"{yyyy}{mm}")

                    case 'transactions_timeframe':

                        SSN = selections['SSN']
                        start = selections['start_date'].split('-')
                        end = selections['end_date'].split('-')

                        # Format the start and end date as YYYYMMDD
                        fstart = f"{start[2]}{start[0]}{start[1]}"
                        fend = f"{end[2]}{end[0]}{end[1]}"

                        params = (SSN, fstart, fend)

                    case _:
                        print("Unknown: Application.cli_query.customers_nav")

            case _:
                print(f"Unknown: Application.cli_query: {component_id}")

        # Release limits on max columns and rows and display width
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)
        pd.set_option('display.width', 150)

        # Run the appropriate query and save the data
        data = self.ssql.parse_file(
            'sql_scripts/cli_script.sql',
            flag=component_id.upper(),
            params=params
        )

        # Commit the query to the database
        self.ssql.commit()

        # Unpack the data, removing empty iterables
        data = unpacked(data, remove_empty=True)

        # If the query came back empty, print a message and return
        if not data:
            values = [f"{attr}: {val}" for attr, val in selections.items()]
            print("\nNo records matching the following values:\n")
            print("\n".join(values))
            return

        # Construct a DataFrame from the data
        df = pd.DataFrame(data[1:], columns=data[0])

        # Sort the DataFrame by timestamp if the column exists
        if 'Date' in df.columns:
            df = df.sort_values(by='Date', ascending=False)

        # Print the dataframe
        print(df)

        # Total value if the value column exists
        if 'Value' in df.columns:
            total_value = round(df['Value'].sum(), 2)
            print(f"\nTotal: {total_value}")

    # Loads the config.json file into the config attribute
    def load_config(self) -> None:
        with open("macconfig.json") as f:
            self.config = json.load(f)

    # Read data from json into a dataframe
    def json_read(self, json_file: str) -> DataFrame:
        return self.espark.json_to_df(json_file)

    # Perform ETL on the json files and endpoint, saving output into MySQL
    def pipeline(self) -> None:

        """

        Functional Requirement 1.1

        Extracts, transforms, and loads data from json files and an api
        into Pyspark DataFrames.

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

        # Gather all data files of the supported file extensions
        data_files = [
            file
            for ext in SUPPORTED_EXTENSIONS
            for file in glob.glob(f"application_data/*{ext}")
        ]

        # Read each file into a DataFrame, save each in a dictionary
        df_map = self.espark.load_files(*data_files, rtype=dict)

        # Make a get request to the loan endpoint and save as DataFrame
        loan_df = self.espark.get(LOAN_API_URL)

        # Add the loan DataFrame to the df_map
        df_map.update({'cdw_sapp_loan_application': loan_df})

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

        # Write each DataFrame to the mysql table that matches the filename
        for name, df in df_map.items():
            self.espark.mysql_write(name, df)


if __name__ == "__main__":

    myapp = Application("Hello World!", log="OFF")
