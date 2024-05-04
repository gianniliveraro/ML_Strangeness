#!/bin/bash

# MASTER SWITCHES
UseJSON=true

RunSigmaAnalysisOnly=false
RunCompleteSigmaAnalysis=true

# Define input and output names
InputFiles="AO2Ds_ReducedList"
OutputName="SigmaCandidatesTree"

if [ "$RunSigmaAnalysisOnly" = true ]; then
    echo "Running sigma0 Analysis!"
    if [ "$UseJSON" = true ]; then
        export OPTIONS="-b --configuration json://SigmaAnalysisTest-config.json --shm-segment-size 10000000000000 --pipeline lambdakzero-mlselection:3 --aod-file @${InputFiles}.txt"
    else 
        export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline lambdakzero-mlselection:3 --aod-file @${InputFiles}.txt"
        
    fi
     
    o2-analysis-lf-lambdakzeromlselection ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} 
    mv dpl-config.json SigmaAnalysisTest-config.json
fi 

if [ "$RunCompleteSigmaAnalysis" = true ]; then
    echo "Running sigma0 Analysis ans creating output Tree! Fasten seatbelts!"
    if [ "$UseJSON" = true ]; then
        export OPTIONS="-b --configuration json://SigmaCompleteAnalysis-config.json --shm-segment-size 10000000000000 --pipeline sigma-analysis:3 --aod-file @${InputFiles}.txt"
    else
        export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline sigma-analysis:3 --aod-file @${InputFiles}.txt"
        
    fi 
    o2-analysis-lf-sigmaanalysis ${OPTIONS} | o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzeromlselection ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} | o2-analysis-lf-stradautracksextraconverter ${OPTIONS}
    mv dpl-config.json SigmaCompleteAnalysis-config.json
fi
