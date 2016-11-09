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
pmemd.cuda -i ../../../../cfiles/$MDset/minin3 -o min3out -p $DXX.com.prmtop -c min2.rst -ref min2.rst  -r min3.rst -O
pmemd.cuda -i ../../../../cfiles/$MDset/minin4 -o min4out -p $DXX.com.prmtop -c min3.rst -ref min3.rst  -r min4.rst -O
pmemd.cuda -i ../../../../cfiles/$MDset/minin5 -o min5out -p $DXX.com.prmtop -c min4.rst -ref min4.rst  -r min5.rst -O


    ambpdb -p $DXX.com.prmtop < min5.rst > check_min.pdb
    cp ./min5.rst ../prod
    cp ./$DXX.com.prmtop ../prod
    cd ../prod


###########md_complex##################################
pmemd.cuda -O -i ../../../../cfiles/$MDset/heatinp -o heat.out -p $DXX.com.prmtop -c min5.rst -r heat.rst -x heat.mdcrd -ref min5.rst
pmemd.cuda -O -i ../../../../cfiles/$MDset/denceinp -o density.out -p $DXX.com.prmtop -c heat.rst -r density.rst -x density.mdcrd -ref heat.rst
pmemd.cuda -O -i ../../../../cfiles/$MDset/equilinp -o equil.out -p $DXX.com.prmtop -c density.rst -r equil.rst -x equil.mdcrd
pmemd.cuda -O -i ../../../../cfiles/$MDset/productinp -o product.out -p $DXX.com.prmtop -c equil.rst -r product.rst -x md_prod_001.mdcrd


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

