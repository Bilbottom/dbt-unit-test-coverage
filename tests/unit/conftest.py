"""
Create the fixtures to use throughout the tests.
"""
import pathlib

import pytest

from dbt_unit_test_coverage.dbt import DbtConfig


@pytest.fixture
def dbt_config(tmp_path: pathlib.Path) -> DbtConfig:
    return DbtConfig(
        name="test",
        dbt_project_root=tmp_path,
        model_paths=[tmp_path / "models"],
        test_paths=[tmp_path / "tests"],
        target_path=tmp_path / "target",
    )
