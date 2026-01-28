"""Dock widget for the plugin."""

from __future__ import annotations

from qgis.core import QgsProject, QgsRasterLayer, QgsVectorLayer
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QCloseEvent
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QDockWidget,
    QLabel,
    QVBoxLayout,
    QWidget,
)
from qgis.utils import iface

# Define available layers with name and URL
AVAILABLE_LAYERS = [
    {
        "name": "OpenStreetMap",
        "url": "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "provider": "wms",
        "type": "raster",
    },
    {
        "name": "Google Satellite",
        "url": "type=xyz&url=https://mt1.google.com/vt/lyrs%3Ds%26x%3D{x}%26y%3D{y}%26z%3D{z}",
        "provider": "wms",
        "type": "raster",
    },
    {
        "name": "Google Terrain",
        "url": "type=xyz&url=https://mt1.google.com/vt/lyrs%3Dp%26x%3D{x}%26y%3D{y}%26z%3D{z}",
        "provider": "wms",
        "type": "raster",
    },
    {
        "name": "CGI Offices",
        "url": "https://raw.githubusercontent.com/jopppis/cgi-office-locations/main/offices-finland.geojson",
        "provider": "ogr",
        "type": "vector",
    },
]


class LayerSelectorWidget(QDockWidget):
    """Layer selector dock widget for the plugin."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the dock widget."""
        super().__init__("Layer Selector", parent)

        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        # Add a header label
        self.label = QLabel("Select layers to add to map:")
        self.main_layout.addWidget(self.label)

        # Create checkboxes for each available layer
        self.layer_checkboxes: dict[str, QCheckBox] = {}
        for layer_info in AVAILABLE_LAYERS:
            checkbox = QCheckBox(layer_info["name"])
            checkbox.stateChanged.connect(
                lambda state, info=layer_info: self._on_layer_checkbox_changed(
                    state, info
                )
            )
            self.layer_checkboxes[layer_info["name"]] = checkbox
            self.main_layout.addWidget(checkbox)

        # Add stretch to push content to top
        self.main_layout.addStretch()

        self.setWidget(self.main_widget)

        # Connect to project layer signals to sync checkbox state
        QgsProject.instance().layerRemoved.connect(self._on_layer_removed)
        QgsProject.instance().layersAdded.connect(self._on_layers_added)

        # Initialize checkbox states based on current project layers
        self._sync_checkboxes_with_project()

    def _on_layer_checkbox_changed(self, state: int, layer_info: dict) -> None:
        """Handle checkbox state change to add/remove layer."""
        layer_name = layer_info["name"]

        if state == Qt.Checked:
            # Check if layer already exists in project
            existing_layers = QgsProject.instance().mapLayersByName(layer_name)
            if not existing_layers:
                # Add the layer
                if layer_info.get("type") == "vector":
                    layer = QgsVectorLayer(
                        layer_info["url"], layer_name, layer_info["provider"]
                    )
                else:
                    layer = QgsRasterLayer(
                        layer_info["url"], layer_name, layer_info["provider"]
                    )

                if layer.isValid():
                    QgsProject.instance().addMapLayer(layer)
        else:  # Qt.Unchecked
            # Remove layer if it exists
            existing_layers = QgsProject.instance().mapLayersByName(layer_name)
            for layer in existing_layers:
                QgsProject.instance().removeMapLayer(layer.id())
            # Refresh map canvas to update the display
            iface.mapCanvas().refresh()

    def _on_layer_removed(self, layer_id: str) -> None:
        """Handle layer removal from project - uncheck corresponding checkbox."""
        # We need to check all checkboxes since we only get the layer ID
        self._sync_checkboxes_with_project()

    def _on_layers_added(self, layers: list) -> None:
        """Handle layers added to project - check corresponding checkboxes."""
        self._sync_checkboxes_with_project()

    def _sync_checkboxes_with_project(self) -> None:
        """Sync checkbox states with current project layers."""
        for layer_name, checkbox in self.layer_checkboxes.items():
            existing_layers = QgsProject.instance().mapLayersByName(layer_name)
            # Block signals to prevent triggering add/remove when syncing
            checkbox.blockSignals(True)
            checkbox.setChecked(len(existing_layers) > 0)
            checkbox.blockSignals(False)

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        """Clean up signal connections when widget is closed."""
        try:
            QgsProject.instance().layerRemoved.disconnect(self._on_layer_removed)
            QgsProject.instance().layersAdded.disconnect(self._on_layers_added)
        except TypeError:
            # Signals may already be disconnected
            pass
        super().closeEvent(event)
