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
# 03_ProcessData
# ================
#
# This code reads a flat TTree and creates training and testing samples for ML
# TODO: Create a dataset description file!!
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
fSplitTrainTest = False # if true, perform train test split. If false, the entire input dataset is converted to .parquet

# Please, include a short description of the output dataset:
DatasetDescription = "Dataset with...."

# Number of signal and bkg candidates for training/test. Set these values if fSplitTrainTest==True
NSignal = 200000
NBkg = 200000

##--------------------------------- PATHS ------------------------------------
# Change these paths to ones in your own machine!
MAIN_PATH = '/storage1/liveraro/ML_Strangeness/'

##--------------------------------- DATASET ----------------------------------
DatasetName = 'MCSigma0FindableLambdasTree' # input root flat TTree 
Target = "Lambda" # Target particle (class). Options: Lambda, Gamma, KZeroShort, AntiLambda. Set this if fSplitTrainTest==True!
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
if fSplitTrainTest:
  print("\n-------------------------------------------")
  print('[INFO]: The input dataset has a total of {} signal candidates, {} will be selected: '.format(len(dataframeFinal[dataframeFinal[Class_name]==True]), NSignal))
  print('[INFO]: The input dataset has a total of {} Bkg candidates, {} will be selected'.format(len(dataframeFinal[dataframeFinal[Class_name]==False]), NBkg))

  SignalCandidates = dataframeFinal[dataframeFinal[Class_name]==True].sample(n=NSignal, random_state=42) 
  BkgCandidates = dataframeFinal[dataframeFinal[Class_name]==False].sample(n=NBkg, random_state=42) 
  TotalCandidates = pd.concat([SignalCandidates, BkgCandidates], axis=0).sample(frac=1) # merging and shuffling

  # Creating training, validation and testing sets:
  Data_TrainVal, Data_Test = train_test_split(TotalCandidates, test_size=0.30, random_state=42, stratify=TotalCandidates[Class_name])
  Data_Train, Data_Val = train_test_split(Data_TrainVal, test_size=0.10, random_state=42, stratify=Data_TrainVal[Class_name])

  #----------------------------- SAVING DATASETS ---------------------------------
  Data_Train.to_parquet(MAIN_PATH+"Dataset/Processed/{}_Train.parquet".format(Target))
  Data_Val.to_parquet(MAIN_PATH+"Dataset/Processed/{}_Val.parquet".format(Target))
  Data_Test.to_parquet(MAIN_PATH+"Dataset/Processed/{}_Test.parquet".format(Target))

  #--------------------------------- END ---------------------------------
  print("\n-------------------------------------------")
  print('[INFO]: Train set total size: {}'.format(len(Data_Train)))
  print('[INFO]: Val set total size: {}'.format(len(Data_Val)))
  print('[INFO]: Test set total size: {}'.format(len(Data_Test)))

else: 
  print("\n-------------------------------------------")
  print('[INFO]: The input dataset has a total of {} signal candidates'.format(len(dataframeFinal[dataframeFinal[Class_name]==True])))
  print('[INFO]: The input dataset has a total of {} Bkg candidates'.format(len(dataframeFinal[dataframeFinal[Class_name]==False])))
  dataframeFinal.to_parquet(MAIN_PATH+"Dataset/Processed/{}.parquet".format(DatasetName))


# # Updating RunList:
# with open(RESULTS_PATH+"RunList.txt", "a+") as file_object:
#     file_object.seek(0)
#     # If file is not empty then append '\n'
#     data = file_object.read(100)
#     if len(data) > 0 :
#         file_object.write("\n")
#     # Append text at the end of file
#     file_object.write("Run {}: {}".format(RunNumber, RunDescription))

t1 = time.time() - t0
print("\n_________________________________________")
print("Total time elapsed (min): ", t1/60)
print("_________________________________________")