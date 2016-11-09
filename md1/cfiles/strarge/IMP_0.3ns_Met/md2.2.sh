#!/bin/bash

n=$1
m=$2
MDset=$3
#ligandの名前はDAn　DXn


###############全体ループ##################################

while  [ $n -le $m ] 
    do

############ 命名#########################################
    if [ $n -lt 10 ]
        then
        DXX=D0$n
        else
        DXX=D$n
    fi
#########min_complex##################################
if test -e ./structs/$DXX.mol2 ; then 


    cd ./MD_am1/$DXX/com/equi

pmemd.cuda -i ../../../../cfiles/$MDset/minin0 -o min0out -p $DXX.com.prmtop -c $DXX.com.inpcrd -ref $DXX.com.inpcrd  -r min0.rst -O
pmemd.cuda -i ../../../../cfiles/$MDset/minin1 -o min1out -p $DXX.com.prmtop -c min0.rst -ref min0.rst  -r min1.rst -O
pmemd.cuda -i ../../../../cfiles/$MDset/minin2 -o min2out -p $DXX.com.prmtop -c min1.rst -ref min1.rst  -r min2.rst -O


    ambpdb -p $DXX.com.prmtop < min2.rst > check_min.pdb
    
    cp ./$DXX.com.prmtop ../prod
    cp ./min2.rst ../prod
    cd ../prod


###########md_complex##################################
pmemd.cuda -O -i ../../../../cfiles/$MDset/heatinp -o heat.out -p $DXX.com.prmtop -c min2.rst -ref min2.rst -r heat.rst -x heat.mdcrd
pmemd.cuda -O -i ../../../../cfiles/$MDset/equilinp -o equil.out -p $DXX.com.prmtop -c heat.rst -r equil.rst -ref heat.rst  -x equil.mdcrd
pmemd.cuda -O -i ../../../../cfiles/$MDset/productinp -o product.out -p $DXX.com.prmtop -c equil.rst -r product.rst -ref equil.rst  -x md_prod_001.mdcrd


    ambpdb -p $DXX.com.prmtop < equil.rst > check_equal.pdb
    ambpdb -p $DXX.com.prmtop < product.rst > check_product.pdb

###########min_lig##########################################

    cd ../../lig/equi


    cd ../prod


    cd ../../../..

else
echo "$DXX not found!"

fi

####nの再定義#############################################################
    n=`expr $n + 1 `

     done

