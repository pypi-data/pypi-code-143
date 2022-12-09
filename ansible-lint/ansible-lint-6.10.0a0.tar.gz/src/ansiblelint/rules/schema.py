"""Rule definition for JSON Schema Validations."""
from __future__ import annotations

import logging
import sys

from ansiblelint.errors import MatchError
from ansiblelint.file_utils import Lintable
from ansiblelint.rules import AnsibleLintRule
from ansiblelint.schemas import JSON_SCHEMAS, validate_file_schema

_logger = logging.getLogger(__name__)


DESCRIPTION_MD = """ Returned errors will not include exact line numbers, but they will mention
the schema name being used as a tag, like ``schema[playbook]``,
``schema[tasks]``.

This rule is not skippable and stops further processing of the file.

If incorrect schema was picked, you might want to either:

* move the file to standard location, so its file is detected correctly.
* use ``kinds:`` option in linter config to help it pick correct file type.
"""


class ValidateSchemaRule(AnsibleLintRule):
    """Perform JSON Schema Validation for known lintable kinds."""

    description = DESCRIPTION_MD

    id = "schema"
    severity = "VERY_HIGH"
    tags = ["core", "experimental"]
    version_added = "v6.1.0"

    def matchyaml(self, file: Lintable) -> list[MatchError]:
        """Return JSON validation errors found as a list of MatchError(s)."""
        result = []
        if file.kind not in JSON_SCHEMAS:
            return []

        errors = validate_file_schema(file)
        if errors:
            if errors[0].startswith("Failed to load YAML file"):
                _logger.debug(
                    "Ignored failure to load %s for schema validation, as !vault may cause it."
                )
                return []

            result.append(
                MatchError(
                    message=errors[0],
                    filename=file,
                    rule=ValidateSchemaRule(),
                    details=ValidateSchemaRule.description,
                    tag=f"schema[{file.kind}]",
                )
            )
        return result


# testing code to be loaded only with pytest or when executed the rule file
if "pytest" in sys.modules:
    import pytest

    # pylint: disable=ungrouped-imports
    from ansiblelint.config import options
    from ansiblelint.rules import RulesCollection
    from ansiblelint.runner import Runner

    @pytest.mark.parametrize(
        ("file", "expected_kind", "expected"),
        (
            (
                "examples/collection/galaxy.yml",
                "galaxy",
                ["'GPL' is not one of"],
            ),
            (
                "examples/roles/invalid_requirements_schema/meta/requirements.yml",
                "requirements",
                ["{'foo': 'bar'} is not valid under any of the given schemas"],
            ),
            (
                "examples/roles/invalid_meta_schema/meta/main.yml",
                "meta",
                ["False is not of type 'string'"],
            ),
            (
                "examples/playbooks/vars/invalid_vars_schema.yml",
                "vars",
                ["'123' does not match any of the regexes"],
            ),
            (
                "examples/execution-environment.yml",
                "execution-environment",
                [],
            ),
            (
                "examples/ee_broken/execution-environment.yml",
                "execution-environment",
                ["Additional properties are not allowed ('foo' was unexpected)"],
            ),
            ("examples/meta/runtime.yml", "meta-runtime", []),
            (
                "examples/broken_collection_meta_runtime/meta/runtime.yml",
                "meta-runtime",
                ["Additional properties are not allowed ('foo' was unexpected)"],
            ),
            (
                "examples/inventory/production.yml",
                "inventory",
                [],
            ),
            (
                "examples/inventory/broken_dev_inventory.yml",
                "inventory",
                ["Additional properties are not allowed ('foo' was unexpected)"],
            ),
            (
                ".ansible-lint",
                "ansible-lint-config",
                [],
            ),
            (
                "examples/.config/ansible-lint.yml",
                "ansible-lint-config",
                [],
            ),
            (
                "examples/broken/.ansible-lint",
                "ansible-lint-config",
                ["Additional properties are not allowed ('foo' was unexpected)"],
            ),
            (
                "examples/ansible-navigator.yml",
                "ansible-navigator-config",
                [],
            ),
            (
                "examples/broken/ansible-navigator.yml",
                "ansible-navigator-config",
                ["Additional properties are not allowed ('ansible' was unexpected)"],
            ),
            (
                "examples/roles/hello/meta/argument_specs.yml",
                "arg_specs",
                [],
            ),
            (
                "examples/roles/broken_argument_specs/meta/argument_specs.yml",
                "arg_specs",
                ["Additional properties are not allowed ('foo' was unexpected)"],
            ),
        ),
        ids=(
            # "playbook-fail",
            "galaxy",
            "requirements",
            "meta",
            "vars",
            "ee",
            "ee-broken",
            "meta-runtime",
            "meta-runtime-broken",
            "inventory",
            "inventory-broken",
            "lint-config",
            "lint-config2",
            "lint-config-broken",
            "navigator",
            "navigator-broken",
            "argspecs",
            "argspecs-broken",
        ),
    )
    def test_schema(file: str, expected_kind: str, expected: list[str]) -> None:
        """Validate parsing of ansible output."""
        lintable = Lintable(file)
        assert lintable.kind == expected_kind

        rules = RulesCollection(options=options)
        rules.register(ValidateSchemaRule())
        results = Runner(lintable, rules=rules).run()

        assert len(results) == len(expected), results
        for idx, result in enumerate(results):
            assert result.filename.endswith(file)
            assert expected[idx] in result.message
            assert result.tag == f"schema[{expected_kind}]"
