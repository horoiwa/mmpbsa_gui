# coding: utf-8


import sys
import os
import shutil




param = sys.argv
n=int(param[1])
m=int(param[2])
MDset=param[3]
repeat= int(param[4])

print n
print m
print MDset
print repeat

os.chdir("./md1")
os.system("./cfiles/"+MDset+"/md2.2.sh "+str(n)+" "+str(m)+" "+MDset)
os.chdir("..")




if repeat == 3:
    os.chdir("./md2")
    os.system("./cfiles/"+MDset+"/md2.2.sh "+str(n)+" "+str(m)+" "+MDset)
    os.chdir("..")

    os.chdir("./md3")
    os.system("./cfiles/"+MDset+"/md2.2.sh "+str(n)+" "+str(m)+" "+MDset)
    os.chdir("..")
else:
    pass




