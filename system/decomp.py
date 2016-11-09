# coding: utf-8


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil
import sys

"""
[要件]
統合MMPBSA解析クラス
＃def 生データの整理
＃class プロット用にまとめる
＃class n回計測のデータの平均を表示、標準偏差も
#プロットデータのスマート化
＃ついでに経時エネルギー変化も排出
#データはhomedirに吐き出すように

#静電　vdw 疎水性の寄与まで

[仕様]
ディレクトリ構成
#homedir/
＃/{md1 md2 md3 mkdir(D01...)}/ 以下
解析はすべて新たに作成するD01...ディレクトリで行う

外部入力
＃計測回数 datanum=
＃残基数 residue=

"""

param =sys.argv
n=int(param[1])
m=int(param[2])
MDset=param[3]
dataset=int(param[4])
receptor=param[5]

ref= "D01"
"""
os.chdir("/home/klogw/1_work/99_python/decomp_add")
n=1
m=1
MDset="EXP_test_sf3IXP"
dataset=1
receptor="sfEcR_3IXP_nonsteroid"
ref= "D01"
"""


#情報収集フェイズ
f=open("./md1/cfiles/"+MDset+"/pbsa_info")
x=f.readlines()
snaps= str(x[3].split()[-1])

f2=open("./md1/input_info/"+receptor+"/info")
x2=f2.readlines()
LIG=int(str(x2[0].split()[-1]))
residue= int(LIG -1)



"""
###外部入力###
dataset=3
#計測回数
n=1
#D01から
m=4
#D04まで

ref="D01" #D01がレファレンス
snaps=100
residue=376
############

"""
#一回測定のデータ整形のためのクラス
#md実行ディレクトリ名と対象の化合物名を引数にとる
#経時および分解プロットまでできる
class Decomp:
    def __init__(self,MD,DXX):
        self.mddir= MD
        self.tag= DXX
        csv ="../../%s/MMPBSA_am1/%s/PBSA/FINAL_DECOMP_MMPBSA.dat" %(MD,DXX)
        self.df =pd.read_csv(csv,delimiter=",",skiprows=5)
        
        
    #残基名収集 
    #インデックスは1から始まる
    def get_name(self):
        Name=self.df.ix[1:residue,0]   
        temp=["NAN"]
        for x in Name:
            y=x.split()
            temp.append( y[0] + y[1])
            
        Name=pd.DataFrame(temp,columns={"Name"})
        Name=Name.drop([0])
        return Name
    
    
    #トータルdG
    def get_dG(self):
        dG=self.df.ix[1:residue,17]
        return dG
    
    
    #プロット用に整形されたデータフレーム
    def plot_data(self):
        Name=self.get_name()
        dG=self.get_dG()
        
        dataframe=pd.concat([Name.ix[1:residue],dG.ix[1:residue]],axis=1)
        return dataframe
    
    #単一プロット用
    def plot_1D(self):
        data=self.plot_data()
        for n in range(1,residue+1):
            if -0.2 < data.ix[n,1] < 0.5:
                data=data.drop([n])
        
        data.index=data["Name"]
        data=data.drop("Name",axis=1)
        
        
        data.plot(kind="bar")
        plt.tight_layout()
        plt.savefig('decomp1D.png', dpi=200)
        data.to_csv('decomp1D.csv')
        
        
    #本当ならクラス継承すべきだがもはやめんどい
    def get_vdw(self):
        vdw=self.df.ix[1:residue,5]
        return vdw
        
    
    def get_ele(self):
        ele=self.df.ix[1:residue,8]
        return ele
    
    def get_pb(self):
        pb=self.df.ix[1:residue,11]
        return pb
        
        
        
    def  plot_various(self):
        Name=self.get_name()
        vdw=self.get_vdw()
        ele=self.get_ele()
        pb=self.get_pb()
        dG=self.get_dG()
        
        df=pd.concat([Name.ix[1:residue],vdw.ix[1:residue],ele.ix[1:residue],pb.ix[1:residue],dG.ix[1:residue]],axis=1)
        
        
        
        for i in range(1,residue+1):
            if -0.4 <float(df.ix[i,1])< 0.5 and -0.4 <float(df.ix[i,2])< 0.5 and -0.4 <float(df.ix[i,3])< 0.5:
                print "True"
                df=df.drop([i])
        
        df.index=df["Name"]
        df=df.drop("Name",axis=1)
        df.columns=["vdw","ele","pb","Total"]
        
        df.ix[:,:]=df.ix[:,:].astype(float)
        df.plot(kind="bar")
        plt.tight_layout()
        plt.savefig('decomp_various.png', dpi=200)
        df.to_csv('decomp_various.csv')
        
    
    
    #mmpbsaの経時エネルギー変化を部分ごとに抽出
    #partは[complex,receptor,ligand]
    def pbsa_time(self,part):
        temp=np.array(["ENERGY","RMS","GMAX"])
        for x in range(0,20):
            try:
                f = open("../../"+self.mddir+"/MMPBSA_am1/"+self.tag+"/PBSA/"+"_MMPBSA_"+part+"_pb.mdout."+ str(x),"r+")
                lines=f.readlines()
            
                for i in xrange(len(lines)):
                    if "NSTEP       ENERGY          RMS" in lines[i]:
                        ### np.c_[] に注意　not( ) ###
                        z=lines[i+1].split()
                        y=np.array(z[1:4])
                        temp=np.c_[temp,y]
                    
            except:
                print "OKCOMPUTER" + str(x)
            
        Df= pd.DataFrame(temp).T        
        Df= Df.drop([0])
    
        #文字データ扱いなのでfloatに変換しなければ
        #あらゆる関数を適用できる
        #Df=Df.ix[:,Df.columns.map(lambda x: float(x))]
        Df.ix[:,:]=Df.ix[:,:].astype(float)
    
        #最後にcolumnsをつけたす
        Df.columns = ["ENERGY","RMS","GMAX"]
        return Df
    
    def pbsa_time_plot():
        print "AQN"
        

    
    
    


        
#3回測定のデータを処理するためのクラス
#md1-3のdGデータを引数にとるよ
class Plot3D():
    def __init__(self,md1,md2,md3):
        self.dG_3D=pd.concat([md1,md2,md3],axis=1)
        
    #ただの平均    
    def average(self):
        average=self.dG_3D.mean(axis=1)
        return average
    
    #標本標準偏差だよ
    def std(self):
        std=self.dG_3D.std(ddof=False,axis=1)
        return std
    
    #標準偏差付き棒グラフつくるよ
    #名前必須
    def plot_3D(self,Name):
        x= Name
        y= self.average()
        e= self.std()
        
        df =pd.concat([x,y,e],axis=1)
        df.columns=["Name","AVE","STD"]
        
        #次元削減
        for n in range(1,residue+1):
            if -0.2 < df.ix[n,1] < 0.5:
                df=df.drop([n])
                
        df.index=df.ix[:,0]
        df=df.drop("Name",axis=1)
        
        #プロット
        df.plot(kind="bar",yerr = "STD", ecolor = "black")
        plt.tight_layout()
        plt.savefig('decomp3D.png', dpi=200)
        df.to_csv('decomp3D.csv')
        
    
    #生データ用
    def alldata(self,Name):
        x= Name
        y= self.average()
        e= self.std()
        
        df =pd.concat([x,y,e],axis=1)
        df.columns=["Name","AVE","STD"]
        df.to_csv('decomp3D_alldata.csv')
        
        return df
        

        
        
        
        
#二つのデータを比較するクラス
#dGのみのデータを想定
class Compar:
    def __init__(self,data1,data2):
        self.data1=data1
        self.data2=data2
        

    def compar_plot(self,name):
        df=pd.concat([name,data1,data2],axis=1)
        df.columns=["Name","data1","data2"]
        
        
        for i in range(1,residue+1):
            if -0.2<df.ix[i,1]<0.5 and -0.2<df.ix[i,2]<0.5:
                df=df.drop([i])
            
        df.index=df.ix[:,0]
        df=df.drop("Name",axis=1)
        df.plot(kind="bar")
        plt.tight_layout()
        plt.savefig('reference.png', dpi=200)
        df.to_csv('reference.csv')

        
        
        
        

        
        
        
        
        
if "UDK"=='UDK':
    os.system("mkdir ./RESULT")
    os.chdir("./RESULT")
    #統合解析用
    #まずはD01ディレクトリの作成から
    for i in range(n,m+1):
        #名前の定義
        if i < 10:
            DXX= "D0" + str(i)
        else:
            DXX= "D" + str(i)
        
        if os.path.exists("../md1/structs/"+DXX+".mol2"):
            
            os.makedirs(DXX)
            os.chdir("./"+DXX)

            #計測回数別ディレクトリの作成と解析
            for i in range(1,dataset+1):
                os.makedirs("./md" + str(i))
                #経時変化のプロット
                try:
                    com= Decomp("md"+str(i),DXX).pbsa_time("complex")
                    rec= Decomp("md"+str(i),DXX).pbsa_time("receptor")
                    lig= Decomp("md"+str(i),DXX).pbsa_time("ligand")
                    tot= com - rec -lig

                    tot.plot(x=tot.index,y="ENERGY")
                    plt.savefig("dG_time.png")
                    shutil.move("./dG_time.png","./md"+str(i)+"/dG_time.png")


                except:
                    print "time_mmpbsa error"


                #分解棒グラフの作成
                #トータル
                Decomp("md"+str(i),DXX).plot_1D()
                shutil.move("./decomp1D.png","./md"+str(i)+"/decomp1D.png")
                shutil.move("./decomp1D.csv","./md"+str(i)+"/decomp1D.csv")
                #個別分解
                Decomp("md"+str(i),DXX).plot_various()
                shutil.move("./decomp_various.png","./md"+str(i)+"/decomp_various.png")
                shutil.move("./decomp_various.csv","./md"+str(i)+"/decomp_various.csv")



            #平均ディレクトリ
            if dataset == 3:
                try:
                    os.makedirs("average")

                    x= Decomp("md1",DXX).get_dG()
                    y= Decomp("md2",DXX).get_dG()
                    z= Decomp("md3",DXX).get_dG()
                    name= Decomp("md1",DXX).get_name()

                    Plot3D(x,y,z).plot_3D(name)
                    Plot3D(x,y,z).alldata(name)

                    shutil.move("./decomp3D.png","./average/decomp3D.png")
                    shutil.move("./decomp3D.csv","./average/decomp3D.csv")
                    shutil.move("./decomp3D_alldata.csv","./average/decomp3D_alldata_csv")

                except:
                    print "3D_decomp error"

            #レファレンス棒グラフの作成
                try:
                    print "AQN"
                    #レファレンス側のデータ取得
                    x1= Decomp("md1",ref).get_dG()
                    y1= Decomp("md2",ref).get_dG()
                    z1= Decomp("md3",ref).get_dG()
                    name= Decomp("md1",ref).get_name()
                    data1= Plot3D(x1,y1,z1).average()

                    x2= Decomp("md1",DXX).get_dG()
                    y2= Decomp("md2",DXX).get_dG()
                    z2= Decomp("md3",DXX).get_dG()
                    name= Decomp("md1",DXX).get_name()
                    data2= Plot3D(x2,y2,z2).average()

                    Compar(data1,data2).compar_plot(name)


                except:
                    print "reference error"


            #最初に戻る
            os.chdir("..")


else:
    os.chdir("..")
        
        
            
        
#2.0ではディレクトリがとびとびだとダメなエラーを改変
#機能も追加


# In[ ]:



