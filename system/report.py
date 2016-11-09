# coding: utf-8

# In[7]:

from openeye.oechem import *
import glob


# In[8]:

#mollistへ
mol_list=[]
name_list=[]

sdf_list= sorted([ x.split("/")[-1] for x in glob.glob("./md1/sdf/*.sdf")])

for sdf in sdf_list:
    print sdf, " is True"
    ifs= oemolistream("./md1/sdf/"+ sdf)
    mol= OEGraphMol()
    OEReadMolecule(ifs,mol)
    mol_list.append(mol)
    name_list.append(sdf)
    


# In[9]:

#smilelistへ
"""
smi_list=[]

for mol in mol_list:
    smi= OEMolToSmiles(mol)
    smi_list.append(smi)

print smi_list
print name_list
"""


# In[33]:

import pandas as pd
import os

if os.path.exists("./RESULT/Result_total.csv"):
    csv= pd.read_csv("./RESULT/Result_total.csv",delimiter=",",index_col='Name')
else:
    csv= pd.read_csv("./RESULT/result_md1.csv",delimiter=",",index_col='Name')
    


# In[16]:

from openeye.oedepict import *

#reportoptionの初期化

#header,body,footerの設定

#OEReportOptions(line,columnn) #bodyのcell設定
ropts = OEReportOptions(6,4)

#OESetupReportOptions(ropts,itf)
    
ropts.SetHeaderHeight(5)
ropts.SetFooterHeight(5)
ropts.SetCellGap(2)
ropts.SetPageMargins(10)
    
report = OEReport(ropts)


cellwidth, cellheight = report.GetCellWidth(), report.GetCellHeight()
opts = OE2DMolDisplayOptions(cellwidth, cellheight, OEScale_AutoScale)


# In[38]:




for (mol,name) in zip(mol_list,name_list):
    #画像
    mol.SetTitle(name)
    print name
    cell= report.NewCell()  #次のセルへ
    
    OEPrepareDepiction(mol) #molに二次元構造を付加
    disp = OE2DMolDisplay(mol, opts) #
    OERenderMolecule(cell, disp)
    OEDrawBorder(cell, OEPen(OELightGrey, OELightGrey, OEFill_Off, 1.0))

    
    
    
    
    
    
    #ここらへんはwxPythonのイメージで
    # render corresponding data
    cell = report.NewCell()
    OEDrawBorder(cell, OEPen(OELightGrey, OELightGrey, OEFill_Off, 1.0))
    
    image=cell
    imagew, imageh = image.GetWidth(), image.GetHeight()
    
    tframe = OEImageFrame(image, imagew * 0.30, imageh, OE2DPoint(0.0, 5.0)) #左1/3は名前で占有
    tgrid = OEImageGrid(tframe, 12, 1) #フレームを12ライン1カラムに分割
    tfont = OEFont(OEFontFamily_Default, OEFontStyle_Bold,
                   8, OEAlignment_Left, OEBlack)
    tpos = OE2DPoint(5.0, tgrid.GetCellHeight() / 2.0)

    # generating grid for values

    vframe = OEImageFrame(image, imagew * 0.70, imageh, OE2DPoint(imagew * 0.30, 5.0))
    vgrid = OEImageGrid(vframe, 12, 1)
    vfont = OEFont(OEFontFamily_Default, OEFontStyle_Default,
                   8, OEAlignment_Left, OEBlack)
    vpos = OE2DPoint(5.0, vgrid.GetCellHeight() / 2.0)
    
    #tag-value辞書をつくります
    name=name.split(".")[0] #D02.sdf => D02
    
    data=[]
    data.append(("Name", name))
    if not os.path.exists("./RESULT/Result_total.csv"):
        data.append(("MMPBSA", str(csv.ix[name,'mmpbsa'])))
    else:
        data.append(("TOTAL", str(csv.ix[name,'TOTAL'])))
        
    if not os.path.exists("./RESULT/Result_total.csv"):
        data.append(("TdS", str(csv.ix[name,'TdS'])))
        data.append(("Estr", str(csv.ix[name,'Estr'])))
    
    
    # rendering (tag - value) data enumerateはインデックスを付加　たぶん0はじまりなんやろな
    for idx, (tag, value) in enumerate(data):
        cell = tgrid.GetCell(idx + 1, 1)
        cell.DrawText(tpos, tag + ":", tfont, cell.GetWidth())
        cell = vgrid.GetCell(idx + 1, 1)
        cell.DrawText(vpos, value, vfont, cell.GetWidth())

    
    




#出力
try:
    OEWriteReport("./RESULT/Report.pdf", report)
    print "MMPBSA finished gracefully"
except:
    print "Finished, but something wrong"


# In[ ]:



