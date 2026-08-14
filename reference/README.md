# Reference

Scripts and SQL written during the manual exploration phase before migrating to dbt. Kept for context they document how the data was profiled , how the star schema was designed, and the reasoning behind decisions that are now encoded in the dbt models .

`check_nulls_procedure.sql` and `nulls_checking.py` were used together to profile null rates across every column in every table after loading. Findings from this are in `docs/data_profiling.md`. The dbt `not_null` tests in `schema.yml` now enforce what this phase established.

`creating_tables.sql` and `data_modeling.sql` cover the manual star schema build DDL, grain verification queries, and PK/FK declarations. All of this is now handled by dbt models and `post_hook` constraints in `models/analytics/`.