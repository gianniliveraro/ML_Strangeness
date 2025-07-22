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
# ProcessData
# ================
#
# This code reads a TTree and creates training and testing samples for ML
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
fSplitTrainTest = True # if true, perform train/test/validation split. If false, the entire input dataset is converted to an unique .parquet file

# Number of signal and bkg candidates in the total dataset (before splitting)
NSignal = 50000 
NBkg = 50000 

##--------------------------------- PATHS ------------------------------------
# Change these paths to ones in your own machine!
MAIN_PATH = '/storage1/liveraro/ML_Strangeness/'

##--------------------------------- DATASET ----------------------------------
DatasetName = 'AO2D_example' # .root TTree from O2Physics 
OutputPrefix = "Example"
Class_name = "fIsCorrectlyAssoc" # Class name (target)

#--------------------------------- LOADING DATA ------------------------------
rfile = uproot.open(MAIN_PATH+"Dataset/Raw/{}.root".format(DatasetName))

# Get the list of directories (TDirectory) in the ROOT file
keys = rfile.keys()
directory_names = [x.split(';')[0] for x in keys if "/" not in x ]
group_names = [x.split(';')[0] for x in keys if "/" in x ]
Subgroups = np.unique(np.array([x.split('/')[1] for x in group_names]))

print("\n_________________________________________")
print('[INFO]: The input dataset has {} directories'.format(len(directory_names)))
print('[INFO]: The input dataset has {} subgroups'.format(len(Subgroups)))
print('[INFO]: The input dataset has {} groups'.format(len(group_names)))
print('[INFO]: The input dataset has {} keys'.format(len(keys)))

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
  Data_Train.to_parquet(MAIN_PATH+"Dataset/Processed/{}_Train.parquet".format(OutputPrefix))
  Data_Val.to_parquet(MAIN_PATH+"Dataset/Processed/{}_Val.parquet".format(OutputPrefix))
  Data_Test.to_parquet(MAIN_PATH+"Dataset/Processed/{}_Test.parquet".format(OutputPrefix))
  Data_Val.to_csv(MAIN_PATH+"Dataset/Processed/{}_Val.csv".format(OutputPrefix)) # Activate this line if you want to take a look on a .csv file


  #--------------------------------- END -----------------------------------------
  print("\n-------------------------------------------")
  print('[INFO]: Train set total size: {}'.format(len(Data_Train)))
  print('[INFO]: Val set total size: {}'.format(len(Data_Val)))
  print('[INFO]: Test set total size: {}'.format(len(Data_Test)))

else: 

  print("\n-------------------------------------------")
  print('[INFO]: The input dataset has a total of {} signal candidates'.format(len(dataframeFinal[dataframeFinal[Class_name]==True])))
  print('[INFO]: The input dataset has a total of {} Bkg candidates'.format(len(dataframeFinal[dataframeFinal[Class_name]==False])))

  dataframeFinal.to_parquet("{}.parquet".format(DatasetName))
  dataframeFinal.to_csv("{}.csv".format(DatasetName))

t1 = time.time() - t0
print("\n_________________________________________")
print("Total time elapsed (min): ", t1/60)
print("_________________________________________")