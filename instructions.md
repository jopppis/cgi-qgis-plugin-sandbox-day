# QGIS Sandbox day

## Introduction

In this even we take a dive into QGIS plugin development and build a small plugin that will help to understand the QGIS plugin development process and provide a skeleton for bulding something more exciting.

The main branch of this repository is meant to be a starting point that contains all the necessities required before actual plugin development can start. You could copy it to a new repository and start building your own plugin on top of it although there are more extensive templates out there (from where I cherry picked things here) like https://github.com/GispoCoding/cookiecutter-qgis-plugin and https://github.com/kartoza/qgis-plugin-template.

First thing to do is to set up the development environment using the instructions in the `README.md`.

We start by building a plugin that lets users to pick coordinates from the map (layer of their liking) and then generate a route between the coordinates using CGI Navici APIs. This plugin should familiarize you with concepts like:

- Working with QGIS map canvas and layers
- Building UI with Qt
- Working with external APIs in QGIS

You are free to start building in any way you prefer but for those that like bit more guidance, there is a git branch called `example` implements the aforementioned plugin in steps. You can check the commits for instance from https://github.com/jopppis/cgi-qgis-plugin-sandbox-day/commits/example/.

Each of the commit will append instructions to this file.

## Step 1: Add dock widget to UI

We want to make it easy for the users to interact with our plugin so we add a nice widget to the UI.

This consits of two main steps:
1. Add `dock_widget.py` file where we define the widget and its UI.
2. Add the widget from the file to the UI using main plugin file `plugin.py`.

We also add a button to toggle the visibility of the widget to the toolbar.

## Step 2: Convert the empty widget to layer selector widget

We want to start doing something useful with our plugin so we make the widget to something nice. In order to look at nice maps we need some layers and it is much more fun to implement layer selector yourself than use pre-made things.

When we add the elements to the UI we need to also add logic that does things when user interacts with the UI. This is usually done using signals and slots in Qt. In our case we add handlers to add new layers when user ticks checkboxes and remove layers when user unticks them or removes the layers from the layer tree.

## Step 3: Add company propaganda to the mix

In case you wonder how far away is some company offices, we should add them to the map so that we can get the route to them later on. I scraped the company offices in Finland and put them up in https://raw.githubusercontent.com/jopppis/cgi-office-locations/main/offices-finland.geojson. The GeoJSON contains the locations in ETRS-TM35FIN (EPSG:3067) coordinate reference system. We need to modify layer loading a little since this information is in vector format while the existing layers were raster layers.

This should had actually been a some more fun GIS service like OGC API features but I did not have time to implement it so we go with GeoJSON.

## Step 4: Add routing widget with basic geocoding functionality

Now we have the data on map and we can start building the routing part. We start by adding a new widget to the UI that will in time contain the routing functionality. As a stepping stone for the routing we add a geocoding to convert addresses to coordinates. This is done using CGI Navici service. You can find some information on Navici APIs from `navici_apit_v1.md` file.

Here we need to bit of work to make sure the API calls are done right and that the responses are parsed correctly.
