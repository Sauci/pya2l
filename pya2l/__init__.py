"""
@project: pya2l
@file: __init__.py
@author: Guillaume Sottas
@date: 13.04.2018
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))

from .cli import main
