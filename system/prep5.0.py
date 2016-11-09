# coding: utf-8


import sys
import os
import shutil



"""
外部変数は
n= 2　（int）
m= 12  (int) など
receptor sf3ixp
MDconfig set1　　を想定


ディレクトリ構成
md1と同じディレクトリ（home）から開始

"""
param = sys.argv

n= int(param[1])
m= int(param[2])
RECEP= param[3]
WAT=param[4]


def leap():
    
    os.makedirs("./md1/leap/"+ DXX)
    os.chdir("./md1/leap/"+ DXX)
    shutil.copy("../../structs/"+ DXX +".mol2", ".")
    
    os.system("antechamber -fi mol2 -i "+DXX+".mol2 -fo prepc -o "+DXX+".prep -at gaff -c bcc -nc 0")
    os.system("parmchk2 -i "+DXX+".prep -f prepc -o "+DXX+".frcmod")
    shutil.copy("../../input_info/"+RECEP+"/"+RECEP+".pdb","./"+DXX+".com.pdb")
    
    
    #複合体の作成
    f=open("../../input_info/"+RECEP+"/info")
    LIG= f.readlines()[0].split()[-1]
    os.system('sed -i -e "s/'+DXX+'     1/'+DXX+'   '+LIG+'/g"  NEWPDB.PDB')
    os.system("cat NEWPDB.PDB >> "+DXX+".com.pdb")
    os.system('echo "END" >> '+DXX+'.com.pdb')
    
    #inputfile作成
    shutil.copy("../../input_info/"+RECEP+"/leap_"+WAT+".in",".")
    os.system('sed -i -e "s/VAR/'+DXX+'/g"  leap_'+WAT+'.in')




    os.system("tleap -f leap_"+WAT+".in > leap_"+WAT+".out")
    os.system("ambpdb -p "+DXX+".com.prmtop < "+DXX+".com.inpcrd > cheak_complex.pdb")
    
    os.chdir("../../../") #homeにもどる 
    
    
def md_cryst():
    os.makedirs("./md1/MD_am1/"+DXX+"/com/equi")
    os.makedirs("./md1/MD_am1/"+DXX+"/com/prod")
    os.makedirs("./md1/MD_am1/"+DXX+"/cryst")
    
    
    shutil.copy("./md1/leap/"+DXX+"/"+DXX+".com.prmtop","./md1/MD_am1/"+DXX+"/com/equi/"+DXX+".com.prmtop")
    shutil.copy("./md1/leap/"+DXX+"/"+DXX+".com.inpcrd","./md1/MD_am1/"+DXX+"/com/equi/"+DXX+".com.inpcrd")
    shutil.copy("./md1/leap/"+DXX+"/cheak_complex.pdb","./md1/MD_am1/"+DXX+"/cryst/"+DXX+"_solv_com.pdb")








    
if "meaningless" == "meaningless":
    
    os.system("mkdir ./md1/leap")
    os.system("mkdir ./md1/MD_am1")
    
    
    for i in range(n,m+1):
        if i < 10:
            DXX= "D0%s" %str(i)
        else:
            DXX= "D%s" %str(i)
        print DXX
            
            
        if os.path.exists("./md1/structs/"+DXX+".mol2"): 
            leap()
            md_cryst()
            print DXX + " finished"
                
        else:
            print "Sorry %s not found" %(DXX)
        
    else:
        
        print "Prep END"
        
    
        
    



