"""
The ``dbt_project.yml`` file exposed as a dataclass.
"""

from __future__ import annotations

import dataclasses
import pathlib
from typing import TypeVar

import yaml

_T = TypeVar("_T")


def _deduplicate(items: list[_T]) -> list[_T]:
    """
    Return a list with duplicates removed.

    Note that this *will not* work on un-hashable types, and is not
    guaranteed to preserver item order.

    :param items: The list to deduplicate.

    :return: The deduplicated list.
    """
    return list(set(items))


@dataclasses.dataclass
class DbtConfig:
    name: str
    dbt_project_root: pathlib.Path
    model_paths: list[pathlib.Path]
    test_paths: list[pathlib.Path]
    target_path: pathlib.Path
    compiled_paths: list[pathlib.Path] = dataclasses.field(init=False)

    def __post_init__(self):
        # fmt: off
        self.compiled_paths = [
            self.target_path / "compiled" / self.name / model_path.relative_to(self.dbt_project_root)
            for model_path in self.model_paths
        ]
        # fmt: on

    @classmethod
    def from_root(cls, dbt_project_root: pathlib.Path) -> DbtConfig:
        """
        Construct a DbtConfig from the dbt project root.

        :param dbt_project_root: The directory where the ``dbt_project.yml``
            file lives.

        :return: A DbtConfig.
        """
        with (dbt_project_root / "dbt_project.yml").open() as config_yml:
            config = yaml.safe_load(config_yml)

        return DbtConfig(
            name=config["name"],
            dbt_project_root=dbt_project_root,
            model_paths=_deduplicate([dbt_project_root / p for p in config.get("model-paths", "models")]),
            test_paths=_deduplicate([dbt_project_root / p for p in config.get("test-paths", "tests")]),
            target_path=dbt_project_root / config.get("target-path", "target"),
        )
