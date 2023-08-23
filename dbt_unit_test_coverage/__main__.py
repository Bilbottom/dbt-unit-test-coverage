"""
Generate the code coverage for the dbt project.
"""
import importlib.metadata
import pathlib
import subprocess
from typing import Annotated

import typer

from dbt_unit_test_coverage.badge import generate_badge
from dbt_unit_test_coverage.coverage import compute_test_coverage

_DISTRIBUTION_METADATA = importlib.metadata.metadata("dbt_unit_test_coverage")


def _version_callback(value: bool) -> None:
    """
    Print the version of the package and exit.
    """
    if value:
        print(_DISTRIBUTION_METADATA["version"])
        raise typer.Exit()


def main(
    project_dir: Annotated[str, typer.Option()] = ".",
    profiles_dir: Annotated[str, typer.Option()] = ".",
    badge_path: Annotated[str, typer.Option()] = "coverage-dbt.svg",
    compile_dbt: Annotated[bool, typer.Option("--compile-dbt")] = False,
    cov_report: Annotated[bool, typer.Option("--cov-report")] = False,
    version: Annotated[bool, typer.Option("--version", callback=_version_callback, is_eager=True)] = None,
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
    if compile_dbt:
        subprocess.run(["dbt", "compile", f"--project-dir={project_dir}", f"--profiles-dir={profiles_dir}"])

    coverage_metric = compute_test_coverage(
        project_dir=pathlib.Path(project_dir),
        cov_report=cov_report,
    )
    generate_badge(
        badge_path=pathlib.Path(badge_path).resolve(),
        coverage=coverage_metric,
    )


app = lambda: typer.run(main)  # noqa
if __name__ == "__main__":
    app()
