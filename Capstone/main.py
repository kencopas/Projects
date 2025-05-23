from pyspark.sql.functions import col, lower, concat, lit, substring, lpad, regexp_replace, concat_ws
from pyspark.sql import DataFrame
from utils.spark_utils import EasySpark
from utils.sql_utils import SafeSQL
from cli_manager import CLIManager
import json
import pandas as pd

class Application:

    """
    
    app
    
    """

    COLUMNS = {
        'credit_card': ['Transaction ID', 'Value', 'Type', 'Branch Code', 'Customer SSN', 'Time ID', 'Customer CCN'],
        'customer': ['Customer SSN', 'First', 'Middle', 'Last', 'CCN', 'Street Address', 'City', 'State', 'Country', 'Zip', 'Phone', 'Email', 'Last Updated'],
        'branch': ['Branch Code', 'Name', 'Street', 'City', 'State', 'Zip', 'Phone', 'Last Updated']
    }


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

        # If the last sql query did not return any rows, extract, transform, and load the customer data into the database
        if not query_output[-1]:
            self.pipeline()

        # Initialize and run the CLIManager
        self.run_cli()

    # Initialize and run the CLIManager
    def run_cli(self):
        self.cli = CLIManager(self)
        self.cli.run()
    
    def cli_query(self, path: tuple):

        print(path.items())
        component_id, selections = list(path.items())[0]

        match component_id:
            case 'transactions_div':
                cust_zip = selections['tzip']
                mm, yyyy = selections['tdate'].split('-')

                data = self.ssql.run(f"""
                    -- Join the credit card and customer table, query only the credit card data
                    SELECT
                        cc.*
                    FROM
                        cdw_sapp_credit_card cc
                    LEFT JOIN
                        cdw_sapp_customer cust
                    ON
                        cc.cust_ssn = cust.ssn
                    WHERE
                        cust.cust_zip = {cust_zip}
                        AND cc.timeid LIKE '{yyyy}{mm}%';
                """)

                df = pd.DataFrame(data, columns=self.COLUMNS['credit_card'])
                total_bill = round(df['Value'].sum(), 2)

                print(df)
                print(f"\nTotal: {total_bill}")

            case 'customers_nav':

                nav, selections = list(selections.items())[0]
                print(nav, selections)

                match nav:
                    case "view_account":

                        SSN = selections['SSN']

                        data = self.ssql.run(f"""
                            -- Query the customer data
                            SELECT
                                *
                            FROM
                                cdw_sapp_customer
                            WHERE
                                ssn = {SSN};
                        """)

                        df = pd.DataFrame(data, columns=self.COLUMNS['customer'])

                        print(df)
                    
                    case "modify_account_div":

                        SSN = selections['SSN']
                        attr = selections['modify_attribute']
                        new_val = selections['modify_value']

                        data = self.ssql.run(f"""
                            -- Update the value
                            UPDATE
                                cdw_sapp_customer
                            SET
                                {attr} = '{new_val}'
                            WHERE
                                ssn = {SSN};

                            -- Query the updated row
                            SELECT
                                *
                            FROM
                                cdw_sapp_customer
                            WHERE
                                ssn = {SSN};
                        """)

                        self.ssql.commit()

                        df = pd.DataFrame(data[1], columns=self.COLUMNS['customer'])

                        print(f"Updated Data:\n\n{df}")

                    case 'generate_bill_div':

                        ccn = selections['CCN']
                        mm, yyyy = selections['gbdate'].split('-')

                        data = self.ssql.run(f"""
                            SELECT
                                transaction_value,
                                transaction_type,
                                timeid
                            FROM
                                cdw_sapp_credit_card
                            WHERE
                                cust_cc_no = {ccn}
                                AND timeid LIKE '{yyyy}{mm}%';
                        """)

                        df = pd.DataFrame(data, columns=['Value', 'Type', 'Timestamp'])
                        total_bill = round(df['Value'].sum(), 2)

                        print(df)
                        print(f"\nTotal: {total_bill}")

                    case 'transactions_timeframe_div':

                        SSN = selections['SSN']
                        start = selections['tstartdate'].split('-')
                        end = selections['tenddate'].split('-')

                        fstart = f"{start[2]}{start[0]}{start[1]}"
                        fend = f"{end[2]}{end[0]}{end[1]}"

                        data = self.ssql.run(f"""
                            select
                                cc.transaction_value,
                                cc.transaction_type,
                                cc.timeid,
                                cc.cust_cc_no
                            from
                                cdw_sapp_credit_card cc
                            left join
                                cdw_sapp_customer cust
                            on
                                cust.ssn = cc.cust_ssn
                            where
                                cust.ssn = {SSN}
                                AND cc.timeid >= {fstart}
                                AND cc.timeid <= {fend};
                        """)

                        df = pd.DataFrame(data, columns=["Value", "Type", "Timestamp", "CCN"])
                        total_bill = round(df['Value'].sum(), 2)

                        print(df)
                        print(f"\nTotal: {total_bill}")

                    case _:
                        print("Unknown Application.cli_query.customers_nav")

            case _:
                print(f"unknown: Application.cli_query: {component_id}")

    # Loads the config.json file into the config attribute
    def load_config(self) -> None:
        with open("config.json") as f:
            self.config = json.load(f)

    # Read data from json into a dataframe
    def json_read(self, json_file: str) -> DataFrame:
        return self.espark.json_to_df(json_file)

    # Perform ETL on the json files and endpoint, saving output into MySQL using PySpark
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

        # Retrieve the api response from the loan dataset endpoint as a DataFrame
        loan_df = self.espark.api_to_df(r"https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json")

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
        
        # This works because the filenames directly correspond to the MySQL table names
        for name, df in df_map.items():
            self.espark.mysql_write(name, df)

if __name__ == "__main__":

    myapp = Application("Hello World!", log="OFF")