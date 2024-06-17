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
# 00_DownloadData
# ================
#
# This script downloads datasets from the Hyperloop system (run it inside O2Physics environment)
# Original script by Nicolò Jacazio
# Modified by Gianni S. S. Liveraro
#
#    Comments, questions, complaints, suggestions?
#    Please write to:
#    gianni.shigeru.setoue.liveraro@cern.ch
#    romain.schotter@cern.ch
#    david.dobrigkeit.chinellato@cern.ch
#____________________________
# Imports
import os
import json
import subprocess
import xml.etree.ElementTree as ET
import numpy as np 
import time
t0 = time.time() # Initial time
#---------------------------  MAIN CONFIGURATIONS ----------------------------
# Global Variables
VERBOSE_MODE = False
DRY_MODE_RUNNING = False
fDOWNLOAD_FILES=True
TRAIN_ID = 219304 
OutputDirectoryName = 'LF_LHC24d2b_pass3_Strangeness' #  Choose the name of the download directory

##--------------------------------- PATHS ------------------------------------
# Change these paths to ones in your own machine!
MAIN_PATH = '/storage1/liveraro/ML_Strangeness/'
DOWNLOAD_PATH = MAIN_PATH + "Dataset/Raw/{}/".format(OutputDirectoryName)

# Creating directory to save files
os.makedirs(DOWNLOAD_PATH, exist_ok=True) 

alien_path="https://alimonitor.cern.ch/alihyperloop-data/trains/train.jsp?train_id={}".format(TRAIN_ID)
key_file="userkey.pem"
cert_file="usercert.pem"

#---------------------------- HELPER FUNCTIONS ----------------------------
def run_cmd(cmd):
    """Run shell commands."""
    cmd = cmd.split()
    run_result = subprocess.run(cmd, capture_output=not VERBOSE_MODE)
    return run_result

def find_paths(cmd):
    """Run shell command to find and list paths."""
    cmd = cmd.split()
    result = subprocess.run(cmd, capture_output=True, text=True)
    output_lines = result.stdout.split('\n')
    # Remove any empty lines from the output
    output_lines = [line.strip() for line in output_lines if line.strip()]
    return output_lines

def get_AO2D_paths(hyperpath, merge_status):
    """Get paths of AO2D files."""
    if merge_status=="done":
        cmdAOD = f"alien_find {hyperpath}/AOD/ {'AO2D.root'}"
        cmdAnalysisResults = f"alien_find {hyperpath}/AOD/ {'AnalysisResults.root'}"
    else:
        cmdAOD = f"alien_find {hyperpath} {'AO2D.root'}"
        cmdAnalysisResults = f"alien_find {hyperpath} {'AnalysisResults.root'}"

    AOD_paths = find_paths(cmdAOD)
    AR_paths = find_paths(cmdAnalysisResults)
    return AOD_paths, AR_paths 

def copy_from_alien(alienpathAO2D, alienpathAR, OutputDir, FileNumber):
        cmdAOD = f"alien_cp -q {alienpathAO2D} file:{OutputDir}/AO2D_{FileNumber}.root"
        cmdAR = f"alien_cp -q {alienpathAR} file:{OutputDir}/AnalysisResults_{FileNumber}.root"
        run_cmd(cmdAOD)
        run_cmd(cmdAR)

def get_Output_list(train_id=188604, OutputDir="/.", alien_path="https://alimonitor.cern.ch/alihyperloop-data/trains/train.jsp?train_id=", key_file="userkey.pem", cert_file="usercert.pem"):
    """Gets JSON file to lists main output directories in AliMonitor."""
    out_name = os.path.join(OutputDir, f"HyperloopID_{train_id}.json")
    if not os.path.isfile(key_file) or not os.path.isfile(cert_file):
        print("Cannot find key or cert file.")
        return []

    if not os.path.isfile(out_name):
        download_cmd = f"curl --key {key_file} --cert {cert_file} --insecure {alien_path}{train_id} -o {out_name}"
        print("run command:", download_cmd)
        run_cmd(download_cmd)

    with open(out_name) as json_data:
        data = json.load(json_data)
        # Extract the information inside the "outputdir" key as a list
        Mainpaths = [job['outputdir'] for job in data['jobResults']]
        MergeStates = [merge['merge_state'] for merge in data['jobResults']]
        RunNumbers = [runnumber['run'] for runnumber in data['jobResults']]
    return Mainpaths, MergeStates, RunNumbers

#--------------------------------  EXECUTION ----------------------------
def main():
    # Get hyperloop jobs path:
    HY_PATH, MERGE_STATE, RUN_NUMBER = get_Output_list(train_id=TRAIN_ID, OutputDir=DOWNLOAD_PATH)
    
    with open(DOWNLOAD_PATH+'RunNumbers.txt', 'w') as file:
            for run in RUN_NUMBER:
                file.write(str(run)+"\n")
            file.close()
    
    # Loop to count and list files only
    JOB_Counter = 0
    Ao2DFileList = []
    ARFileList = []
    for i in HY_PATH:
        # Get paths of AO2D files
        Merge_Status = MERGE_STATE[JOB_Counter]
        ao2d_paths, ar_paths = get_AO2D_paths(i, Merge_Status)
        Ao2DFileList.extend(ao2d_paths)
        ARFileList.extend(ar_paths)
        JOB_Counter = JOB_Counter + 1
    NTotalAO2Ds = len(Ao2DFileList)

    # Loop to download files
    if fDOWNLOAD_FILES:
        JOB_Counter = 0
        FILE_Counter = 0
        OutputPATHS = []
        
        for i in HY_PATH:
            # Get paths of AO2D files
            Merge_Status = MERGE_STATE[JOB_Counter]
            ao2d_paths, ar_paths = get_AO2D_paths(i, Merge_Status)
            PATH_Counter = 0
            for j in ao2d_paths:
                copy_from_alien(j, ar_paths[PATH_Counter], DOWNLOAD_PATH, FILE_Counter)
                OutputPATHS.append(str(DOWNLOAD_PATH)+"AO2D_{}.root".format(FILE_Counter))
                PATH_Counter = PATH_Counter+1
                FILE_Counter = FILE_Counter + 1
                print('\r FILE {} out {}'.format(FILE_Counter, NTotalAO2Ds), end="")

        # Write the file paths to the text file
        with open(DOWNLOAD_PATH+'input.txt', 'w') as file:
            for path in OutputPATHS:
                file.write(str(path)+"\n")
            file.close()
    
    # End
    t1 = time.time() - t0
    print("_________________________________________")
    print("Total time elapsed (min): ", t1/60)
    print("_________________________________________")


if __name__ == "__main__":
    main()


