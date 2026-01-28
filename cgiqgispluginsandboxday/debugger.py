"""Plugin setup."""

import os
import sys
from pathlib import Path

from cgiqgispluginsandboxday.logger import get_logger

logger = get_logger()


def _get_interpreter_path() -> str:
    """Get the path to the current python interpreter as string.

    QGIS macos does return some weird path to
    /Applications/QGIS.app/Contents/MacOS/QGIS from sys.executable. This
    function tries to get the correct path to the actual python interpreter.

    Alternatively the path can be fixed by setting PYTHONEXECUTABLE env variable
    in the QGIS settings to the correct path (e.g
    /Applications/QGIS.app/Contents/MacOS/bin/python3).
    """
    if sys.platform == "darwin":
        return str(Path(sys.executable).parent / "python3")

    return sys.executable


def setup_debugger() -> None:
    """Setup debugger."""
    if os.environ.get("QGIS_DEBUGPY_HAS_LOADED") == "1":
        return

    if os.environ.get("QGIS_PLUGIN_USE_DEBUGGER") == "debugpy":
        logger.info("Creating debugpy debugger")
        try:
            import debugpy  # noqa: PLC0415

            debugpy.configure(python=_get_interpreter_path())
            debugpy.listen(("localhost", 5678))
        except Exception:
            logger.exception("Unable to create debugpy debugger")
        else:
            os.environ["QGIS_DEBUGPY_HAS_LOADED"] = "1"
    elif os.environ.get("QGIS_PLUGIN_USE_DEBUGGER") == "pydevd_pycharm":
        logger.info("Creating pycharm debugger")
        try:
            import pydevd_pycharm  # noqa: PLC0415

            port = os.environ.get("QGIS_PLUGIN_DEBUGGER_PORT")
            debugger_port = int(port) if port is not None else 5678
            pydevd_pycharm.settrace(
                "localhost",
                port=debugger_port,
                stdoutToServer=True,
                stderrToServer=True,
                suspend=False,
            )
        except Exception:
            logger.exception("Unable to use pydevd_pycharm debugger")
