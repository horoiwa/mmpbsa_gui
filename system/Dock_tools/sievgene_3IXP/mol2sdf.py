import os

for i in range(5,11):
    DXX= "D0"+str(i) if i < 10 else "D"+str(i)
    os.system('babel -imol2 '+DXX+'.mol2 -osdf ./sdf/'+DXX+'.sdf')
