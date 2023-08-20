<div align="center">

[![Python 3.9](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![GitHub last commit](https://img.shields.io/github/last-commit/Bilbottom/dbt-unit-test-coverage)](https://github.com/Bilbottom/dbt-unit-test-coverage/commits/main)
[![coverage](coverage.svg)](https://github.com/dbrgn/coverage-badge)

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Bilbottom/dbt-unit-test-coverage/main.svg)](https://results.pre-commit.ci/latest/github/Bilbottom/dbt-unit-test-coverage/main)

</div>

---

# dbt Unit Test Coverage 🧪🔣

This is a package to generate a code coverage metric for dbt models' unit tests.

This is not for public consumption (yet!), but rather to show off some Sainsbury's extensions. This also requires a specific fork of the dbt-unit-testing package, namely:

- https://github.com/Bilbottom/dbt-unit-testing

## Usage 📖

This package will generate a **very rudimentary** coverage metric for the dbt models' unit tests. We can't measure line hits like we can with Python code, but we can measure the number of models that have unit tests and _which of their CTEs_ have unit tests.

To run the code coverage report, invoke the `dbt-unit-test-coverage` package after compiling the project:

```bash
dbt clean
dbt deps
dbt compile

dbt-unit-test-coverage
```

Help for the `dbt-unit-test-coverage` package can be generated using the `--help` flag thanks to [the `typer` library](https://typer.tiangolo.com/):

```bash
dbt-unit-test-coverage --help
```

## Summary of extensions

### CTE unit testing

This builds off of another fork, this one from the [EqualExperts/dbt-unit-testing](https://github.com/EqualExperts/dbt-unit-testing) repo:

- https://github.com/Bilbottom/dbt-unit-testing

This fork adds the ability to unit test particular CTEs in a model, provided you follow [the dbt-labs style guide](https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md) and include [the `select * from final` line](https://github.com/dbt-labs/corp/blob/725b6e9cf2af208d24a52fc04095c2feaff20b9d/dbt_style_guide.md?plain=1#L157-L158) at the bottom of the model.

### Code coverage

With the CTE unit tests, we can then measure the number of (logical) CTEs that don't have tests which forms the coverage metric.

## Future plans

The v1.5 release of [dbt-core](https://github.com/dbt-labs/dbt-core) introduced programmatic invocations:

- https://docs.getdbt.com/reference/programmatic-invocations

This would allow us to piggyback off of the dbt functionality even more, rather than hacking together our own solutions.

Additionally, the coverage metric is easy to manipulate in your favour, so we intend to improve the metric by:

- Validating the columns in the tests to make sure that each of the columns in the CTE are tested
- Penalising CTEs that are overcomplicated and should be split into multiple CTEs (e.g. a CTE that has large sub-queries)

This is currently based on the [EqualExperts/dbt-unit-testing](https://github.com/EqualExperts/dbt-unit-testing) framework, but this package will be updated to also be able to use whatever native unit testing framework dbt ends up having -- see:

- https://github.com/dbt-labs/dbt-core/discussions/8275
