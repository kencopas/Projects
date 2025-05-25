from datetime import datetime

from utils.sql_utils import SafeSQL
from utils.cli_utils import MultipleChoice, UserInput, MenuDivider


# Validate a date input format
def valid_date(user_input: str):

    # Extract the tokens from the date and cast each to an int
    tokens = [int(t) for t in user_input.split('-')]

    # Unpack the tokens and assign the day to 1 by default
    if len(tokens) == 2:
        month, year, day = tokens+[1]
    else:
        month, day, year = tokens

    # Attempt to convert the date to a datetime and validate the year
    try:
        datetime(year, month, day)
        return year <= 2025
    except Exception:
        return False


class CLIManager:

    def __init__(self, app: object):

        self.app = app

        # Build the menu
        self.build_menu()

    # Build the menu by component
    def build_menu(self) -> None:

        # Transaction Details (Divider)
        # Prompts user for zipcode and date
        transactions_div = MenuDivider(
            UserInput(
                id='zip',
                prompt="Please enter a zipcode (5 digits): ",
                type=int,
                length=[5]
            ),
            UserInput(
                id='date',
                prompt="Please enter a month and year (MM-YYYY): ",
                length=[7],
                custom=valid_date
            ),
            id='view_transactions',
            pass_values=self.app.cli_query
        )

        # Modify Account (Divider)
        # Prompts user for the attribute and updated value
        modify_account_div = MenuDivider(
            UserInput(
                id='SSN',
                prompt="Please enter the Social Security Number (9 digits): ",
                type=int,
                length=[9]
            ),
            MultipleChoice(
                id='attribute',
                prompt="Which value would you like to update? ",
                options={
                    "First Name": "FIRST_NAME",
                    "Middle Name": "MIDDLE_NAME",
                    "Last Name": "LAST_NAME",
                    "Credit Card Number": "CREDIT_CARD_NO",
                    "Street Address": "FULL_STREET_ADDRESS",
                    "City": "CUST_CITY",
                    "State": "CUST_STATE",
                    "Country": "CUST_COUNTRY",
                    "Zip Code": "CUST_ZIP",
                    "Phone Number": "CUST_PHONE",
                    "Email": "CUST_EMAIL"
                }
            ),
            UserInput(
                id='new_value',
                prompt="What would you like to update the value to? "
            ),
            id='modify_account'
        )

        # Generate Monthly Bill (Divider)
        # Prompts user for Credit Card Number and date
        generate_bill_div = MenuDivider(
            UserInput(
                id="CCN",
                prompt="Please enter the credit card number: ",
                type=int,
                length=[16]
            ),
            UserInput(
                id="date",
                prompt="Please enter the date (MM-YYYY): ",
                length=[7],
                custom=valid_date
            ),
            id='generate_bill'
        )

        # Transactions Timeframe (Divider)
        # Prompts user for start and end dates
        transactions_timeframe_div = MenuDivider(
            UserInput(
                id='SSN',
                prompt="Please enter the Social Security Number (9 digits): ",
                type=int,
                length=[9]
            ),
            UserInput(
                id="start_date",
                prompt="Please enter the starting date (MM-DD-YYYY)",
                length=[10],
                custom=valid_date
            ),
            UserInput(
                id="end_date",
                prompt="Please enter the ending date (MM-DD-YYYY)",
                length=[10],
                custom=valid_date
            ),
            id="transactions_timeframe",
        )

        # View Account Details (Divider)
        # Prompts the user for Social Security Number
        view_account_div = MenuDivider(
            UserInput(
                id='SSN',
                prompt="Please enter the Social Security Number (9 digits): ",
                type=int,
                length=[9]
            ),
            id='view_account'
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
            id='customers_nav',
            pass_values=self.app.cli_query
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
                "Customers": customers_nav
            }
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
