import os
from snowflake.connector import connect

conn = connect(
    user=os.environ['SNOWFLAKE_USER'],
    password=os.environ['SNOWFLAKE_PASSWORD'],
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    database=os.environ['SNOWFLAKE_DATABASE'],
    role=os.environ['SNOWFLAKE_ROLE'],
    warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
)
cur = conn.cursor()

tables = [
    'customers', 'geolocation', 'order_items', 'order_payments',
    'order_reviews', 'orders', 'products', 'sellers', 'product_category_translation'
]

for table in tables:
    result = cur.execute(f"""
        COPY INTO OLIST_DB.RAW.{table.upper()}
        FROM @OLIST_DB.RAW.OLIST_S3_STAGE/olist_{table}_dataset.csv
        FILE_FORMAT = (FORMAT_NAME = OLIST_DB.RAW.CSV_FORMAT)
        ON_ERROR = 'CONTINUE'
    """).fetchall()

    print(f"{table}: {result}")

conn.close()