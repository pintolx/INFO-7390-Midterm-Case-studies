
# coding: utf-8


import os
import shutil
import pandas as pd

from configparser import ConfigParser
import requests
from bs4 import BeautifulSoup

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

from cla_main import main_function
    
#Get input from configuration

cfg = ConfigParser()
cfg.read('classification.config')
value = cfg.get('cookie','value')
docu = cfg.get('file','name')

tn, fp, fn, tp = main_function(docu,value)


print('TN: ',tn)
print('FP: ',fp)
print('FN: ',fn)
print('TP: ',tp)



print('Number of Actual Delinquents:', tp+fn)
print('Number of Predicted Delinquents:',  tp+fp)
print('Number of records in the dataset:',  tn+tp+fn+fp)
print('Number of Delinquents properly classified:',  tp)
print('Number of nondelinquents improperly classified as delinquents:',  fp)

