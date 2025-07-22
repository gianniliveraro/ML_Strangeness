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
# SplitAO2Ds
# ================
#
# This is a simple script to split the AO2D files between those:
# 1. used exclusively to ML Training/Test workflow
# 2. used exclusively to ML inference inside O2Physics
#
# !! In principle, this is meant to be used specially if you download several AO2Ds from Grid !!
#
#    Comments, questions, complaints, suggestions?
#    Please write to:
#    gianni.shigeru.setoue.liveraro@cern.ch
#    romain.schotter@cern.ch
#    david.dobrigkeit.chinellato@cern.ch
#____________________________
# Imports
import os
import numpy as np 
import random

#---------------------------  MAIN CONFIGURATIONS ----------------------------

## Fraction of AO2D files that will be used in the ML Workflow
Fraction = 0.1 

## input list with all AO2Ds
input_file = "input.txt" 

## Output file names
output_file_1 = "AO2Ds_MLInputList.txt" # List for ML Workflow
output_file_2 = "AO2Ds_O2InputList.txt" # List for O2 workflow

##--------------------------------- PATHS ------------------------------------
# Change these paths to ones in your own machine!
DatasetDirectory = "LF_LHC23k6e_pass2_Strangeness"
MAIN_PATH = '~/ML_Strangeness/'
DATA_PATH = MAIN_PATH + "Dataset/Raw/{}/".format(DatasetDirectory)

#---------------------------- HELPER FUNCTIONS ----------------------------

def split_file_paths(input_file, output_file_1, output_file_2, frac):
    with open(input_file, 'r') as f:
        paths = f.readlines()
    
    random.shuffle(paths)
    
    split_index = int(len(paths) * frac)
    group_1 = paths[:split_index]
    group_2 = paths[split_index:]
    
    with open(output_file_1, 'w') as f:
        f.writelines(group_1)
    
    with open(output_file_2, 'w') as f:
        f.writelines(group_2)

#--------------------------------  EXECUTION ----------------------------

split_file_paths(DATA_PATH+input_file, output_file_1, output_file_2, Fraction)



