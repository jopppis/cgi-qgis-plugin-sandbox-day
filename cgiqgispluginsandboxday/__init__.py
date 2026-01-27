"""Initialize the plugin package."""

from qgis.gui import QgisInterface

from cgiqgispluginsandboxday.debugger import setup_debugger
from cgiqgispluginsandboxday.logger import get_logger
from cgiqgispluginsandboxday.plugin import Plugin

logger = get_logger()

setup_debugger()


def classFactory(iface: "QgisInterface") -> Plugin:  # noqa: N802
    """Plugin class factory."""
    return Plugin()
