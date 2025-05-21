from utils.cli_utils import MultipleChoice, UserInput, MenuDivider

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

    def __init__(self, ssql: object):

        # Save the SafeSQL connection
        self.ssql = ssql

        # Build the menu
        self.build_menu()

    # Build the menu by component
    def build_menu(self) -> None:

        # Transactions Prompts - Prompts user for zipcode, month, and year
        transactions_div = MenuDivider(
            UserInput(id='tzip', prompt="Please enter a zipcode (5 digits): ", type=int, length=[5]),
            UserInput(id='tdate', prompt="Please enter a month and year (MM-YYYY): ", length=[7], custom=valid_date),
            id='transactions_div',
            pass_values=self.transactions
        )

        # Modify Account Prompts - Prompts user for the attribute and updated value 
        modify_account_div = MenuDivider(
            MultipleChoice(
                id='modify_attribute',
                prompt="Which value would you like to update? ",
                nav=self.CUST_SCHEMA_KEY
            ),
            UserInput(id='modify_value', prompt="What would you like to update the value to? "),
            id='modify_account_div'
        )

        # 
        generate_bill_div = MenuDivider(
            UserInput(id="CCN", prompt="Please enter the credit card number: ", type=int, length=[16]),
            UserInput(id="gbdate", prompt="Please enter the month and year (MM-YYYY): ", length=[7], custom=valid_date),
            id='generate_bill_div'
        )

        transactions_timeframe_div = MenuDivider(
            UserInput(id="tstartdate", prompt="Please enter the year, month, and day of the starting date (MM-DD-YYYY)", length=[10], custom=valid_date),
            UserInput(id="tenddate", prompt="Please enter the year, month, and day of the ending date (MM-DD-YYYY)", length=[10], custom=valid_date),
            id="transactions_timeframe_div",
        )

        customers_nav = MenuDivider(
            UserInput(id='SSN', prompt="Please enter the Social Security Number (9 digits): ", type=int, length=[9]),
            MultipleChoice(
                prompt="Please select an action: ",
                options={
                    "View Account Details": "view",
                    "Modify Account Details": modify_account_div,
                    "Generate Monthly Bill": generate_bill_div,
                    "Display Transactions by Timeframe": transactions_timeframe_div
                }
            ),
            id='customers_nav',
            pass_values=self.customers
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

    # Uses zip code and mm-yyyy timestamp to query database for all transactions made with those properties sorted by day
    def transactions(self, path: tuple):
        
        path = dict(path)

        # DEBUG
        print("CLIManager.transactions input: ")
        print(path)

        # self.ssql.run(f"""
        #     SELECT
        #         *
        #     FROM
        #         cdw_sapp_transactions
        #     WHERE
                
        # """)

    # Lists the existing account details of a customer if prompted
    def customers(self, path: tuple):
        print("CLIManager.customers input: ")
        print(path)

    def run(self):
        self.menu.run()
    
if __name__ == "__main__":

    mycli = CLIManager()
    mycli.run()