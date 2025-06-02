import os
from datetime import datetime

import pandas as pd

from utils.sql import SafeSQL
from utils.cli import MultipleChoice, UserInput, MenuDivider
from app.data_client import DataClient
from config.constants import VALIDATIONS


class CLIManager:
    """
    Manages the CLI built from the cli utility
    """

    def __init__(self, dc: DataClient) -> None:

        # Save the DataClient
        self.dc = dc

        # Build the menu
        self.build_menu()

    # View transactions by zipcode and month
    def view_transactions(self, path: tuple):

        cust_zip = path[1]['zip']
        mm, yyyy = path[1]['date'].split('-')

        self.cli_params = (path[0], (cust_zip, f'{yyyy}{mm}'))

    # View account details
    def view_account(self, path: tuple):

        ssn = path[1]['SSN']

        self.cli_params = (path[0], (ssn,))

    # Modify account details by SSN
    def modify_account(self, path: tuple):

        SSN = path[1]['SSN']
        attr, new_val = next(iter(path[1]['modify_attribute'].items()))

        self.cli_params = (path[0], (attr, new_val, SSN, SSN))

    # Generate a monthly bill by CCN
    def generate_bill(self, path: tuple):

        ccn = path[1]['CCN']
        mm, yyyy = path[1]['date'].split('-')

        self.cli_params = (path[0], (ccn, f"{yyyy}{mm}"))

    # View transactions between two dates by SSN
    def transactions_timeframe(self, path: tuple):

        SSN = path[1]['SSN']
        start = path[1]['start_date'].split('-')
        end = path[1]['end_date'].split('-')

        # Start and end dates are formatted as YYYYMMDD
        self.cli_params = (path[0], (
                SSN,
                f"{start[2]}{start[0]}{start[1]}",
                f"{end[2]}{end[0]}{end[1]}"
            ))

    def cli_query(self, path: tuple):
        """
        The cli_query method handles the DataClient querying and displaying
        the result. Passes the DataClient.query method that component id and
        query parameters saved in the cli_params attribute by the component
        that had just terminated before this call.
        """

        # Terminate if the exit option was chosen
        if path[1] == "EXIT":
            print("\nThank you for using the Loan Application Interface!\n")
            self.dc.stop()
            exit(0)

        # Release limits on max columns and rows and display width
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)
        pd.set_option('display.width', 150)

        comp_id, params = self.cli_params

        # Query the data with the DataClient
        data = self.dc.query(comp_id.upper(), params)

        # If the query came back empty, print a message and return
        if not data:
            print("\nNo matching records.\n")
            return

        # Construct a DataFrame from the data
        df = pd.DataFrame(data[1:], columns=data[0])

        # Sort the DataFrame by timestamp if the column exists
        if 'Date' in df.columns:
            df = df.sort_values(by='Date', ascending=False)

        # Clear the console
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        # Print the dataframe
        print("\nQuery Successful.\n\n")
        print(df)

        # Total value if the value column exists
        if 'Value' in df.columns:
            total_value = round(df['Value'].sum(), 2)
            print(f"\nTotal: {total_value}")

    @staticmethod
    def valid_date(user_input: str):
        """
        Validates a date input with tokens separated by a '-'
        """

        try:
            # Extract the tokens from the date and cast each to an int
            tokens = [int(t) for t in user_input.split('-')]

            # Unpack the tokens and assign the day to 1 by default
            if len(tokens) == 2:
                month, year, day = tokens+[1]
            else:
                month, day, year = tokens

            # Attempt to convert the date to a datetime and validate the year
            datetime(year, month, day)
            return year <= 2025

        except Exception:
            return False

    # Build the menu by component
    def build_menu(self) -> None:

        # Transaction Details (Divider)
        # Prompts user for zipcode and date
        transactions_div = MenuDivider(
            UserInput(
                id='zip',
                prompt="Please enter a zipcode (5 digits): ",
                regex=VALIDATIONS['zip']
            ),
            UserInput(
                id='date',
                prompt="Please enter a month and year (MM-YYYY): ",
                length=7,
                regex=VALIDATIONS['mmyyyy'],
                custom=self.valid_date
            ),
            id='view_transactions',
            pass_values=self.view_transactions
        )

        # View Account Details (Divider)
        # Prompts the user for Social Security Number
        view_account_div = MenuDivider(
            UserInput(
                id='SSN',
                prompt="Please enter the Social Security Number (9 digits): ",
                regex=VALIDATIONS['SSN']
            ),
            id='view_account',
            pass_values=self.view_account
        )

        # Modify Account (Divider)
        # Prompts user for the attribute and updated value
        modify_account_div = MenuDivider(
            UserInput(
                id='SSN',
                prompt="Please enter the Social Security Number (9 digits): ",
                regex=VALIDATIONS['SSN']
            ),
            MultipleChoice(
                id='modify_attribute',
                prompt="Which value would you like to update? ",
                options={
                    "First Name": UserInput(
                        id="FIRST_NAME",
                        prompt="Please enter the new value: ",
                        regex=VALIDATIONS['name']
                    ),
                    "Middle Name": UserInput(
                        id="MIDDLE_NAME",
                        prompt="Please enter the new value: ",
                        regex=VALIDATIONS['name']
                    ),
                    "Last Name": UserInput(
                        id="LAST_NAME",
                        prompt="Please enter the new value: ",
                        regex=VALIDATIONS['name']
                    ),
                    "Credit Card Number": UserInput(
                        id="CREDIT_CARD_NO",
                        prompt="Please enter the new value (16 digits): ",
                        regex=VALIDATIONS['CCN']
                    ),
                    "Street Address": UserInput(
                        id="FULL_STREET_ADDRESS",
                        prompt="Please enter the new value: ",
                        regex=VALIDATIONS['address']
                    ),
                    "City": UserInput(
                        id="CUST_CITY",
                        prompt="Please enter the new value: ",
                        regex=VALIDATIONS['city']
                    ),
                    "State": UserInput(
                        id="CUST_STATE",
                        prompt="Please enter the new value (ex: FL): ",
                        regex=VALIDATIONS['state']
                    ),
                    "Country": UserInput(
                        id="CUST_COUNTRY",
                        prompt="Please enter the new value: ",
                        regex=VALIDATIONS['country']
                    ),
                    "Zip Code": UserInput(
                        id="CUST_ZIP",
                        prompt="Please enter the new value (5 digits): ",
                        regex=VALIDATIONS['zip']
                    ),
                    "Phone Number": UserInput(
                        id="CUST_PHONE",
                        prompt="Please enter the new value ((XXX)XXX-XXXX): ",
                        regex=VALIDATIONS['phone_number']
                    ),
                    "Email": UserInput(
                        id="CUST_EMAIL",
                        prompt="Please enter the new value: ",
                        regex=VALIDATIONS['email']
                    )
                }
            ),
            id='modify_account',
            pass_values=self.modify_account
        )

        # Generate Monthly Bill (Divider)
        # Prompts user for Credit Card Number and date
        generate_bill_div = MenuDivider(
            UserInput(
                id="CCN",
                prompt="Please enter the credit card number: ",
                regex=VALIDATIONS['CCN']
            ),
            UserInput(
                id="date",
                prompt="Please enter the date (MM-YYYY): ",
                regex=VALIDATIONS['mmyyyy'],
                custom=self.valid_date
            ),
            id='generate_bill',
            pass_values=self.generate_bill
        )

        # Transactions Timeframe (Divider)
        # Prompts user for start and end dates
        transactions_timeframe_div = MenuDivider(
            UserInput(
                id='SSN',
                prompt="Please enter the Social Security Number (9 digits): ",
                regex=VALIDATIONS['SSN']
            ),
            UserInput(
                id="start_date",
                prompt="Please enter the starting date (MM-DD-YYYY)",
                regex=VALIDATIONS['mmddyyyy'],
                custom=self.valid_date
            ),
            UserInput(
                id="end_date",
                prompt="Please enter the ending date (MM-DD-YYYY)",
                regex=VALIDATIONS['mmddyyyy'],
                custom=self.valid_date
            ),
            id="transactions_timeframe",
            pass_values=self.transactions_timeframe
        )

        # Customer Details (Navigation)
        # Prompts user for Social Security Number and customer action
        customers_nav = MultipleChoice(
            prompt="Please select an action: ",
            options={
                "View Account Details": view_account_div,
                "Modify Account Details": modify_account_div,
                "Generate Monthly Bill": generate_bill_div,
                "Display Transactions by Timeframe": transactions_timeframe_div
            },
            id='customers_nav'
        )

        # Main Menu (Navigator)
        # Prompts the user for the query type they would like to make
        menu_nav = MultipleChoice(
            root=True,
            id='menu_nav',
            prompt=(
                "\nWelcome to the Loan Application Interface!"
                "\nWould you like to view transcation or customer details?"
            ),
            options={
                "Transactions": transactions_div,
                "Customers": customers_nav,
                "Exit": "EXIT"
            },
            pass_values=self.cli_query
        )

        self.menu = menu_nav

    def run(self):
        self.menu.run()


if __name__ == "__main__":

    # Initialize SafeSQL connection
    ssql = SafeSQL(
        user='root',
        password='password',
        host='127.0.0.1'
    )

    ssql.run("USE creditcard_capstone;")

    mycli = CLIManager(ssql)
    mycli.run()
