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
# 02_runTreeCreator
# ================
#
# Script to execute the MLSelectionTreeCreator task
# It outputs a flat TTree with candidates 
# Execution command: source 02_runTreeCreator.sh
#
#    Comments, questions, complaints, suggestions?
#    Please write to:
#    gianni.shigeru.setoue.liveraro@cern.ch
#    romain.schotter@cern.ch
#    david.dobrigkeit.chinellato@cern.ch

#----------------------------------------------------
# MASTER SWITCHES
UseJSON=true

# Define input and output names
InputFiles="AO2Ds_ReducedList"
OutputName="MCSigma0GammasTree"


if [ "$UseJSON" = true ]; then
    export OPTIONS="-b --configuration json://TreeCreator-config.json --shm-segment-size 10000000000000 --pipeline lambdakzeromlselection-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0"
else 
    export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline lambdakzeromlselection-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0 --aod-file @${InputFiles}.txt" 
fi

o2-analysis-lf-lambdakzeromlselectiontreecreator ${OPTIONS} | o2-analysis-lf-lambdakzeropid ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} | o2-analysis-lf-cascadespawner ${OPTIONS} | o2-analysis-lf-stradautracksextraconverter ${OPTIONS} | o2-analysis-lf-stradautrackstofpidconverter ${OPTIONS} | o2-analysis-lf-v0coresconverter ${OPTIONS}

mv dpl-config.json TreeCreator-config.json
echo "Moving outputs to: ~/ML_Strangeness/Dataset/Interim..."
mv AnalysisResults_trees.root ~/ML_Strangeness/Dataset/Interim/${OutputName}.root
mv AnalysisResults.root ~/ML_Strangeness/Dataset/Interim/${OutputName}Histograms.root



