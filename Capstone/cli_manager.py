from utils.cli_utils import MultipleChoice, UserInput, MenuDivider
from utils.sql_utils import SafeSQL

# Validate a date input format
def valid_date(user_input: str):
    # MM-YYYY
    if len(user_input) == 7:
        month, year = user_input.split('-')
        return (1 <= int(month) <= 12) and (0 <= int(year) <= 2025)
    # MM-DD-YYYY
    else:
        month, day, year = user_input.split('-')
        return (1 <= int(month) <= 12) and (1 <= int(day) <= 31) and (0 <= int(year) <= 2025)
    
class CLIManager:

    # Key maps CLI-presented options to MySQL column names
    CUST_SCHEMA_KEY = {
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

    def __init__(self, app: object):
        
        self.app = app

        # Build the menu
        self.build_menu()

    # Build the menu by component
    def build_menu(self) -> None:

        # Transactions (Divider) - Prompts user for zipcode, month, and year
        transactions_div = MenuDivider(
            UserInput(id='tzip', prompt="Please enter a zipcode (5 digits): ", type=int, length=[5]),
            UserInput(id='tdate', prompt="Please enter a month and year (MM-YYYY): ", length=[7], custom=valid_date),
            id='transactions_div',
            pass_values=self.app.cli_query
        )

        # Modify Account (Divider) - Prompts user for the attribute and updated value 
        modify_account_div = MenuDivider(
            UserInput(id='SSN', prompt="Please enter the Social Security Number (9 digits): ", type=int, length=[9]),
            MultipleChoice(
                id='modify_attribute',
                prompt="Which value would you like to update? ",
                options=self.CUST_SCHEMA_KEY
            ),
            UserInput(id='modify_value', prompt="What would you like to update the value to? "),
            id='modify_account_div'
        )

        # Generate Monthly Bill (Divider) - Prompts user for Credit Card Number and month-date timestamp
        generate_bill_div = MenuDivider(
            UserInput(id="CCN", prompt="Please enter the credit card number: ", type=int, length=[16]),
            UserInput(id="gbdate", prompt="Please enter the month and year (MM-YYYY): ", length=[7], custom=valid_date),
            id='generate_bill_div'
        )

        # Transactions Timeframe (Divider) - Prompts user for month-day-year timestamps for start and end dates
        transactions_timeframe_div = MenuDivider(
            UserInput(id='SSN', prompt="Please enter the Social Security Number (9 digits): ", type=int, length=[9]),
            UserInput(id="tstartdate", prompt="Please enter the year, month, and day of the starting date (MM-DD-YYYY)", length=[10], custom=valid_date),
            UserInput(id="tenddate", prompt="Please enter the year, month, and day of the ending date (MM-DD-YYYY)", length=[10], custom=valid_date),
            id="transactions_timeframe_div",
        )

        view_account_div = MenuDivider(
            UserInput(id='SSN', prompt="Please enter the Social Security Number (9 digits): ", type=int, length=[9]),
            id='view_account'
        )

        # Customers (Navigation) - Prompts user for Social Security Number and customer action, routes to the proper divider
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

        menu_nav = MultipleChoice(
            id='menu_nav',
            prompt="Welcome to the Loan Application Interface! Would you like to view transcation details or customer details?",
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