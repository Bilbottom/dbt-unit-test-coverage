"""
Generate the code coverage for the dbt project.
"""
from __future__ import annotations

import importlib.metadata
import os
import pathlib
import subprocess
from typing import Annotated

import typer

from dbt_unit_test_coverage.badge import generate_badge
from dbt_unit_test_coverage.coverage import compute_test_coverage

_DISTRIBUTION_METADATA = importlib.metadata.metadata("dbt_unit_test_coverage")


def _get_path(path: str | None, env_var: str, default: str) -> pathlib.Path:
    """
    Return the given path, respecting environment variables.

    This should really be taken from dbt itself so that we can piggyback off
    of its search hierarchy.

    :param path: The path explicitly passed in.
    :param env_var: The environment variable to check for the path.
    :param default: The default path to use if no other path is found.
    """
    path_ = path or os.environ.get(env_var) or default
    return pathlib.Path(path_)


def _version_callback(value: bool) -> None:
    """
    Print the version of the package and exit.
    """
    if value:
        print(_DISTRIBUTION_METADATA["version"])
        raise typer.Exit()


def main(
    project_dir: Annotated[str, typer.Option()] = None,
    profiles_dir: Annotated[str, typer.Option()] = None,
    badge_path: Annotated[str, typer.Option()] = "coverage-dbt.svg",
    compile_dbt: Annotated[bool, typer.Option("--compile-dbt")] = False,
    cov_report: Annotated[bool, typer.Option("--cov-report")] = False,
    version: Annotated[bool, typer.Option("--version", callback=_version_callback, is_eager=True)] = None,  # noqa
) -> None:
    """
    Generate the code coverage for the dbt project and write it (as an SVG)
    to ``badge_path``.

    :param project_dir: The directory containing the ``dbt_project.yml``
        file.
    :param profiles_dir: The directory containing the ``profiles.yml`` file.
    :param badge_path: The file path to generate the badge to.
    :param compile_dbt: Whether to compile the dbt project before generating
        the code coverage, defaults to ``False``.
    :param cov_report: Whether to print the coverage report to stdout,
        defaults to ``False``.
    :param version: The version of the package.
    """
    project_dir_ = _get_path(project_dir, "DBT_PROJECT_DIR", ".")
    profiles_dir_ = _get_path(profiles_dir, "DBT_PROFILES_DIR", ".")

    if compile_dbt:
        subprocess.run(["dbt", "compile", f"--project-dir={project_dir_}", f"--profiles-dir={profiles_dir_}"])

    coverage_metric = compute_test_coverage(
        project_dir=project_dir_,
        cov_report=cov_report,
    )
    generate_badge(
        badge_path=pathlib.Path(badge_path).resolve(),
        coverage=coverage_metric,
    )
