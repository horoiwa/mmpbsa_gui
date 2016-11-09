# coding: utf-8


import sys
import os
import shutil




param = sys.argv
repeat= int(param[1])

if repeat == 3:
    shutil.copytree("md1","md2")
    shutil.copytree("md1","md3")
else:
    pass




