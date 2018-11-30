# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 01:26:05 2018

@author: wenqi
"""
import pandas as pd
import gc
from cla_main import main_function

filelist=[
        'Q11999',
        'Q21999',
        'Q31999',
        'Q41999',
        'Q12000',
        'Q22000',
        'Q32000',
        'Q42000',
        ]
value='11vr6kgl2a9lt7b8if0mv08vq0'
df = pd.DataFrame(columns = ["Actual Delinquents", "Predicted Delinquents", "Records in the dataset"
                             , "Delinquents properly classified","nondelinquents improperly classified as delinquents"])
for file in filelist:
    tn, fp, fn, tp=main_function(file,value)
    df.loc[df.shape[0]+1]=[tp+fn,tp+fp,tn+tp+fn+fp,tp,fp]
    gc.collect()
filelist2=[
        'Q21999',
        'Q31999',
        'Q41999',
        'Q12000',
        'Q22000',
        'Q32000',
        'Q42000',
        'Q12001',        
        ]
df["Quarter"]=filelist2
print(df)
df.to_csv('matrix.csv')