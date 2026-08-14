{%  macro to_date_key(column) %}
    TO_NUMBER(TO_CHAR({{column}},'YYYYMMDD'))
{% endmacro %}