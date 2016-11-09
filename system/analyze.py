# coding: utf-8

import os
import pandas as pd
import numpy as np
import sys
import shutil

param =sys.argv
repeat=int(param[1])




def average():
    Df1= pd.read_csv("result_md1.csv",delimiter=",",index_col='Name')
    Df2= pd.read_csv("result_md2.csv",delimiter=",",index_col='Name')
    Df3= pd.read_csv("result_md3.csv",delimiter=",",index_col='Name')
   
    dG1=Df1.ix[:,0]+Df1.ix[:,1]
    dG2=Df2.ix[:,0]+Df2.ix[:,1]
    dG3=Df3.ix[:,0]+Df3.ix[:,1]
    
        
    DFtot=pd.concat([dG1,dG2,dG3],axis=1)
    DFave= DFtot.mean(axis=1)
    DFsd=DFtot.std(ddof=False,axis=1)
    
    DFtot=pd.concat([DFtot,DFave,DFsd],axis=1)
    DFtot.columns=["md1","md2","md3","TOTAL","SD"]
    DFtot.to_csv("Result_total.csv")





os.makedirs("./RESULT")
shutil.copy("./md1/result_mmpbsa_conf.csv","./RESULT/result_md1.csv")

if repeat == 3:
    shutil.copy("./md2/result_mmpbsa_conf.csv","./RESULT/result_md2.csv")
    shutil.copy("./md3/result_mmpbsa_conf.csv","./RESULT/result_md3.csv")
    
    
    os.chdir("RESULT")
    average()
    os.chdir("..")





