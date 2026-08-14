from snowflake.connector import connect

conn = connect(connection_name="OLIST_PROJECT")
cur = conn.cursor()

tables = ['customers', 'geolocation', 'order_items', 'order_payments',
          'order_reviews', 'orders', 'products', 'sellers', 'product_category_translation']

for table in tables:
    local_path = f"raw_data/olist_{table}_dataset.csv"
    staged_file = f"olist_{table}_dataset.csv.gz"

    cur.execute(f"PUT file://{local_path} @OLIST_DB.RAW.OLIST_STAGE AUTO_COMPRESS=TRUE")

    result = cur.execute(f"""
        COPY INTO OLIST_DB.RAW.{table.upper()}
        FROM @OLIST_DB.RAW.OLIST_STAGE/{staged_file}
        FILE_FORMAT = (FORMAT_NAME = OLIST_DB.RAW.CSV_FORMAT)
        ON_ERROR = 'CONTINUE'
    """).fetchall()

    print(f"{table}: {result}")

conn.close()