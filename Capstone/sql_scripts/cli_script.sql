-- %%VIEW_TRANSACTIONS%%
-- Join the credit card and customer table, query only the credit card data
SELECT
    cc.TRANSACTION_ID 'Transaction ID',
    cc.TRANSACTION_VALUE 'Value',
    cc.TRANSACTION_TYPE 'Type',
    cc.BRANCH_CODE 'Branch Code',
    cc.CUST_SSN 'SSN',
    cc.TIMEID 'Date',
    cc.CUST_CC_NO 'CCN'
FROM
    cdw_sapp_credit_card cc
LEFT JOIN
    cdw_sapp_customer cust
ON
    cc.cust_ssn = cust.ssn
WHERE
    cust.cust_zip = {}
    AND cc.timeid LIKE '{}%';

-- %%VIEW_ACCOUNT%%
-- Query the customer data matching the SSN
SELECT
    SSN,
    FIRST_NAME 'First',
    MIDDLE_NAME 'Middle',
    LAST_NAME 'Last',
    CREDIT_CARD_NO 'CCN',
    FULL_STREET_ADDRESS 'Address',
    CUST_CITY 'City',
    CUST_STATE 'State',
    CUST_COUNTRY 'Country',
    CUST_ZIP 'Zip Code',
    CUST_PHONE 'Phone',
    CUST_EMAIL 'Email',
    LAST_UPDATED 'Last Updated'
FROM
    cdw_sapp_customer
WHERE
    ssn = {};

-- %%MODIFY_ACCOUNT%%
-- Update the value
UPDATE
    cdw_sapp_customer
SET
    {} = '{}'
WHERE
    ssn = {};

-- Query the updated row
SELECT
    SSN,
    FIRST_NAME 'First',
    MIDDLE_NAME 'Middle',
    LAST_NAME 'Last',
    CREDIT_CARD_NO 'CCN',
    FULL_STREET_ADDRESS 'Address',
    CUST_CITY 'City',
    CUST_STATE 'State',
    CUST_COUNTRY 'Country',
    CUST_ZIP 'Zip Code',
    CUST_PHONE 'Phone',
    CUST_EMAIL 'Email',
    LAST_UPDATED 'Last Updated'
FROM
    cdw_sapp_customer
WHERE
    ssn = {};

-- %%GENERATE_BILL%%
-- Select the transaction details for a credit card number during a specified year and month
SELECT
    transaction_value 'Value',
    transaction_type 'Type',
    timeid 'Date'
FROM
    cdw_sapp_credit_card
WHERE
    cust_cc_no = {}
    AND timeid LIKE '{}%';

-- %%TRANSACTIONS_TIMEFRAME%%
-- Select the transaction info for a customers transactions in a timeframe
SELECT
    cc.transaction_id 'Transaction ID',
    cc.transaction_value 'Value',
    cc.transaction_type 'Type',
    cc.timeid 'Date',
    cc.cust_cc_no 'CCN'
FROM
    cdw_sapp_credit_card cc
LEFT JOIN
    cdw_sapp_customer cust
ON
    cust.ssn = cc.cust_ssn
WHERE
    cust.ssn = {}
    AND cc.timeid >= {}
    AND cc.timeid <= {};