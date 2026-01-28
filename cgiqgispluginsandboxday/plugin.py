"""Plugin setup."""

from __future__ import annotations

from collections.abc import Callable

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QToolBar, QWidget
from qgis.utils import iface

from cgiqgispluginsandboxday.constants import PLUGIN_NAME
from cgiqgispluginsandboxday.layer_selector_widget import LayerSelectorWidget
from cgiqgispluginsandboxday.logger import remove_logger
from cgiqgispluginsandboxday.routing_widget import RoutingWidget


class Plugin:
    """QGIS Plugin Implementation."""

    name = PLUGIN_NAME

    def __init__(self) -> None:
        """Initialize the plugin."""
        self.actions: list[QAction] = []
        self.menu = Plugin.name

        # Dictionary to store dock widgets by name for easy expansion
        self.dock_widgets: dict[str, QWidget] = {}

        # Create plugin toolbar
        self.toolbar: QToolBar = iface.addToolBar(Plugin.name)
        self.toolbar.setObjectName(Plugin.name)

    def add_action(
        self,
        icon_path: str,
        text: str,
        callback: Callable,
        *,
        enabled_flag: bool = True,
        add_to_menu: bool = True,
        add_to_toolbar: bool = True,
        status_tip: str | None = None,
        whats_this: str | None = None,
        parent: QWidget | None = None,
    ) -> QAction:
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.

        :param text: Text that should be shown in menu items for this action.

        :param callback: Function to be called when the action is triggered.

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.

        :param parent: Parent widget for the new action. Defaults None.

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to plugin's own toolbar
            self.toolbar.addAction(action)

        if add_to_menu:
            iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self) -> None:  # noqa N802
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # Layer Selector action
        self.add_action(
            ":/images/themes/default/mActionAddLayer.svg",
            text="Layer Selector",
            callback=self.toggle_layer_selector,
            parent=iface.mainWindow(),
            add_to_toolbar=True,
        )

        # Routing Widget action
        self.add_action(
            ":/images/themes/default/mIconLineLayer.svg",
            text="Routing",
            callback=self.toggle_routing_widget,
            parent=iface.mainWindow(),
            add_to_toolbar=True,
        )

    def onClosePlugin(self) -> None:  # noqa N802
        """Cleanup necessary items here when plugin dockwidget is closed."""

    def unload(self) -> None:
        """Remove the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            iface.removePluginMenu(Plugin.name, action)

        # Remove toolbar
        if self.toolbar is not None:
            del self.toolbar

        # Clean up all dock widgets
        for widget in self.dock_widgets.values():
            if widget is not None:
                iface.removeDockWidget(widget)
                widget.deleteLater()
        self.dock_widgets.clear()

        remove_logger()

    def toggle_layer_selector(self) -> None:
        """Toggle the Layer Selector dock widget."""
        self._toggle_dock_widget(
            "layer_selector",
            lambda: LayerSelectorWidget(iface.mainWindow()),
            Qt.RightDockWidgetArea,
        )

    def toggle_routing_widget(self) -> None:
        """Toggle the Routing dock widget."""
        self._toggle_dock_widget(
            "routing",
            lambda: RoutingWidget(iface.mainWindow()),
            Qt.RightDockWidgetArea,
        )

    def _toggle_dock_widget(
        self,
        widget_name: str,
        widget_factory: Callable[[], QWidget],
        dock_area: Qt.DockWidgetArea,
    ) -> None:
        """Toggle a dock widget's visibility, creating it if necessary.

        :param widget_name: Unique name for the widget in the dock_widgets dict.
        :param widget_factory: Callable that creates the widget instance.
        :param dock_area: Qt dock area where the widget should be placed.
        """
        widget = self.dock_widgets.get(widget_name)
        if widget is None:
            # Create the dock widget
            widget = widget_factory()
            self.dock_widgets[widget_name] = widget
            iface.addDockWidget(dock_area, widget)
        elif widget.isVisible():
            widget.hide()
        else:
            widget.show()
