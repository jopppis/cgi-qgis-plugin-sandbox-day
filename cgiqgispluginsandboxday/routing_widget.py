"""Routing dock widget for the plugin."""

from __future__ import annotations

import json
import os
from typing import Optional

from qgis.core import QgsNetworkAccessManager, QgsPointXY
from qgis.PyQt.QtCore import QUrl, QUrlQuery
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest
from qgis.PyQt.QtWidgets import (
    QDockWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class RoutingWidget(QDockWidget):
    """Routing dock widget for the plugin."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the dock widget."""
        super().__init__("Routing", parent)

        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        # Origin Address
        self.main_layout.addWidget(QLabel("Origin Address:"))
        self.origin_input = QLineEdit()
        self.origin_input.setText("Karvaamokuja 2C, Helsinki")
        self.main_layout.addWidget(self.origin_input)

        self.origin_coords_label = QLabel("Coordinates: -")
        self.main_layout.addWidget(self.origin_coords_label)

        # Destination Address
        self.main_layout.addWidget(QLabel("Destination Address:"))
        self.dest_input = QLineEdit()
        self.dest_input.setText("Mannerheimintie 1, Helsinki")
        self.main_layout.addWidget(self.dest_input)

        self.dest_coords_label = QLabel("Coordinates: -")
        self.main_layout.addWidget(self.dest_coords_label)

        # Get coordinates Button
        self.get_coords_btn = QPushButton("Get coordinates")
        self.get_coords_btn.clicked.connect(self.geocode_addresses)
        self.main_layout.addWidget(self.get_coords_btn)

        # Status/Log Output
        self.main_layout.addWidget(QLabel("Status:"))
        self.status_text = QLabel("")
        self.status_text.setWordWrap(True)
        self.main_layout.addWidget(self.status_text)

        # Store coordinates for the routing
        self.origin_coords: Optional[QgsPointXY] = None
        self.dest_coords: Optional[QgsPointXY] = None

        # Add stretch
        self.main_layout.addStretch()

        self.setWidget(self.main_widget)

    def geocode_addresses(self) -> None:
        """Geocode the origin and destination addresses."""
        origin = self.origin_input.text()
        destination = self.dest_input.text()
        api_key = os.environ.get("NAVICI_API_KEY", "")

        if not api_key:
            self.status_text.setText(
                "Please set the NAVICI_API_KEY environment variable."
            )
            return

        if not origin or not destination:
            self.status_text.setText("Please fill in all fields.")
            return

        self.status_text.setText("Geocoding addresses...")
        self.origin_coords_label.setText("Coordinates: -")
        self.dest_coords_label.setText("Coordinates: -")

        # Geocode Origin
        self._geocode(origin, api_key, "Origin")
        # Geocode Destination
        self._geocode(destination, api_key, "Destination")

    def _geocode(self, address: str, api_key: str, label: str) -> None:
        """Helper to geocode a single address."""
        base_url = "https://mapservices.navici.com/geocoding/geocode"
        query = QUrlQuery()
        query.addQueryItem("address", address)
        query.addQueryItem("crs", "EPSG:3067")
        query.addQueryItem("lang", "fi")
        query.addQueryItem("source", "digiroadAddress|vrkAddress")
        query.addQueryItem("limit", "5")
        query.addQueryItem("apikey", api_key)

        url = QUrl(base_url)
        url.setQuery(query)

        request = QNetworkRequest(url)

        reply = QgsNetworkAccessManager.instance().get(request)
        reply.finished.connect(lambda: self._handle_geocode_response(reply, label))

    def _handle_geocode_response(self, reply: QNetworkReply, label: str) -> None:
        """Handle the geocoding API response."""
        if reply.error() != QNetworkReply.NoError:
            self.status_text.setText(f"{label} Error: {reply.errorString()}")
            return

        try:
            data = json.loads(reply.readAll().data())
            # Basic validation of response structure; adjust based on actual API response
            if isinstance(data, dict) and "features" in data:
                features = data["features"]
                if len(features) > 0:
                    first_result = features[0]

                    if (
                        "geometry" in first_result
                        and "coordinates" in first_result["geometry"]
                    ):
                        coords = first_result["geometry"]["coordinates"]
                        coord_str = f"{coords[0]}, {coords[1]}"
                        if label == "Origin":
                            self.origin_coords = QgsPointXY(coords[0], coords[1])
                            self.origin_coords_label.setText(
                                f"Coordinates: {coord_str}"
                            )
                        elif label == "Destination":
                            self.dest_coords = QgsPointXY(coords[0], coords[1])
                            self.dest_coords_label.setText(f"Coordinates: {coord_str}")

                        self.status_text.setText("")
                else:
                    self.status_text.setText(
                        f"{label}: No results found (empty features)."
                    )
            else:
                self.status_text.setText(f"{label}: No results found.")

        except json.JSONDecodeError:
            self.status_text.setText(f"{label}: Failed to decode JSON response.")
        except Exception as e:
            self.status_text.setText(f"{label} Exception: {e!s}")
