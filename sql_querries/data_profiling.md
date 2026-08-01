# Data Profiling Olist Raw Layer

Before building staging models, I profiled every raw table for null rates and casting issues. Method: a reusable `CHECK_NULLS(table, column)` procedure ran against every column, and any high null rate got a follow-up query comparing raw values to their cast attempt, to tell apart "genuinely missing" from "failed to parse."

## Clean tables
`customers`, `geolocation`, `order_payments`, `sellers`, `product_category_translation` zero nulls anywhere , some of them where all strings which helped with the 0 nulls casting .

## Expected nulls (not an issue)
- **orders**: delivery timestamps (`carrier`, `customer`) are null for 1.8–3% of rowsthese are orders still in transit or cancelled, so the absence is meaningful, not missing data.
- **order_reviews**: `review_comment_message` (59% null) and `review_comment_title` (88% null) are optional free-text fields; `review_score` itself is 100% populated. Customers rate but rarely write comments.
- **order_items.freight_value**: 0.6% null, confirmed genuine source data, not a casting artifactlow enough to leave as-is.

## Investigated and resolved
- **order_items.price**: initially showed 36% null when checked through a debug view.Fixed by correcting the view to `TRY_TO_DECIMAL(PRICE, 10, 3)`; re-checked and confirmed clean

- **products**: four fields (`category_name`, `name_lenght`, `description_lenght`, `photos_qty`) each showed 610 nulls independently. Confirmed via a row-level check that these are the same 610 rows, null on all four fields simultaneously (32,341 rows have zero nulls across these fields, 610 have exactly four)a clean binary split rather than scattered gaps. Confirmed these are 610 genuinely distinct `product_id`s, not a duplication artifact, and that their weight/dimension fields are still populatedmeaning these are real, shippable products missing only descriptive/marketing metadata, likely from incomplete seller listings.

## Decisions
- No rows dropped anywheretables aren't linked with keys yet, so removing rows now risks orphaning references once joins are built.
- Nulls stay as `NULL` through staging; anything downstream that needs a non-null value filters explicitly at the point of use.
- No imputationnone of these fields have a defensible default value.
- The 610 incomplete product listings are kept as-is; `product_id` and core identifiers are intact, so the rows remain fully usable for anything not dependent on the missing fields.

## Next
- Move these views from `RAW` into a dedicated `STAGING` schema (`STG_` naming), replacing the debug versions.
- Build the star schema (`fact_orders`, `dim_customer`, `dim_product`, etc.) on top of staging.