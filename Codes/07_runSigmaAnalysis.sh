#!/bin/bash

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
# 07_runSigmaAnalysis
# ================
#
# Script to execute sigmaanalysis task  
# Execution command: source 07_runSigmaAnalysis.sh
#
#    Comments, questions, complaints, suggestions?
#    Please write to:
#    gianni.shigeru.setoue.liveraro@cern.ch
#    romain.schotter@cern.ch
#    david.dobrigkeit.chinellato@cern.ch

#----------------------------------------------------

# MASTER SWITCHES
UseJSON=false

RunMLSelectionOnly=false # TODO
RunSigmaBuilderOnly=false # TODO
RunCompleteSigmaAnalysis=true

# Define input and output names
InputFiles="AO2Ds_ReducedList" # .txt
OutputTreeName="SigmaCandidatesTree" # # TODO

if [ "$RunCompleteSigmaAnalysis" = true ]; then
    echo "Running sigma0 Analysis and creating output Tree! Fasten seatbelts!"
    if [ "$UseJSON" = true ]; then
        export OPTIONS="-b --configuration json://SigmaCompleteAnalysis-config.json --shm-segment-size 10000000000000 --pipeline sigma-analysis:3 --aod-file @${InputFiles}.txt"
    else
        export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline sigma-analysis:3 --aod-file @${InputFiles}.txt"
        
    fi 
    o2-analysis-lf-sigmaanalysis ${OPTIONS} | o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzeromlselection ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} | o2-analysis-lf-stradautracksextraconverter ${OPTIONS}
    mv dpl-config.json SigmaCompleteAnalysis-config.json
fi
