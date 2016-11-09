# coding: utf-8


import sys
import os
import shutil




param =sys.argv
n=int(param[1])
m=int(param[2])
MDset=param[3]
repeat=int(param[4])
receptor=param[5]



#情報収集フェイズ
f=open("./md1/cfiles/"+MDset+"/pbsa_info")
x=f.readlines()
start= str(x[0].split()[-1])
stop= str(x[1].split()[-1])
inter= str(x[2].split()[-1])
snaps= str(x[3].split()[-1])

f2=open("./md1/input_info/"+receptor+"/info")
x2=f2.readlines()
Lig=str(x2[0].split()[-1])
Pro=str(x2[1].split()[-1])





os.chdir("./md1")
os.system("../system/prepMMPBSA1tra.sh "+str(n)+" "+str(m)+" "+start+" "+stop+" "+inter+" "+snaps+" "+Pro+" "+Lig)
os.chdir("..")




if repeat == 3:
    os.chdir("./md2")
    os.system("../system/prepMMPBSA1tra.sh "+str(n)+" "+str(m)+" "+start+" "+stop+" "+inter+" "+snaps+" "+Pro+" "+Lig)
    os.chdir("..")

    os.chdir("./md3")
    os.system("../system/prepMMPBSA1tra.sh "+str(n)+" "+str(m)+" "+start+" "+stop+" "+inter+" "+snaps+" "+Pro+" "+Lig)
    os.chdir("..")
else:
    pass




