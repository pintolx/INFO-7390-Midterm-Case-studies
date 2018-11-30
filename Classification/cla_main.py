# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 01:54:24 2018

@author: wenqi
"""
import os
import shutil
import pandas as pd

from configparser import ConfigParser
import requests
from bs4 import BeautifulSoup

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

#main function
def main_function(filename,value):
    
    docu=filename
    
    if len(docu)!=6 :
        raise Exception("File name error")
        exit()
    
    docu2=''
    if docu[1]=='4':
        docu2 = docu[0]+'1'+str(int(docu[2:])+1)
    else:
        docu2 = docu[0]+str(int(docu[1])+1)+docu[2:]
    dww=[docu,docu2]      
    
    
    cookie={'PHPSESSID': value}
    url = 'https://freddiemac.embs.com/FLoan/Data/download.php'
    
    r = requests.post(url,cookies=cookie)
    content=r.content
    soup = BeautifulSoup(content,'lxml')
    all_href = soup.find_all('a')
    i=0;
    lod=len(dww)
    url_list=['https://freddiemac.embs.com/FLoan/Data/']*lod
    
    for href in all_href:
        for s in dww:
            if s in href['href']:
                url_list[i]=url_list[i]+href['href']
                i+=1    
    if len(all_href)==0:
         raise Exception("Login error")   
    
    if (not os.path.exists('data')):
        os.mkdir('data')
    os.chdir('data')
    for i in range(len(url_list)):
        r = requests.get(url_list[i],cookies=cookie)
        with open(url_list[i][71:77]+'.zip','wb') as code:
            code.write(r.content)
    files= os.listdir()
	for file in files:
		for docu in dww:
			if ('.zip' in file) and (docu in file):
				shutil.unpack_archive(file)
    os.chdir('..')  
    
    file1="data/historical_data1_time_"+docu+".txt"
    file2="data/historical_data1_time_"+docu2+".txt"  
    
    
    data = pd.read_csv(file1,sep="|",header=None,nrows=101000)
    data.columns = ["LOAN SEQUENCE NUMBER","MONTHLY REPORTING PERIOD","CURRENT ACTUAL UPB","CURRENT LOAN DELINQUENCY STATUS"
                    ,"LOAN AGE",
                   "REMAINING MONTHS TO LEGAL MATURITY","REPURCHASE FLAG","MODIFICATION FLAG"
                    ,"ZERO BALANCE CODE","ZERO BALANCE EFFECTIVE DATE",
                   "CURRENT INTEREST RATE","CURRENT DEFERRED UPB","DUE DATE OF LAST PAID INSTALLMENT (DDLPI)"
                    ,"MI RECOVERIES","NET SALES PROCEEDS",
                   "NON MI RECOVERIES","EXPENSES","LEGAL COSTS","MAINTENANCE AND PRESERVATION COSTS"
                    ,"TAXES AND INSURANCE","MISCELLANEOUS EXPENSES",
                   "ACTUAL LOSS CALCULATION","MODIFICATION COST","STEP MODIFICATION FLAG"
                    ,"DEFERRED PAYMENT MODIFICATION","ESTIMATED LOAN TO VALUE (ELTV)"]
    
    vali = pd.read_csv(file2,sep="|",header=None,nrows=101000)
    vali.columns = ["LOAN SEQUENCE NUMBER","MONTHLY REPORTING PERIOD","CURRENT ACTUAL UPB","CURRENT LOAN DELINQUENCY STATUS"
                    ,"LOAN AGE",
                   "REMAINING MONTHS TO LEGAL MATURITY","REPURCHASE FLAG","MODIFICATION FLAG"
                    ,"ZERO BALANCE CODE","ZERO BALANCE EFFECTIVE DATE",
                   "CURRENT INTEREST RATE","CURRENT DEFERRED UPB","DUE DATE OF LAST PAID INSTALLMENT (DDLPI)"
                    ,"MI RECOVERIES","NET SALES PROCEEDS",
                   "NON MI RECOVERIES","EXPENSES","LEGAL COSTS","MAINTENANCE AND PRESERVATION COSTS"
                    ,"TAXES AND INSURANCE","MISCELLANEOUS EXPENSES",
                   "ACTUAL LOSS CALCULATION","MODIFICATION COST","STEP MODIFICATION FLAG"
                    ,"DEFERRED PAYMENT MODIFICATION","ESTIMATED LOAN TO VALUE (ELTV)"]
    
    train_data=data[:100000]
    train_data = preprocessing(train_data)
    vali_data=vali[:100000]
    vali_data = preprocessing(vali_data)
    
    train_x = train_data.drop('Delinquent',axis=1)
    train_y = train_data['Delinquent']
    test_x = vali_data.drop('Delinquent',axis=1)
    test_y = vali_data['Delinquent']
    
    rf = RandomForestClassifier(max_depth=7,n_estimators=100)
    rf.fit(train_x,train_y)
    pred_y = rf.predict(test_x)
    cm=confusion_matrix(test_y,pred_y)
    tn, fp, fn, tp = cm.ravel()
    print("End with "+filename)
      
    return tn, fp, fn, tp


def preprocessing(data):
    data['Delinquent']=[0 if x == '0' else 1 for x in data['CURRENT LOAN DELINQUENCY STATUS']]
    data.drop(['LOAN SEQUENCE NUMBER','REPURCHASE FLAG','CURRENT LOAN DELINQUENCY STATUS','MODIFICATION FLAG','ZERO BALANCE CODE'
           ,'ZERO BALANCE EFFECTIVE DATE','DUE DATE OF LAST PAID INSTALLMENT (DDLPI)','MI RECOVERIES'
          ,'NET SALES PROCEEDS','NON MI RECOVERIES','EXPENSES','LEGAL COSTS','MAINTENANCE AND PRESERVATION COSTS'
          ,'TAXES AND INSURANCE','MISCELLANEOUS EXPENSES','ACTUAL LOSS CALCULATION','MODIFICATION COST'
          ,'STEP MODIFICATION FLAG','ESTIMATED LOAN TO VALUE (ELTV)'],axis=1,inplace=True)
    dictionary_25 = {'Y':1,'N':0,' ':-1}
    data['DEFERRED PAYMENT MODIFICATION'] = [dictionary_25[x] for x in data['DEFERRED PAYMENT MODIFICATION']]
    return data

