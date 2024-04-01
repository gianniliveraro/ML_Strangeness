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
# ================
#
# This code reads a flat TTree and creates training and testing samples for ML
# TODO: modify code to receive a TTree that passed through aod-merger!!
#
#    Comments, questions, complaints, suggestions?
#    Please write to:
#    gianni.shigeru.setoue.liveraro@cern.ch
#    romain.schotter@cern.ch
#    david.dobrigkeit.chinellato@cern.ch

#____________________________
# Imports
import numpy as np
import pandas as pd
import uproot
import os
from sklearn.model_selection import train_test_split
import time
t0 = time.time() # Initial time

#---------------------------  MAIN CONFIGURATIONS ----------------------------

# Number of signal and bkg candidates for training/test
NSignal = 100000
NBkg = 100000
##--------------------------------- PATHS ------------------------------------
MAIN_PATH = '/storage1/liveraro/ML_Strangeness/'
RESULTS_PATH = MAIN_PATH + '/Results/'

##--------------------------------- DATASET ----------------------------------
DatasetName = 'MCCandidatesTree.root' # root flat TTree 
Target = "Lambda" # Target particle (class). Options: Lambda, Gamma (In the future: KZeroShort, AntiLambda) 
Class_name = 'fIs'+Target

#--------------------------------- LOADING DATA ------------------------------
rfile = uproot.open(MAIN_PATH+"Dataset/Interim/{}.root".format(DatasetName))

# Get the list of directories (TDirectory) in the ROOT file
keys = rfile.keys()
directory_names = [x.split(';')[0] for x in keys if "/" not in x ]
group_names = [x.split(';')[0] for x in keys if "/" in x ]
Subgroups = np.unique(np.array([x.split('/')[1] for x in group_names]))

# Creating Pandas dataframes from TTrees 
iteraction = 0
for dir in group_names:

  tree = rfile[dir]

  if iteraction==0:
    dataframeFinal = tree.arrays(library='pd')

  else:
    dataframe = tree.arrays(library='pd')
    dataframeFinal = pd.concat([dataframeFinal, dataframe],axis=0)

  iteraction = iteraction + 1
#--------------------------------- PROCESSING ---------------------------------
SignalCandidates = dataframeFinal[dataframeFinal[Class_name]==True].sample(n=NSignal, random_state=42) 
BkgCandidates = dataframeFinal[dataframeFinal[Class_name]==False].sample(n=NBkg, random_state=42) 
TotalCandidates = pd.concat([SignalCandidates, BkgCandidates], axis=0).sample(frac=1) # merging and shuffling

print('Total of {} signal candidates'.format(NSignal))
print('Total of {} Bkg candidates'.format(len(BkgCandidates)))

# Creating training and testing sets:
Data_Train, Data_Test = train_test_split(TotalCandidates, test_size=0.30, random_state=42, stratify=TotalCandidates[Class_name])

#----------------------------- SAVING DATASETS ---------------------------------
Data_Train.to_parquet(MAIN_PATH+"Dataset/Processed/{}_Train.parquet".format(Target))
Data_Test.to_parquet(MAIN_PATH+"Dataset/Processed/{}_Test.parquet".format(Target))

# End
t1 = time.time() - t0
print("_________________________________________")
print("Total time elapsed (min): ", t1/60)
print("_________________________________________")