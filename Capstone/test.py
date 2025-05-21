from utils.sql_utils import SafeSQL

my = SafeSQL(user='root', password='password', host='127.0.0.1')

def view_details(ssn: int):
    my.run(f"""
        SELECT
            *
        FROM
            cdw_sapp_customer
        WHERE
            SSN = {ssn};
    """)

def modify_details(attr: str, value: str | int, ssn: int):
    my.run(f"""
        UPDATE
            cdw_sapp_customer
        SET
            {attr} = {value}
        WHERE
            SSN = {ssn};
    """)

def generate_bill(timestamp: str):
    my.run(f"""
        SELECT
            TRANSACTION_ID,
            TRANSACTION_VALUE,
            TRANSACTION_TYPE,
            TIMEID
        FROM
            cdw_sapp_credit_card
        WHERE
            CUST_SSN = 123459988
            AND TIMEID LIKE "{timestamp}%";
    """)