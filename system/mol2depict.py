# coding: utf-8

from openeye.oechem import *
from openeye.oedepict import *
import os
import sys

param=sys.argv
n=int(param[1])
m=int(param[2])

while n < m +1:
    DXX= "D0"+str(n) if n<10 else "D"+str(n)
    
    if os.path.exists("./md1/structs/"+DXX+".mol2"):
        os.system('babel -imol2 ./md1/structs/'+DXX+'.mol2 -osmi ./RESULT/'+DXX+"/"+DXX+".smi")
        
        os.chdir("./RESULT/"+DXX)
        f=open("./"+DXX+".smi","r")
        smi= f.readlines()[0].split()[0]
        
        mol = OEGraphMol()
        OESmilesToMol(mol, smi+ " "+DXX+".mol2")
        OEPrepareDepiction(mol)

        width, height = 300, 300
        opts = OE2DMolDisplayOptions(width, height, OEScale_AutoScale)
        disp = OE2DMolDisplay(mol, opts)
        OERenderMolecule( DXX+".png", disp)
        
        os.system("freeform -calc solv -in ./"+DXX+".smi")
        os.system("rm ./"+DXX+".smi")
        
        
        os.chdir("../..")

        
    n = n+1



