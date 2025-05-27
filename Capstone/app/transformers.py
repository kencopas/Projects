"""

This file contains the ETL constants and file-specific transformer functions
for data to be cleaned and formatted before being loaded into the MySQL
database. The TRANSFORMERS_MAP maps the filename to the transformer function
designated.

"""

from pyspark.sql.functions import col, lower, concat, lit, substring, lpad


def transform_customer(df):

    """
    MIDDLE_NAME -> lowercase
    FULL_STREET_ADDRESS -> <STREET_NAME>, <APT_NO>
    CUST_PHONE -> (XXX)XXX-XXXX
    APT_NO -> drop
    STREET_NAME -> drop
    """

    try:
        df = df \
            .withColumn("MIDDLE_NAME", lower("MIDDLE_NAME")) \
            .withColumn("FULL_STREET_ADDRESS", concat(
                col("STREET_NAME"), lit(", "), col("APT_NO").cast("string")
            )) \
            .withColumn("CUST_PHONE", concat(
                lit("(XXX)"),
                substring(col("CUST_PHONE").cast("string"), 1, 3),
                lit("-"),
                substring(col("CUST_PHONE").cast("string"), 4, 4)
            )) \
            .drop("APT_NO").drop("STREET_NAME")

        return df

    except Exception as e:
        print(f"Exception occured: {e}")


def transform_branch(df):

    """

    BRANCH_ZIP -> default=999999
    BRANCH_PHONE -> (XXX)XXX-XXXX

    """

    try:
        df = df \
            .fillna({"BRANCH_ZIP": "999999"}) \
            .withColumn("BRANCH_PHONE", concat(
                lit("("),
                substring(col("BRANCH_PHONE").cast("string"), 1, 3),
                lit(")"),
                substring(col("BRANCH_PHONE").cast("string"), 4, 3),
                lit("-"),
                substring(col("BRANCH_PHONE").cast("string"), 7, 4)
            ))

        return df

    except Exception as e:
        print(f"Exception occured: {e}")


def transform_credit(df):

    """

    CREDIT_CARD_NO -> rename CUST_CC_NO
    TIMEID -> YYYYMMDD
    YEAR -> drop
    MONTH -> drop
    DAY -> drop

    """

    try:
        df = df \
            .withColumnRenamed("CREDIT_CARD_NO", "CUST_CC_NO") \
            .withColumn("TIMEID", concat(
                col("YEAR").cast("string"),
                lpad(col("MONTH").cast("string"), 2, "0"),
                lpad(col("DAY").cast("string"), 2, "0")
            )) \
            .drop("YEAR").drop("MONTH").drop("DAY")

        return df

    except Exception as e:
        print(f"Exception occured: {e}")


# Maps the data filenames to the corresponding transformer function
transformers_map: dict[str: callable] = {
    'cdw_sapp_customer': transform_customer,
    'cdw_sapp_branch': transform_branch,
    'cdw_sapp_credit_card': transform_credit
}
