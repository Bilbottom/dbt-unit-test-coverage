"""
Test the ``dbt_unit_test_coverage/dbt/config.py`` module.
"""

import pathlib
import textwrap

import pytest

import dbt_unit_test_coverage.dbt.config as config

pytestmark = pytest.mark.unit  # noqa


@pytest.fixture
def dbt_config_root(tmp_path) -> pathlib.Path:
    """
    Create a mock ``dbt_project.yml`` file in a temp directory.
    """
    dbt_project = tmp_path / "dbt_project.yml"
    dbt_project.write_text(
        textwrap.dedent(
            """
            ---
            name: project_name
            model-paths: ["models"]
            test-paths: ["tests"]
            target-path: "target"
            """
        )
    )
    return tmp_path


def test__dbt_config__compiled_paths(dbt_config_root: pathlib.Path):
    """
    Test the ``DbtConfig`` dataclass.
    """
    dbt_config = config.DbtConfig.from_root(dbt_config_root)

    assert dbt_config.compiled_paths == [dbt_config_root / "target/compiled/project_name/models"]


def test__dbt_config__from_root(dbt_config_root: pathlib.Path):
    """
    Test the ``DbtConfig`` dataclass.
    """
    dbt_config = config.DbtConfig.from_root(dbt_config_root)

    assert dbt_config.name == "project_name"
    assert dbt_config.model_paths == [dbt_config_root / "models"]
    assert dbt_config.test_paths == [dbt_config_root / "tests"]
    assert dbt_config.target_path == dbt_config_root / "target"
