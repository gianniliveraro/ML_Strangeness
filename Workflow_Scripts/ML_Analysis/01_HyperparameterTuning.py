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
# ML hyperparameter tuning code
# ================
#
# This code finds the best set of hyperparameters of a BDT model
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
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, GridSearchCV, StratifiedKFold
from sklearn.metrics import confusion_matrix, accuracy_score, mean_absolute_error, roc_curve, precision_recall_curve, roc_auc_score
from sklearn.preprocessing import binarize
from xgboost import XGBClassifier
import optuna
import pickle
import json
import time
t0 = time.time() # Initial time

#---------------------------  MAIN CONFIGURATIONS -----------------------------
##--------------------------------- FLAGS ------------------------------------
fUseOptuna = True # if False uses GridSearchCV for hyperparameters search
fCreateNewrun = False # if True, creates a directory in 'ML_Strangeness/Results/' to save ML run configurations and results 

# Please, include a short description of this Run:
RunDescription = "Test run of the ML workflow with Gammas"

##--------------------------------- PATHS ------------------------------------
MAIN_PATH = '/storage1/liveraro/ML_Strangeness/'
RESULTS_PATH = MAIN_PATH + '/Results/'
os.makedirs(RESULTS_PATH, exist_ok=True)

##--------------------------------- DATASET ------------------------------------
Target = "Gamma" # Target particle. Options: AntiLambda, Gamma, KZeroShort 
DatasetName = Target # csv file
Class_name = 'fIs'+Target

# Define Features
FeaturesToTrain = ['fPt', 'fQt', 'fAlpha', 'fRadius', 'fCosPA', 'fDCADau',
       'fDCANegPV', 'fDCAPosPV']

Dataset = pd.read_parquet(MAIN_PATH+'Dataset/{}_Train.parquet'.format(DatasetName))
Features_DF = Dataset[FeaturesToTrain]
classes_DF = Dataset[[Class_name]].astype('int32')

#BDtClassweight = len(classes_DF[classes[Class_name]==0])/len(classes[classes[Class_name]==1]) # activate this if class balancing is necessary

##--------------------- HYPERPARAMETER SEARCH SPACE ----------------------------

BDT_params = {'objective':['binary:logistic'],
              'learning_rate': [0.001, 0.01, 0.05, 0.1, 0.5, 1.0], 
              'max_depth': [2, 4, 6, 8, 10, 12],
              'n_estimators': [10, 50, 100, 200, 300, 400, 500],
              'random_state' :[42]
              #'scale_pos_weight' :[BDtClassweight]
}

def objective(trial): # Optuna search space
    """Define the objective function"""

    params = {
        'max_depth': trial.suggest_int('max_depth', 1, 9),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 1.0, log=True),
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'gamma': trial.suggest_float('gamma', 1e-8, 1.0, log=True),
        'subsample': trial.suggest_float('subsample', 0.01, 1.0, log=True),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.01, 1.0, log=True),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 1.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 1.0, log=True),
        'random_state': 42,
        'eval_metric': 'logloss'
    }

    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    scores = []
    for train_index, test_index in kf.split(Features_DF, classes_DF):

        # Train test split
        X_train, y_train = Dataset.drop(Class_name, axis=1).iloc[train_index], Dataset[Class_name].iloc[train_index]
        X_test, y_test = Dataset.drop(Class_name, axis=1).iloc[test_index], Dataset[Class_name].iloc[test_index]

        model = XGBClassifier(**params)
        model.fit(X_train, y_train)

        predictions = model.predict_proba(X_test)
        score = roc_auc_score(y_test, predictions[:, 1])
        scores.append(score)
    return np.mean(scores)

##--------------------------- RUNNING SEARCH ----------------------------

if fUseOptuna:
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100)
    BDT_params = study.best_params

else:
    BDT_Classifier = XGBClassifier()
    CV_BDT = GridSearchCV(estimator=BDT_Classifier, param_grid=BDT_params, cv= 5, scoring='roc_auc', verbose=2)
    CV_BDT.fit(Features_DF.iloc[:, :].values, classes_DF.iloc[:, :].values.ravel())
    BDT_params = CV_BDT.best_params_ # BDT

print('Best hyperparameters:', BDT_params)


##--------------------------- SAVING IMPORTANT INFO ----------------------------
Dataset_params = {}
RunConfig_dict = {}

# Creating output dicts:
Dataset_params['DatasetName'] = DatasetName
Dataset_params['Class'] = Class_name
Dataset_params['Features'] = FeaturesToTrain

RunConfig_dict['Dataset'] = Dataset_params
RunConfig_dict["BDT"] = BDT_params

# ______________________________________________________________________________
# Creates directory to save ML run configurations and results

if fCreateNewrun:
    RunNumber = len(next(os.walk(RESULTS_PATH))[1])
    RUN_PATH = RESULTS_PATH+'Run {}'.format(RunNumber)
    os.makedirs(RUN_PATH, exist_ok=True)

    file = open(RUN_PATH+"/README.txt", "w")
    file.write('Description: ' + RunDescription + '\n \n')
    file.write('------------------------------------------------------- \n \n')
    file.write('Run configurations: \n \n')
    file.write(json.dumps(RunConfig_dict, indent=2))
    file.close()

    with open(RUN_PATH+"/RunConfig.pkl", 'wb') as f:
        pickle.dump(RunConfig_dict, f)

    # Updating RunList:
    with open(RESULTS_PATH+"RunList.txt", "a+") as file_object:
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        # Append text at the end of file
        file_object.write("Run {}: {}".format(RunNumber, RunDescription))