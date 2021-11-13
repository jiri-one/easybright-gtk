#!/bin/python

from os import system
from pathlib import Path

easybright_main_file = str(Path(__file__).parent / "easybright.py")

system(f"python {easybright_main_file}")
