# coding: utf-8
 
import os
import glob

os.chdir("./md1/sdf")
SDfiles= glob.glob("*.sdf")

for sdf in SDfiles:
	print "Convert" + sdf
	DXX= sdf[0:3]
	if os.path.exists("../structs/"+DXX+".mol2"):
	    print DXX+".mol2 already exists"
	    
	else:
	    os.system("babel -isdf "+sdf+" -omol2 ../structs/"+DXX+".mol2" )
	    os.system('sed -i -e "s/LIG1/'+DXX+'/g"  ../structs/'+DXX+'.mol2')
	    

os.chdir("../..")
