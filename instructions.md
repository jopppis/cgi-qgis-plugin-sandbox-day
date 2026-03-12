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
