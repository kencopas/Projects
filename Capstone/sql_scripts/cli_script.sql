-- %%VIEW_TRANSACTIONS%%
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
    cust.cust_zip = %p
    AND cc.timeid LIKE '%p%';

-- %%VIEW_ACCOUNT%%
-- Query the customer data matching the SSN
SELECT
    *
FROM
    cdw_sapp_customer
WHERE
    ssn = %p;

-- %%MODIFY_ACCOUNT%%
-- Update the value
UPDATE
    cdw_sapp_customer
SET
    %p = '%p'
WHERE
    ssn = %p;

-- Query the updated row
SELECT
    *
FROM
    cdw_sapp_customer
WHERE
    ssn = %p;

-- %%GENERATE_BILL%%
-- Select the transaction details for a credit card number during a specified year and month
SELECT
    transaction_value 'Value',
    transaction_type 'Type',
    timeid 'Timestamp'
FROM
    cdw_sapp_credit_card
WHERE
    cust_cc_no = %p
    AND timeid LIKE '%p%';

-- %%TRANSACTIONS_TIMEFRAME%%
-- Select the transaction info for a customers transactions in a timeframe
SELECT
    cc.transaction_value,
    cc.transaction_type,
    cc.timeid,
    cc.cust_cc_no
FROM
    cdw_sapp_credit_card cc
LEFT JOIN
    cdw_sapp_customer cust
ON
    cust.ssn = cc.cust_ssn
WHERE
    cust.ssn = %p
    AND cc.timeid >= %p
    AND cc.timeid <= %p;