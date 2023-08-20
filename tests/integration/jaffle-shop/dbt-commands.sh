
dbt clean --project-dir tests/integration/jaffle-shop
dbt deps --project-dir tests/integration/jaffle-shop

dbt seed --project-dir tests/integration/jaffle-shop --profiles-dir tests/integration/jaffle-shop
dbt run --project-dir tests/integration/jaffle-shop --profiles-dir tests/integration/jaffle-shop

dbt compile --project-dir tests/integration/jaffle-shop --profiles-dir tests/integration/jaffle-shop
