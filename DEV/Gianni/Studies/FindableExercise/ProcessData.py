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
# This code reads a flat TTree and creates a parquet file
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

##--------------------------------- DATASET ----------------------------------
DatasetName = 'AnalysisResults_FindableTreeGammas' # input root flat TTree 

#--------------------------------- LOADING DATA ------------------------------
rfile = uproot.open("{}.root".format(DatasetName))

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
print("\n-------------------------------------------")
print('[INFO]: The input dataset has a total of {} candidates'.format(len(dataframeFinal)))

dataframeFinal.to_parquet("{}.parquet".format(DatasetName))

t1 = time.time() - t0
print("\n_________________________________________")
print("Total time elapsed (min): ", t1/60)
print("_________________________________________")