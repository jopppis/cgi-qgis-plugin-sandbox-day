"""Initialize the plugin package."""

import os
from typing import TYPE_CHECKING

from cgiqgispluginsandboxday.plugin import Plugin
from cgiqgispluginsandboxday.qgis_plugin_tools.infrastructure.debugging import (
    setup_debugpy,
    setup_ptvsd,
    setup_pydevd,
)

if TYPE_CHECKING:
    from qgis.gui import QgisInterface

debugger = os.environ.get("QGIS_PLUGIN_USE_DEBUGGER", "").lower()
if debugger == "debugpy":
    setup_debugpy()
elif debugger == "ptvsd":
    setup_ptvsd()
elif debugger == "pydevd":
    setup_pydevd()


def classFactory(iface: "QgisInterface") -> Plugin:  # noqa: N802
    """Plugin class factory."""
    return Plugin()
