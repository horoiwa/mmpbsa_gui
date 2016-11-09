#!/bin/bash

#for 1 trajectory
n=$1
m=$2
start=$3
stop=$4
inter=$5
snaps=$6   #stop/inter
Pro=$7
Lig=$8


#############outputdirから開始です######################

mkdir MMPBSA_am1

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

#####トラジェクトリの準備#####################################

if test -e ./structs/$DXX.mol2 ; then 

    mkdir ./MMPBSA_am1/$DXX
    mkdir ./MMPBSA_am1/$DXX/com
    mkdir ./MMPBSA_am1/$DXX/com/mdcrd

    cd ./MMPBSA_am1/$DXX/com/mdcrd

    cp ../../../../MD_am1/$DXX/com/prod/$DXX.com.prmtop ./"$DXX"_com.prmtop
          
echo "trajin ../../../../MD_am1/$DXX/com/prod/md_prod_001.mdcrd $start $stop $inter" > imagetraj.in
echo "center :1-$Lig origin mass" >> imagetraj.in
echo "image origin center" >> imagetraj.in
echo "trajout ./md_prod_001_img.mdcrd" >> imagetraj.in
echo "go" >> imagetraj.in

cpptraj "$DXX"_com.prmtop ./imagetraj.in

    cd ../../../..

   ##############繰り返し#########################

    mkdir ./MMPBSA_am1/$DXX/lig
    mkdir ./MMPBSA_am1/$DXX/lig/mdcrd
     
    cd ./MMPBSA_am1/$DXX/lig/mdcrd

    cd ../../../..

##############noboxしてくよ#################
###別にsじゃないけど書き換えめんどいのでs_ligとか####

    cd ./MMPBSA_am1/$DXX/com

    mkdir s_lig
    mkdir s_res
    mkdir s_com
    mkdir topo
    


    cd ./s_res

echo "trajin ../mdcrd/md_prod_001_img.mdcrd 1 $snaps 1" > boxremove.in
echo "strip :WAT" >> boxremove.in
echo "strip :Cl-" >> boxremove.in
echo "strip :Na+" >> boxremove.in
echo "strip :$Lig" >> boxremove.in
echo "trajout ./rec.mdcrd nobox" >> boxremove.in
echo "go" >> boxremove.in

cpptraj ../mdcrd/"$DXX"_com.prmtop ./boxremove.in


    cd ../s_lig

echo "trajin ../mdcrd/md_prod_001_img.mdcrd 1 $snaps 1" > boxremove.in
echo "strip :$Pro" >> boxremove.in
echo "strip :WAT" >> boxremove.in
echo "strip :Cl-" >> boxremove.in
echo "strip :Na+" >> boxremove.in
echo "trajout ./lig.mdcrd nobox" >> boxremove.in
echo "go" >> boxremove.in

cpptraj ../mdcrd/"$DXX"_com.prmtop ./boxremove.in


    cd ../s_com

echo "trajin ../mdcrd/md_prod_001_img.mdcrd 1 $snaps 1" > boxremove.in
echo "strip :WAT" >> boxremove.in
echo "strip :Cl-" >> boxremove.in
echo "strip :Na+" >> boxremove.in
echo "trajout ./com.mdcrd nobox" >> boxremove.in
echo "go" >> boxremove.in

cpptraj ../mdcrd/"$DXX"_com.prmtop ./boxremove.in

    cd ../..

 ######repeat############

 


##############topoつくるよ#####################################
   
    cd ./com/topo
#tot#
cp ../../../../MD_am1/$DXX/cryst/"$DXX"_solv_com.pdb ./totIN.pdb
    
#res#
grep -v "WAT" ./totIN.pdb |grep -v "Na+"|grep -v "Cl-" | grep -v "$DXX   $Lig"  > recIN.pdb

#lig#
grep "$DXX   $Lig" ./totIN.pdb > ligIN.pdb

#com#
grep -v "WAT" ./totIN.pdb |grep -v "Na+"|grep -v "Cl-"  > comIN.pdb




#resleap

echo "source leaprc.ff14SB" > leap_res.in
echo "loadAmberParams frcmod.ionsjc_tip3p" >> leap_res.in
echo "source leaprc.gaff" >> leap_res.in
echo "set default PBRadii mbondi2" >> leap_res.in
echo "SYS = loadpdb ./recIN.pdb" >> leap_res.in
echo "saveAmberParm SYS ./rec.top ./rec.crd" >> leap_res.in
echo "savepdb SYS rec.pdb" >> leap_res.in
echo "quit" >> leap_res.in

tleap -f leap_res.in > leap_res.log

#ligleap

echo "source leaprc.ff14SB" > leap_lig.in
echo "loadAmberParams frcmod.ionsjc_tip3p" >> leap_lig.in
echo "source leaprc.gaff" >> leap_lig.in
echo "set default PBRadii mbondi2" >> leap_lig.in
echo "loadAmberParams ../../../../leap/$DXX/$DXX.frcmod" >> leap_lig.in
echo "loadAmberPrep ../../../../leap/$DXX/$DXX.prep" >> leap_lig.in
echo "SYS = loadpdb ./ligIN.pdb" >> leap_lig.in
echo "saveAmberParm SYS ./lig.top ./lig.crd" >> leap_lig.in
echo "savepdb SYS lig.pdb" >> leap_lig.in
echo "quit" >> leap_lig.in

tleap -f leap_lig.in > leap_lig.log    

#comleap
echo "source leaprc.ff14SB" > leap_com.in
echo "loadAmberParams frcmod.ionsjc_tip3p" >> leap_com.in
echo "source leaprc.gaff" >> leap_com.in
echo "set default PBRadii mbondi2" >> leap_com.in
echo "loadAmberParams ../../../../leap/$DXX/$DXX.frcmod" >> leap_com.in
echo "loadAmberPrep ../../../../leap/$DXX/$DXX.prep" >> leap_com.in
echo "SYS = loadpdb ./comIN.pdb" >> leap_com.in
echo "saveAmberParm SYS ./com.top ./com.crd" >> leap_com.in
echo "savepdb SYS com.pdb" >> leap_com.in
echo "quit" >> leap_com.in

tleap -f leap_com.in > leap_com.log  

   cd ../..

##comのtopo作成終了##############
#                    #
###################################


   cd ../..

#######enegy###########################
cd ./MMPBSA_am1/$DXX
mkdir PBSA
cd ./PBSA

cp ../com/s_lig/lig.mdcrd lig.mdcrd
cp ../com/s_com/com.mdcrd com.mdcrd
cp ../com/s_res/rec.mdcrd rec.mdcrd

cp ../com/topo/lig.top lig.top
cp ../com/topo/com.top com.top
cp ../com/topo/rec.top rec.top


cd ..
mkdir lig_only
cd ./lig_only

cp ../lig/s_lig/lig_only.mdcrd lig_only.mdcrd
cp ../lig/topo/lig_only.top lig_only.top

cd ../../..



else
echo "$DXX not found!"

fi


#nの再定義
    n=`expr $n + 1 `
    done


