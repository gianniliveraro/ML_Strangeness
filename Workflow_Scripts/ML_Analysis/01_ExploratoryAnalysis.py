# Copyright 2019-2020 CERN and copyright holders of ALICE O2.
# See https:#alice-o2.web.cern.ch/copyright for details of the copyright holders.
# All rights not expressly granted are reserved.
#
# This software is distributed under the terms of the GNU General Public
# License v3 (GPL Version 3), copied verbatim in the file "COPYING".
#
# In applying this license CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.
#
# Exploratory Analysis
# ================
#
# This code ....
#
#    Comments, questions, complaints, suggestions?
#    Please write to:
#    gianni.shigeru.setoue.liveraro@cern.ch
#    romain.schotter@cern.ch
#    david.dobrigkeit.chinellato@cern.ch

#____________________________
# Imports
from __future__ import division
import pandas as pd
import numpy as np
import os
import sklearn
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, mean_absolute_error, roc_curve, precision_recall_curve
from sklearn.preprocessing import binarize
from xgboost import XGBClassifier
import pickle
import time
t0 = time.time() # Initial time

#---------------------------  MAIN CONFIGURATIONS -----------------------------
##--------------------------------- FLAGS ------------------------------------

##--------------------------------- PATHS ------------------------------------
MAIN_PATH = '/storage1/liveraro/ML_Strangeness/'
RESULTS_PATH = MAIN_PATH + '/Results/'

##--------------------------------- DATASET ------------------------------------
DatasetName = 'LambdaMLTree' # csv file
Class_name = 'fIsLambda'

# Define Features
FeaturesToTrain = []

Dataset = pd.read_parquet(MAIN_PATH+'Dataset/{}_Train.parquet'.format(DatasetName))
print(Dataset.columns)
Features_DF = Dataset[FeaturesToTrain]
classes_DF = Dataset[[Class_name]]

print('features: ', Features_DF)
print('class: ', classes_DF.astype('int32'))
#BDtClassweight = len(classes[classe