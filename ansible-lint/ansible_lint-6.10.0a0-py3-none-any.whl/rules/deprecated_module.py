"""Implementation of deprecated-module rule."""
# Copyright (c) 2018, Ansible Project

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ansiblelint.rules import AnsibleLintRule

if TYPE_CHECKING:
    from ansiblelint.file_utils import Lintable


class DeprecatedModuleRule(AnsibleLintRule):
    """Deprecated module."""

    id = "deprecated-module"
    description = (
        "These are deprecated modules, some modules are kept "
        "temporarily for backwards compatibility but usage is discouraged."
    )
    link = "https://docs.ansible.com/ansible/latest/collections/index_module.html"
    severity = "HIGH"
    tags = ["deprecations"]
    version_added = "v4.0.0"

    _modules = [
        # spell-checker:disable
        "accelerate",
        "aos_asn_pool",
        "aos_blueprint",
        "aos_blueprint_param",
        "aos_blueprint_virtnet",
        "aos_device",
        "aos_external_router",
        "aos_ip_pool",
        "aos_logical_device",
        "aos_logical_device_map",
        "aos_login",
        "aos_rack_type",
        "aos_template",
        "azure",
        "cl_bond",
        "cl_bridge",
        "cl_img_install",
        "cl_interface",
        "cl_interface_policy",
        "cl_license",
        "cl_ports",
        "cs_nic",
        "docker",
        "ec2_ami_find",
        "ec2_ami_search",
        "ec2_remote_facts",
        "ec2_vpc",
        "kubernetes",
        "netscaler",
        "nxos_ip_interface",
        "nxos_mtu",
        "nxos_portchannel",
        "nxos_switchport",
        "oc",
        "panos_nat_policy",
        "panos_security_policy",
        "vsphere_guest",
        "win_msi",
        "include",
        # spell-checker:enable
    ]

    def matchtask(
        self, task: dict[str, Any], file: Lintable | None = None
    ) -> bool | str:
        module = task["action"]["__ansible_module__"]
        if module in self._modules:
            message = "{0} {1}"
            return message.format(self.shortdesc, module)
        return False
