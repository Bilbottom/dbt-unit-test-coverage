"""
Test the ``dbt_unit_test_coverage/__main__.py`` module.
"""
import os
import pathlib

import pytest
import typer

import dbt_unit_test_coverage.main as main


@pytest.fixture(scope="session", autouse=True)
def set_env() -> None:
    """
    Set the environment variables.
    """
    os.environ["TEST__DBT_UNIT_TEST_COVERAGE__BAR"] = "bar"
    main._DISTRIBUTION_METADATA["version"] = "1.2.3"


@pytest.mark.parametrize(
    "path, env_var, default, expected",
    [
        ("foo", "TEST__DBT_UNIT_TEST_COVERAGE__BAR", "baz", "foo"),
        (None, "TEST__DBT_UNIT_TEST_COVERAGE__BAR", "baz", "bar"),
        (None, "TEST__DBT_UNIT_TEST_COVERAGE__FOO", "baz", "baz"),
    ],
)
def test__get_path(
    path: str,
    env_var: str,
    default: str,
    expected: str,
) -> None:
    """
    Test the ``_get_path`` function.
    """
    assert main._get_path(path, env_var, default) == pathlib.Path(expected)


def test__version_callback(capsys) -> None:
    """
    Test the ``_version_callback`` function.
    """
    with pytest.raises(typer.Exit):
        main._version_callback(True)
        captured = capsys.readouterr()
        assert captured.out == "1.2.3"
