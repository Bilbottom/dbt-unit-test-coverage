"""
Entry point for the ``dbt_unit_test_coverage`` package.
"""
import typer

import dbt_unit_test_coverage.main

app = lambda: typer.run(dbt_unit_test_coverage.main.main)  # noqa: E731
if __name__ == "__main__":
    app()
