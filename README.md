# CGI QGIS Plugin Sandbox Day

## Introduction

In this sandbox day we get to try QGIS plugin development and build a small
plugin that will help to understand the QGIS plugin development process and
provide a skeleton for future plugins.

## Useful information

- [QGIS Python Developer Guide](https://docs.qgis.org/3.44/en/docs/pyqgis_developer_cookbook/index.html)
- Debugging/Development Tools -panel in QGIS

## Prerequisites

### Install QGIS

#### Windows
Download OSGeo4W installer from https://qgis.org/download/ and install.

Use express install method and select QGIS LTR and GDAL.

#### MacOS

Installing might be easiest via Homebrew (use LTR version):

```bash
brew install qgis@ltr
```

You can also download from https://qgis.org/downloads/macos/ltr/qgis_ltr_final-3_40_5_20250321_160709.dmg

Afterwards you might need to allow QGIS to run by going to `Settings - Privacy & Security - Security - QGIS - Allow Anyway` because Macos blocks unsigned applications and QGIS is not yet signed.

### Clone this repository

### Install QGIS plugin reloader
Open QGIS and go to `Plugins` - `Manage and Install Plugins`.

### Add NAVICI api key to QGIS

In order to use the Navici APIs we need API key. For this sandbox day you will be given an API key that you should configure in QGIS by going to `Preferences - System - Environment` and adding `NAVICI_API_KEY=<API_KEY>` to the environment variables (you can use e.g. Overwrite method in Apply).

### Setup up virtual environment

On Windows run:
```console
C:\Users\<username>\AppData\Local\Programs\OSGeo4W\bin\python-qgis-ltr.bat create_qgis_venv.py
```
Pick the installed OSGeo4W python version if available, and if not select Custom and enter `C:\Users\<username>\AppData\Local\Programs\OSGeo4W\apps\qgis-ltr`.

```console
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

On Linux run:
```console
python create_qgis_venv.py
source .venv\bin\activate
pip install -r requirements-dev.txt
```

On Macos run:
```console
python create_qgis_venv.py --python-executable /Applications/QGIS-LTR.app/Contents/MacOS/bin/python3
source .venv\bin\activate
pip install -r requirements-dev.txt
```

## Development

### Add the plugin on QGIS

A symbolic link / directory junction should be made to the directory containing the installed plugins pointing to the dev plugin package.

On Windows Command promt
```console
mkdir %AppData%\QGIS\QGIS3\profiles\default\python\plugins
mklink /J %AppData%\QGIS\QGIS3\profiles\default\python\plugins\cgiqgispluginsandboxday .\cgiqgispluginsandboxday
```

On Windows PowerShell
```console
New-Item -ItemType SymbolicLink -Path ${env:APPDATA}\QGIS\QGIS3\profiles\default\python\plugins\cgiqgispluginsandboxday -Value ${pwd}\cgiqgispluginsandboxday
```

On Linux
```console
ln -s cgiqgispluginsandboxday/ ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/cgiqgispluginsandboxday
```

On MacOS
```console
ln -s $(pwd)/cgiqgispluginsandboxday/ ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/cgiqgispluginsandboxday
```

After that you should be able to enable the plugin in the QGIS Plugin Manager.

### Debugging

The project includes `launch.json` file which can be used to debug the plugin in Visual Studio Code.

In order to use the debugger, you need to enable the debugging in QGIS by going to `Preferences - System - Environment` and adding `QGIS_PLUGIN_USE_DEBUGGER=debugpy` to the environment variables (you can use e.g. Overwrite method in Apply).

After restarting QGIS you should be able to start debugging from Visual Studio Code `Run and Debug` panel but take care to pick the configuration matching you OS.

You might need to install debugpy to the python installation by running:
```console
PIP_REQUIRE_VIRTUALENV=false /Applications/QGIS-LTR.app/Contents/MacOS/bin/python3 -m pip install debugpy
```
on the python installation you are using for QGIS.

## Not covered in this excercise

We go over the basics of the plugin development but do not cover many important topics in production grade plugins, including but not limited to:

- Translations
- Testing
- Packaging & Deployment
- Backend services
- UI design tools

## Esimerkkiplugineja

- Essi

## License
This plugin is distributed under the terms of the [GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.html) license.

See [LICENSE](LICENSE) for more information.
