# coding: utf-8
import sys
import multiprocessing 
import os
import numpy as np


param =sys.argv
n=param[1]
m=param[2]
MDset=param[3]
repeat=int(param[4])



os.chdir("./md1")
os.system("python2.7 ../system/calcCONF_molcharge.py "+n+" "+m+" "+MDset )
os.system("python2.7 ../system/mmpbsa_conf_writing.py "+n+" "+m)
os.chdir("..")


if repeat == 3:
    os.chdir("./md2")
    os.system("python2.7 ../system/calcCONF_molcharge.py "+n+" "+m+" "+MDset )
    os.system("python2.7 ../system/mmpbsa_conf_writing.py "+n+" "+m)
    os.chdir("..")

    os.chdir("./md3")
    os.system("python2.7 ../system/calcCONF_molcharge.py "+n+" "+m+" "+MDset )
    os.system("python2.7 ../system/mmpbsa_conf_writing.py "+n+" "+m)
    os.chdir("..")

    
else:
    pass

