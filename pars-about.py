#!/usr/bin/python3

import sys
import os

local_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if os.path.exists(local_src):
    sys.path.insert(0, local_src)
else:
    sys.path.insert(0, "/usr/share/pars/pars-about/src")

import Main
