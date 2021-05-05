__author__ = """Francesco Ranaudo"""
__email__ = 'francesco.ranaudo@gmail.com'
__version__ = '0.8.0'

import os
import json
from pathlib import Path
from .decorators import *


home = str(Path.home())

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))
DOCS = os.path.abspath(os.path.join(HOME, 'docs'))
TEMP = os.path.abspath(os.path.join(HOME, 'temp'))
SETTINGS = os.path.join(HERE, './settings.json')


with open(SETTINGS, 'r') as f:
    path = json.load(f)["tokens_path"]

# the default location is in ~/.tokens
if path == "None":
    TOKENS = os.path.join(Path.home(), ".tokens")
else:
    TOKENS = path

if not os.path.isdir(TOKENS):
    Path(TOKENS).mkdir(parents=True, exist_ok=True)
