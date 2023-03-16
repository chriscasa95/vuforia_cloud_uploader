# Vuforia Cloud Uploader

Vuforia Cloud Uploader is a CLI programm to upload images to targentmanager for Vufora cloud. The progam is using the the custom [VWS authentication](https://library.vuforia.com/web-api/vuforia-web-api-authentication#vws-authentication).


Functions:

- Upload image.
- Upload images extracted from a given video.
- Upload images from given folder.

See [vuforia_uploader.py](./vuforia_uploader.py) for deatailed CLI description an capabilities.

## CLI .exe usage example for uploading images

show help:

    .\vuforia_uploader.exe upload image --help

upload images (with powershell):

    .\vuforia_uploader.exe upload image `
        -p ./data/IMG_20221206_141113.jpg `
        -ak eb861e363ecf1563a824b290dd2e32b633d9d7b3 `
        -sk 0aba77815d86e9861597d6226b4c2f70493891db `
        -n TestBild `
        -w 5.0 `
        -m ./data/metadata.json


## Installation

Install `virtualenv`

    pip install virtualenv

Create enviroment called `venv`

    python -m venv venv

Activate the enviroment:

    # Windows
    ./venv/Scripts/activate

    # Linux
    source ./venv/bin/activate

Install python libs

    pip install -r requirements.txt

### Ubuntu WSL

Install OpenCV dependencies:

    apt-get update && apt-get install -y python3-opencv

### Windows Powershell

Set powershell modes for python venv execution:     
    
    # forbid .ps1 execution 
    Set-ExecutionPolicy Restricted -force 
    
    # allow .ps1 execution 
    Set-ExecutionPolicy Unrestricted -force 

## Build executables

Install [pyinstaller](https://pyinstaller.org/en/stable/).

CLI:

    pyinstaller --onefile vuforia_uploader.py