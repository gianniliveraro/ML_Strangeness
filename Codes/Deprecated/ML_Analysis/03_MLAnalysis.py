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
# ML analysis code
# ================
#
# BDT Performance Analysis using the test set predictions
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
from sklearn.metrics import confusion_matrix, accuracy_score, mean_absolute_error, roc_curve, precision_recall_curve, roc_auc_score
from sklearn.preprocessing import binarize
import pickle
import json
import time
from matplotlib import pyplot as plt
t0 = time.time() # Initial time

#---------------------------  MAIN CONFIGURATIONS -----------------------------

##----------------------- PATHS AND LOADING SETTINGS----------------------------
MAIN_PATH = '/storage1/liveraro/ML_Strangeness/'
RESULTS_PATH = MAIN_PATH + 'Workflow_Scripts/ML_Analysis/Results/'

print('Which ML Run would you like to load?. Available Runs: \n', os.listdir(RESULTS_PATH))
RunNumber = str (input())
RUN_PATH = RESULTS_PATH+'{}'.format(RunNumber)
# Loading dict with predictions
with open(RUN_PATH+"/RunConfig.pkl", 'rb') as f:
    RunConfig = pickle.load(f)

PredictionsDF = pd.read_parquet(RUN_PATH+"/Predictions.parquet")
#PredictionsDF = PredictionsDF[PredictionsDF.InvMass<4]

print('N signal candidates: ', len(PredictionsDF[PredictionsDF.GroundTruth==1]))
print('N bkg candidates: ', len(PredictionsDF[PredictionsDF.GroundTruth==0]))

# Calculating True Positive Rate (TPR) and False Positive Rate (FPR) for different threshold values
FPR, TPR, thresholds = roc_curve(PredictionsDF['GroundTruth'].values.ravel(), PredictionsDF['Prediction'].values, drop_intermediate=False) 

# Area Under the Curve
auc = roc_auc_score(PredictionsDF['GroundTruth'].values.ravel(), PredictionsDF['Prediction'].values) 

# ROC Curve:
fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(FPR, TPR, label="AUC ="+np.format_float_positional(auc, precision=3))
ax.plot([0,1], [0,1], linestyle='--', label='Random Selection, AUC = 0.5')
ax.set_xlabel('False Positive Rate', fontsize=15)
ax.set_ylabel('True Positive Rate', fontsize=15)
ax.set_title('BDT ROC Curve', fontsize=15)
ax.grid(linestyle='--')
ax.legend(loc='lower right')
plt.savefig(RUN_PATH+'/ROC Curve.png', bbox_inches='tight')
plt.show()

plt.clf() 

# Plot TPR x Threshold

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(thresholds, TPR)
ax.set_xlabel('Decision Threshold', fontsize=15)
ax.set_ylabel('True Positive Rate', fontsize=15)
ax.set_title('TPR x Decision Threshold', fontsize=15)
ax.grid(linestyle='--')
ax.set_xlim((0,1.0))
plt.savefig(RUN_PATH+'/TPR.png', bbox_inches='tight')
plt.show()

plt.clf() 

# Plot FPR x Threshold

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(thresholds, FPR)
ax.set_xlabel('Decision Threshold', fontsize=15)
ax.set_ylabel('False Positive Rate', fontsize=15)
ax.set_title('FPR x Decision Threshold', fontsize=15)
ax.grid(linestyle='--')
ax.set_xlim((0,1.0))
plt.savefig(RUN_PATH+'/FPR.png', bbox_inches='tight')
plt.show()
plt.clf() 

# ML output histogram
fig = plt.figure()
plt.hist(PredictionsDF[PredictionsDF.GroundTruth==0].Prediction, label='Background', bins=100, color='blue', alpha=0.5)
plt.hist(PredictionsDF[PredictionsDF.GroundTruth==1].Prediction, label='Signal', bins=100, color='red', alpha=0.5)
plt.yscale('log')

plt.title('BDT output: candidates probability distribution')
plt.xlabel('BDT output (P)',fontsize='x-large')

plt.ylabel('Counts',fontsize='x-large')
plt.legend(fontsize='x-large')
ax.grid(linestyle='--')
#plt.figtext(0.70, 0.75, r"$\bf{ALICE\/ Performance}$" + '\n Pb-Pb at $\sqrt{s}=5.02$ $TeV$ \n $(0-100)$%', ha='center')
plt.savefig(RUN_PATH+'/ProbabilityPlot.png', bbox_inches='tight')
plt.show()

# Ground-truth Mass histogram
NBins = 500 
xmin = 0.0
xmax = 2.0
overall_range = (PredictionsDF['InvMass'].min(), PredictionsDF['InvMass'].max())
bin_width = (overall_range[1] - overall_range[0]) / NBins
bins = np.arange(overall_range[0], overall_range[1] + bin_width, bin_width)

# Plot
fig = plt.figure()

plt.hist(PredictionsDF[PredictionsDF.GroundTruth==0].InvMass, label='Background', bins=bins, histtype='step', fill=False, 
         align='mid', linewidth=1, density=False, range=(overall_range[0], overall_range[1]))

plt.hist(PredictionsDF[PredictionsDF.GroundTruth==1].InvMass, label='Signal', bins=bins, histtype='step', fill=False, 
         align='mid', linewidth=1, density=False, range=(overall_range[0], overall_range[1]))

plt.yscale('log')
plt.xlim(xmin, xmax)
plt.title('Invariant Mass Distribution')
plt.xlabel('Invariant Mass',fontsize='x-large')
plt.ylabel('Counts',fontsize='x-large')
plt.legend(fontsize='x-large')
ax.grid(linestyle='--')
#plt.figtext(0.70, 0.75, r"$\bf{ALICE\/ Performance}$" + '\n Pb-Pb at $\sqrt{s}=5.02$ $TeV$ \n $(0-100)$%', ha='center')
plt.savefig(RUN_PATH+'/InvMassPlot.png', bbox_inches='tight')
plt.show()
plt.clf()

# ML output Mass histogram
NBins = 2000 
overall_range = (PredictionsDF['InvMass'].min(), PredictionsDF['InvMass'].max())
bin_width = (overall_range[1] - overall_range[0]) / NBins
bins = np.arange(overall_range[0], overall_range[1] + bin_width, bin_width)

# Plot
fig = plt.figure()

plt.hist(PredictionsDF[PredictionsDF.Prediction<=0.5].InvMass, label='P<=0.5', bins=bins, histtype='step', fill=False, 
         align='mid', linewidth=1, density=False, range=(overall_range[0], overall_range[1]))

plt.hist(PredictionsDF[PredictionsDF.Prediction>0.5].InvMass, label='P>0.5', bins=bins, histtype='step', fill=False, 
         align='mid', linewidth=1, density=False, range=(overall_range[0], overall_range[1]))


plt.yscale('log')
plt.xlim(xmin, xmax)
plt.title('Invariant Mass Distribution')
plt.xlabel('Invariant Mass',fontsize='x-large')
plt.ylabel('Counts',fontsize='x-large')
plt.legend(fontsize='x-large')
ax.grid(linestyle='--')
#plt.figtext(0.70, 0.75, r"$\bf{ALICE\/ Performance}$" + '\n Pb-Pb at $\sqrt{s}=5.02$ $TeV$ \n $(0-100)$%', ha='center')
plt.savefig(RUN_PATH+'/MLInvMassPlot.png', bbox_inches='tight')
plt.show()