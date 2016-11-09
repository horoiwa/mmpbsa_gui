#!/bin/bash

#２Dsdfを３Dmol2に変換するためだけにhybridによるドッキングを行うという不毛なことをしている。電荷計算までしてくれるから楽だね

n=
m=
rec=receptor.oeb.gz


#############outputdirから開始です######################

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

    mkdir $DXX

        cd  ./$DXX
        mkdir ./HYB

            cd ./HYB
            omega2 -in ../../sdf2.0/$DXX.sdf -out multiconformer_$DXX.oeb.gz -rms 0.1 -strictstereo false
            hybrid -receptor ../../receptor.oeb.gz  -dbase multiconformer_$DXX.oeb.gz -num_poses 1 -docked_molecule_file $DXX.sdf -dock_resolution High
            cd ..

        babel -isdf ./HYB/$DXX.sdf -omol2 $DXX.mol2
        sed -i -e "s/LIG1/$DXX/g"  $DXX.mol2
        cp ../grid/test.inp .
        sed -i -e "s/XXX/$DXX/g"  test.inp
        sievgene.g120 < test.inp
        cd ..

#nの再定義
    n=`expr $n + 1 `

    done

