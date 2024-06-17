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
from concurrent.futures import ThreadPoolExecutor
t0 = time.time() # Initial time

#---------------------------  MAIN CONFIGURATIONS ----------------------------
fSplitTrainTest = False # if true, perform train test split. If false, the entire input dataset is converted to .parquet
fIsStratified = False
StudyName = "TrainingGeneralMLModels"

# Please, include a short description of the output dataset:
DatasetDescription = "Dataset with...." # TODO

# Number of signal and bkg candidates for training/test. Set these values if fChooseNCandidates==True
fChooseNCandidates = False # Is this is false, them NBkg=3*NSignal
NSignal = 100000
NBkg = 300000

##--------------------------- SELECT HYPOTHESIS ------------------------------------
# // 1: Consistent with Lambda only, 2: Consistent with Anti-Lambda only
# // 3: Consistent with Lambda and Anti-Lambda, 4: Consistent with Gamma only
# // 5: Consistent with Lambda and Gamma, 6: Consistent with Anti-Lambda and Gamma
# // 7: Consistent with Lambda, Anti-Lambda, and Gamma, 8: Consistent with K0Short only
# // 9: Consistent with Lambda and K0Short, 10: Consistent with Anti-Lambda and K0Short
# // 11: Consistent with Lambda, Anti-Lambda, and K0Short, 12: Consistent with Gamma and K0Short
# // 13: Consistent with Lambda, Gamma, and K0Short, 14: Consistent with Anti-Lambda, Gamma, and K0Short
# // 15: Consistent with Lambda, Anti-Lambda, Gamma, and K0Short
NSelHypothesis = [2,3] 

##--------------------------------- PATHS ------------------------------------
# Change these paths to ones in your own machine!
MAIN_PATH = '/storage1/liveraro/ML_Strangeness/'
SAVE_PATH = MAIN_PATH+'Dataset/Processed/{}/'.format(StudyName)

os.makedirs(SAVE_PATH, exist_ok=True) # Working directory

##--------------------------------- DATASET ----------------------------------
DatasetName = 'SigmaAnalysisTree' #'MCNewCandidatesTree' # input root flat TTree 
Target = "Gamma" # Target particle (class). Options: Lambda, Gamma, KZeroShort, AntiLambda. Set this if fSplitTrainTest==True!
Class_name = 'fIs'+Target


#--------------------------------- LOADING DATA ------------------------------
rfile = uproot.open(MAIN_PATH+"Dataset/Interim/{}/{}.root".format(StudyName, DatasetName))

# Get the list of directories (TDirectory) in the ROOT file
keys = rfile.keys()
directory_names = [x.split(';')[0] for x in keys if "/" not in x ]
group_names = [x.split(';')[0] for x in keys if "/" in x ]
Subgroups = np.unique(np.array([x.split('/')[1] for x in group_names]))

Niteractions = len(group_names)
# # Creating Pandas dataframes from TTrees 
# iteraction = 0
# for dir in group_names:
#   tree = rfile[dir]

#   if iteraction==0:
#     dataframeFinal = tree.arrays(library='pd')

#   else:
#     dataframe = tree.arrays(library='pd')
#     dataframeFinal = pd.concat([dataframeFinal, dataframe],axis=0)
#   print('\r Iteraction {} out {}'.format(iteraction, Niteractions), end="")
#   iteraction = iteraction + 1

# Preallocate a list to collect dataframes
dataframes = []

# Creating Pandas dataframes from TTrees
for iteraction, dir in enumerate(group_names):
    tree = rfile[dir]
    dataframe = tree.arrays(library='pd')
    dataframes.append(dataframe)
    print('\r Iteraction {} out of {}'.format(iteraction + 1, Niteractions), end="")

# Concatenate all dataframes at once
dataframeFinal = pd.concat(dataframes, axis=0)

#--------------------------------- PROCESSING ---------------------------------
if fSplitTrainTest:

  if fIsStratified:

    # Using main hypothesis
    SignalLikeCandidates = dataframeFinal[dataframeFinal.fSelHypothesis.isin(NSelHypothesis)]

    if fChooseNCandidates:
      print("\n-------------------------------------------")
      print('[INFO]: The input dataset has a total of {} signal candidates, {} will be selected: '.format(len(SignalLikeCandidates[SignalLikeCandidates[Class_name]==True]), NSignal))
      print('[INFO]: The input dataset has a total of {} Bkg candidates, {} will be selected'.format(len(SignalLikeCandidates[SignalLikeCandidates[Class_name]==False]), NBkg))

    else:
      NSignal = len(SignalLikeCandidates[SignalLikeCandidates[Class_name]==True])
      NBkg = len(SignalLikeCandidates[SignalLikeCandidates[Class_name]==False])

      if int(3*NSignal)<NBkg:
        NBkg = 3*NSignal
        
      print("\n-------------------------------------------")
      print('[INFO]: The input dataset has a total of {} signal candidates, {} will be selected: '.format(NSignal, NSignal))
      print('[INFO]: The input dataset has a total of {} Bkg candidates, {} will be selected'.format(len(SignalLikeCandidates[SignalLikeCandidates[Class_name]==False]), NBkg))

    SignalCandidates = SignalLikeCandidates[SignalLikeCandidates[Class_name]==True].sample(n=NSignal, random_state=42) 
    BkgCandidates = SignalLikeCandidates[SignalLikeCandidates[Class_name]==False].sample(n=NBkg, random_state=42) 

    # From other hypothesis
    BkgLikeCandidates = dataframeFinal[~dataframeFinal.fSelHypothesis.isin(NSelHypothesis)].sample(frac=1).sample(n=int(NBkg*0.1), random_state=42)

    # Joiniing all candidates
    TotalCandidates = pd.concat([SignalCandidates, BkgCandidates, BkgLikeCandidates], axis=0).sample(frac=1) # merging and shuffling

  else: 

    if fChooseNCandidates:
      print("\n-------------------------------------------")
      print('[INFO]: The input dataset has a total of {} signal candidates, {} will be selected: '.format(len(dataframeFinal[dataframeFinal[Class_name]==True]), NSignal))
      print('[INFO]: The input dataset has a total of {} Bkg candidates, {} will be selected'.format(len(dataframeFinal[dataframeFinal[Class_name]==False]), NBkg))

    else: 

      NSignal = len(dataframeFinal[dataframeFinal[Class_name]==True])
      NBkg = 3*NSignal
      print("\n-------------------------------------------")
      print('[INFO]: The input dataset has a total of {} signal candidates, {} will be selected: '.format(NSignal, NSignal))
      print('[INFO]: The input dataset has a total of {} Bkg candidates, {} will be selected'.format(len(dataframeFinal[dataframeFinal[Class_name]==False]), NBkg))
      
    SignalCandidates = dataframeFinal[dataframeFinal[Class_name]==True].sample(n=NSignal, random_state=42) 
    BkgCandidates = dataframeFinal[dataframeFinal[Class_name]==False].sample(n=NBkg, random_state=42) 
    TotalCandidates = pd.concat([SignalCandidates, BkgCandidates], axis=0).sample(frac=1) # merging and shuffling
    
  # Creating training, validation and testing sets:
  Data_TrainVal, Data_Test = train_test_split(TotalCandidates, test_size=0.30, random_state=42, stratify=TotalCandidates[Class_name])
  Data_Train, Data_Val = train_test_split(Data_TrainVal, test_size=0.10, random_state=42, stratify=Data_TrainVal[Class_name])

  #----------------------------- SAVING DATASETS ---------------------------------
  Data_Train.to_parquet(SAVE_PATH+"{}_Train.parquet".format(Target))
  Data_Val.to_parquet(SAVE_PATH+"{}_Val.parquet".format(Target))
  Data_Test.to_parquet(SAVE_PATH+"{}_Test.parquet".format(Target))

  #--------------------------------- END ---------------------------------
  print("\n-------------------------------------------")
  print('[INFO]: Train set total size: {}'.format(len(Data_Train)))
  print('[INFO]: Val set total size: {}'.format(len(Data_Val)))
  print('[INFO]: Test set total size: {}'.format(len(Data_Test)))

else: 
  print("\n-------------------------------------------")
  print('[INFO]: The input dataset has a total of {} signal candidates'.format(len(dataframeFinal[dataframeFinal[Class_name]==True])))
  print('[INFO]: The input dataset has a total of {} Bkg candidates'.format(len(dataframeFinal[dataframeFinal[Class_name]==False])))
  dataframeFinal.to_parquet(SAVE_PATH+"{}.parquet".format(DatasetName))


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