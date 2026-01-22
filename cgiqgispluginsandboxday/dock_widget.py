"""Dock widget for the plugin."""

from __future__ import annotations

from qgis.PyQt.QtWidgets import QDockWidget, QLabel, QVBoxLayout, QWidget


class PluginDockWidget(QDockWidget):
    """Main dock widget for the plugin."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the dock widget."""
        super().__init__("CGI Plugin Sandbox Day", parent)

        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        # Add a placeholder label
        self.label = QLabel("CGI QGIS Plugin Sandbox Day")
        self.main_layout.addWidget(self.label)

        # Add stretch to push content to top
        self.main_layout.addStretch()

        self.setWidget(self.main_widget)
