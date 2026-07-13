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
fSplitTrainTest = False # if true, perform train/test/validation split. 
fSeparateAO2Ds = False   # else if true, merge signal and bacgkround ao2ds, then perform perform train/test/validation split
                        # else, the entire input dataset is converted to an unique .parquet file

# Number of signal and bkg candidates in the total dataset (before splitting)
NSignal = 100000
NBkg = 100000


##--------------------------------- PATHS ------------------------------------
# Change these paths to ones in your own machine!
MAIN_PATH = '/home/jesgum/ML_Strangeness/'
TABLES_TO_KEEP = [] # Tables with training variables that needs to be accessed e.g. O2tracks

##--------------------------------- DATASET ----------------------------------
DatasetName = 'AO2DMerged' # .root TTree from O2Physics 
OutputPrefix = "MCharm"

SignalFile = 'AO2DMerged_Signal'
BackgroundFile = 'AO2DMerged_Background'

Class_name = "fIsCorrectlyAssoc" # Class name (target)


def filter_df(data_frame):
  """
  Filter columns; e.g.
  Geometry = 1
  data_frame = data_frame[(data_frame.fLUTConfigId == Geometry)]
  """
  return data_frame

def create_pd_df(dataset_name, n_req_cands):
  rfile = uproot.open(MAIN_PATH+"{}".format(dataset_name))

  # Get the list of directories (TDirectory) in the ROOT file
  keys = rfile.keys()


  if not TABLES_TO_KEEP:
      directory_names = [x.split(';')[0] for x in keys if "/" not in x]
      group_names = [x.split(';')[0] for x in keys if "/" in x]
  else:
      directory_names = [x.split(';')[0] for x in keys if '/' not in x and any(t in x for t in TABLES_TO_KEEP)]
      group_names = [x.split(';')[0] for x in keys if '/' in x and any(t in x for t in TABLES_TO_KEEP)]

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

    if len(filter_df(dataframeFinal)) > n_req_cands:
      return filter_df(dataframeFinal)

  print("\n_________________________________________")
  print('[INFO]: Dataframe created for {}'.format(dataset_name))

  return filter_df(dataframeFinal)

#--------------------------------- PROCESSING ---------------------------------
def main():
  if fSplitTrainTest:

    # LOADING DATA 
    dataframeFinal = create_pd_df(DatasetName, NSignal)

    print("\n-------------------------------------------")
    print('[INFO]: The input dataset has a total of {} signal candidates, {} will be selected: '.format(len(dataframeFinal[dataframeFinal[Class_name]==True]), NSignal))
    print('[INFO]: The input dataset has a total of {} bkg candidates, {} will be selected'.format(len(dataframeFinal[dataframeFinal[Class_name]==False]), NBkg))

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

  elif fSeparateAO2Ds:
    # LOADING DATA 

    dataframeSignalFinal = create_pd_df(SignalFile, NSignal)
    dataframeBkgFinal = create_pd_df(BackgroundFile, NBkg)

    print("\n-------------------------------------------")
    print('[INFO]: The input dataset has a total of {} signal candidates, {} will be selected: '.format(len(dataframeSignalFinal), NSignal))
    print('[INFO]: The input dataset has a total of {} Bkg candidates, {} will be selected'.format(len(dataframeBkgFinal), NBkg))
    
    # Creating training, validation and testing sets:
    SignalCandidates = dataframeSignalFinal.sample(n=NSignal, random_state=42)
    BkgCandidates = dataframeBkgFinal.sample(n=NBkg, random_state=42)
    SignalCandidates["fIsCorrectlyAssoc"] = True
    BkgCandidates["fIsCorrectlyAssoc"] = False

    # Split signal
    Signal_TrainVal, Signal_Test = train_test_split(SignalCandidates, test_size=0.30, random_state=42)
    Signal_Train, Signal_Val = train_test_split(Signal_TrainVal, test_size=0.10, random_state=42)

    # Split background
    Bkg_TrainVal, Bkg_Test = train_test_split(BkgCandidates, test_size=0.30, random_state=42)
    Bkg_Train, Bkg_Val = train_test_split(Bkg_TrainVal, test_size=0.10, random_state=42)

    # Merge splits
    Data_Train = pd.concat([Signal_Train, Bkg_Train], axis=0).sample(frac=1, random_state=42)
    Data_Val = pd.concat([Signal_Val, Bkg_Val], axis=0).sample(frac=1, random_state=42)
    Data_Test = pd.concat([Signal_Test, Bkg_Test], axis=0).sample(frac=1, random_state=42)

    # Save datasets
    Data_Train.to_parquet(MAIN_PATH + f"Dataset/Processed/{OutputPrefix}_Train.parquet")
    Data_Val.to_parquet(MAIN_PATH + f"Dataset/Processed/{OutputPrefix}_Val.parquet")
    Data_Test.to_parquet(MAIN_PATH + f"Dataset/Processed/{OutputPrefix}_Test.parquet")

    # Optional CSV for validation
    Data_Val.to_csv(MAIN_PATH + f"Dataset/Processed/{OutputPrefix}_Val.csv")

    print("\n-------------------------------------------")
    print("[INFO]: Train set class distribution:\n{}".format(Data_Train["fClass"].value_counts()))

    print("\n-------------------------------------------")
    print('[INFO]: Train set total size: {}'.format(len(Data_Train)))
    print('[INFO]: Val set total size: {}'.format(len(Data_Val)))
    print('[INFO]: Test set total size: {}'.format(len(Data_Test)))

  else:

    dataframeFinal = create_pd_df(DatasetName)
    print("\n-------------------------------------------")
    print('[INFO]: The input dataset has a total of {} signal candidates'.format(len(dataframeFinal[dataframeFinal[Class_name]==True])))
    print('[INFO]: The input dataset has a total of {} Bkg candidates'.format(len(dataframeFinal[dataframeFinal[Class_name]==False])))

    dataframeFinal.to_parquet("{}.parquet".format(DatasetName))
    dataframeFinal.to_csv("{}.csv".format(DatasetName))

  t1 = time.time() - t0
  print("\n_________________________________________")
  print("Total time elapsed (min): ", t1/60)
  print("_________________________________________")

if __name__ == "__main__":
  main()