"""Routing dock widget for the plugin."""

from __future__ import annotations

import json
import os
from typing import Optional

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsNetworkAccessManager,
    QgsPointXY,
    QgsProject,
)
from qgis.gui import QgsMapToolEmitPoint
from qgis.PyQt.QtCore import QUrl, QUrlQuery
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest
from qgis.PyQt.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from qgis.utils import iface


class RoutingWidget(QDockWidget):
    """Routing dock widget for the plugin."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the dock widget."""
        super().__init__("Routing", parent)

        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        # Map tool for picking points
        self.map_tool = QgsMapToolEmitPoint(iface.mapCanvas())
        self.map_tool.canvasClicked.connect(self.handle_map_click)
        self.picking_mode: str | None = None  # "origin" or "destination"

        # Origin Address
        self.main_layout.addWidget(QLabel("Origin Address:"))
        origin_layout = QHBoxLayout()
        self.origin_input = QLineEdit()
        self.origin_input.setText("Karvaamokuja 2C, Helsinki")
        origin_layout.addWidget(self.origin_input)

        self.pick_origin_btn = QPushButton("From map")
        self.pick_origin_btn.setFixedWidth(80)
        self.pick_origin_btn.clicked.connect(lambda: self.activate_picker("origin"))
        origin_layout.addWidget(self.pick_origin_btn)
        self.main_layout.addLayout(origin_layout)

        self.origin_coords_label = QLabel("Coordinates: -")
        self.main_layout.addWidget(self.origin_coords_label)

        # Destination Address
        self.main_layout.addWidget(QLabel("Destination Address:"))
        dest_layout = QHBoxLayout()
        self.dest_input = QLineEdit()
        self.dest_input.setText("Mannerheimintie 1, Helsinki")
        dest_layout.addWidget(self.dest_input)

        self.pick_dest_btn = QPushButton("From map")
        self.pick_dest_btn.setFixedWidth(80)
        self.pick_dest_btn.clicked.connect(lambda: self.activate_picker("destination"))
        dest_layout.addWidget(self.pick_dest_btn)
        self.main_layout.addLayout(dest_layout)

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

    def activate_picker(self, mode: str) -> None:
        """Activate the map picker tool."""
        self.picking_mode = mode
        iface.mapCanvas().setMapTool(self.map_tool)
        self.status_text.setText(f"Click on map to select {mode}...")

    def handle_map_click(self, point: QgsPointXY, button: int) -> None:
        """Handle click on map."""
        _ = button  # Unused
        if not self.picking_mode:
            return

        api_key = os.environ.get("NAVICI_API_KEY", "")
        if not api_key:
            self.status_text.setText("Please set API Key first.")
            iface.mapCanvas().unsetMapTool(self.map_tool)
            self.picking_mode = None
            return

        source_crs = iface.mapCanvas().mapSettings().destinationCrs()
        target_crs = QgsCoordinateReferenceSystem("EPSG:3067")

        tr = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())
        point_3067 = tr.transform(point)

        # Display coordinates
        coord_str = f"{point_3067.x():.2f}, {point_3067.y():.2f}"
        if self.picking_mode == "origin":
            self.origin_coords_label.setText(f"Coordinates: {coord_str}")
            self.origin_coords = point_3067
        elif self.picking_mode == "destination":
            self.dest_coords_label.setText(f"Coordinates: {coord_str}")
            self.dest_coords = point_3067

        self.status_text.setText("Fetching address...")

        # Reverse Geocode
        mode = self.picking_mode
        self.picking_mode = (
            None  # Reset picking mode immediately after getting the point
        )
        self._reverse_geocode(point_3067.x(), point_3067.y(), api_key, mode)

        # Reset tool
        iface.mapCanvas().unsetMapTool(self.map_tool)

    def _reverse_geocode(self, x: float, y: float, api_key: str, mode: str) -> None:
        """Reverse geocode coordinates."""
        base_url = "https://mapservices.navici.com/geocoding/reverse"
        query = QUrlQuery()
        query.addQueryItem("x", str(x))
        query.addQueryItem("y", str(y))
        query.addQueryItem("to", "EPSG:3067")
        query.addQueryItem("from", "EPSG:3067")
        query.addQueryItem("lang", "fi")
        query.addQueryItem("limit", "1")
        query.addQueryItem("maxdistance", "100")
        query.addQueryItem("mmlFilter", "48111,48112,48120")
        query.addQueryItem("offset", "0")
        query.addQueryItem("source", "osmPlace,vrkAddress")
        query.addQueryItem("type", "address")
        query.addQueryItem("apikey", api_key)

        url = QUrl(base_url)
        url.setQuery(query)

        request = QNetworkRequest(url)
        reply = QgsNetworkAccessManager.instance().get(request)
        reply.finished.connect(
            lambda: self._handle_reverse_geocode_response(reply, mode)
        )

    def _handle_reverse_geocode_response(self, reply: QNetworkReply, mode: str) -> None:
        """Handle the reverse geocoding API response."""
        if reply.error() != QNetworkReply.NoError:
            self.status_text.setText(f"Reverse Geocode Error: {reply.errorString()}")
            return

        try:
            data = json.loads(reply.readAll().data())
            # Parse GeoJSON FeatureCollection
            if (
                isinstance(data, dict)
                and "features" in data
                and len(data["features"]) > 0
            ):
                features = data["features"]
                first_feature = features[0]
                properties = first_feature.get("properties", {})

                address = (
                    properties.get("label")
                    or properties.get("name")
                    or "Unknown Address"
                )

                self.status_text.setText("Address found.")

                if mode == "origin":
                    self.origin_input.setText(address)
                elif mode == "destination":
                    self.dest_input.setText(address)
            else:
                self.status_text.setText("No address found.")
                if mode == "origin":
                    self.origin_input.setText("")
                elif mode == "destination":
                    self.dest_input.setText("")

        except json.JSONDecodeError:
            self.status_text.setText("Failed to decode response.")
        except Exception as e:
            self.status_text.setText(f"Exception: {e!s}")

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
