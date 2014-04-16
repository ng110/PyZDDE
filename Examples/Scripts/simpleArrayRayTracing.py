#-------------------------------------------------------------------------------
# Name:        simpleArrayRayTracing.py
# Purpose:     Script for testing array ray tracing
#
# Author:      Indranil
#
# Created:     09/04/2014
# Copyright:   (c) Indranil 2014
# Licence:     MIT License
#-------------------------------------------------------------------------------
from __future__ import print_function

import sys
import matplotlib.pyplot as plt

import pyzdde.zdde as pyz
reload(pyz)

link0 = pyz.PyZDDE()
status = link0.zDDEInit()


if ~status:
    ret = link0.zGetVersion()
    print("Version: ", ret)
    ret = link0.zGetRefresh()
    ret = link0.zGetUpdate()
    try:
        link0.zArrayTrace()
    except:
        info = sys.exc_info()
        print("Error/msg: ", info[1])
link0.zDDEClose()