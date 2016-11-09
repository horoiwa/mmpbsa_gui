#!/bin/bash


n=$1
m=$2


#############outputdirから開始です######################

source $AMBERHOME/amber.sh

#全体ループ
while  [ $n -le $m ] 
    do
# 命名
    if [ $n -lt 10 ]
        then
        DXX=D0$n
        else
        DXX=D$n
    fi

##################################
	if test -e ./structs/$DXX.mol2 ; then    

	    cd ./MMPBSA_am1/$DXX/PBSA

	  mpirun -np 6 MMPBSA.py.MPI -O \
	  -i ../../../mmpbsa.in \
	  -o mmpbsa.out \
	  -cp  com.top \
	  -y   com.mdcrd \
	  -rp  rec.top \
	  -yr  rec.mdcrd \
	  -lp  lig.top \
	  -yl  lig.mdcrd \


	    cd ../../..

	else
	echo "$DXX not found!"

	fi

#nの再定義
    n=`expr $n + 1 `
    done


