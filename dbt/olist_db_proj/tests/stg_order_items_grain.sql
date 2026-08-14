-- tests/assert_stg_order_items_grain.sql
SELECT ORDER_ID, ORDER_ITEM_ID, COUNT(*) AS cnt
FROM {{ ref('stg_order_items') }}
GROUP BY ORDER_ID, ORDER_ITEM_ID
HAVING cnt > 1