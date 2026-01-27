# CGI QGIS Plugin Sandbox Day

## Introduction

In this sandbox day we get to try QGIS plugin development and build a small
plugin that will help to understand the QGIS plugin development process and
provide a skeleton for future plugins.

## Useful information

- [QGIS Python Developer Guide](https://docs.qgis.org/3.44/en/docs/pyqgis_developer_cookbook/index.html)
- Debugging/Development Tools -panel in QGIS

## Prerequisites

### Install Python
Only required on Macos. Install e.g. by Homebrew:

```bash
brew install python@3.12
```

### Install QGIS

#### Windows
Download OSGeo4W installer from https://qgis.org/download/ and install.

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

### Setup up virtual environment

On Windows run:
```console
python create_qgis_venv.py
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


### Start AI service

We connect QGIS to Segmentation AI service via a REST API. The service runs Meta's Segment Anything (SAM) model to segment images based on text prompts.

```bash
cd sam_service
python -m venv .venv # or maybe python3
source .venv/bin/activate # or on Windows .venv/Scripts/activate
pip install -r requirements.txt
fastapi dev main.py --port 8000
```

When the service is running you can access the documentation at http://localhost:8000/docs.

See [sam_service/README.md](sam_service/README.md) for more information.


## Development

### Testing the plugin on QGIS

A symbolic link / directory junction should be made to the directory containing the installed plugins pointing to the dev plugin package.

On Windows Command promt
```console
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

## Not covered in this excercise

We go over the basics of the plugin development but do not cover many important topics in production grade plugins, including but not limited to:

- Translations
- Testing
- Packaging & Deployment
- Backend services

## License
This plugin is distributed under the terms of the [GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.html) license.

See [LICENSE](LICENSE) for more information.
