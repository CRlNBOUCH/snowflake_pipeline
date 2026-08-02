from snowflake.connector import connect

conn = connect(connection_name = 'OLIST_PROJECT')
cur = conn.cursor()

schema = 'RAW'
all_columns = {}

tables = ['CUSTOMERS_DEBUG', 'GEOLOCATION_DEBUG', 'ORDER_ITEMS_DEBUG', 'ORDER_PAYMENTS_DEBUG',
          'ORDER_REVIEWS_DEBUG', 'ORDERS_DEBUG', 'PRODUCTS_DEBUG', 'SELLERS_DEBUG', 'PRODUCT_CATEGORY_TRANSLATION_DEBUG']

for table in tables :
    query = f"""
                SELECT COLUMN_NAME 
                FROM OLIST_DB.INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}';
            """
    cur.execute(query)
    rows = cur.fetchall()
    columns = [row[0] for row in rows]
    all_columns[table] = columns
    print(f"{table} : {len(columns)} columns found :{all_columns[table]}.")


for table, columns in all_columns.items():
    table_name = f"OLIST_DB.{schema}.{table}"

    for column in columns:
        call_str = f"CALL CHECK_NULLS('{table_name}', '{column}')"
        print(repr(call_str))   # repr() shows hidden whitespace/newlines that print() would hide
        cur.execute(call_str)
        cur.execute(f"CALL CHECK_NULLS('{table_name}', '{column}')")
        total, successful, failed = cur.fetchone()
        print(f"{table}.{column}: total={total}, successful={successful}, failed={failed}")
    print('-----------------------------------------------------------------')

conn.close()
    