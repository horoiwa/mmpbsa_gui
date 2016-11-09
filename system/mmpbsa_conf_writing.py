# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os
import sys

param =sys.argv
n=int(param[1])
m=int(param[2])





x=open("result_mmpbsa_conf.csv","a")
x.write("Name,mmpbsa,TdS,Estr, \n")


while n <= m:

# name define for DXX
    if n < 10:
        DXX="D0%s" %(n)
    else:
        DXX="D%s" %(n)
        
        
    def mmpbsa():
        try:
            y=open("./MMPBSA_am1/" + DXX + "/PBSA/mmpbsa.out","r")
            
            for line in y.readlines():
                if "DELTA TOTAL" in line:
                    a=line.split()
                    dG_mmpbsa=str(a[2])
                    x.write(DXX+","+dG_mmpbsa+",")
                
        except:
            print "mmpbsa error"
            
            
        try:
            z=open("./Confene/" + DXX + "/TdS_Estr.dat","r")
            for line in z.readlines():
                if "Average" in line:
                    b=line.split()
                    x.write(b[2] + "," + b[4] + ", \n")
       
        except:
            print "conf error"
        
   
        
    if os.path.exists("./structs/"+DXX+".mol2"):
        mmpbsa()
    else:
        print "Sorry %s not found" %(DXX)
    
    n += 1
    
x.close()


# <codecell>


