#!/bin/bash

# MASTER SWITCHES
UseJSON=true
Useconverters=false
StudyName="FindableExercise"

RunMLSelectionOnly=false
RunCompleteSigmaAnalysis=true

# Define input and output names
InputFiles="/Studies/${StudyName}/AO2Ds_O2InputList"
JSONPATH="Studies/${StudyName}/"
OutputName=""

if [ "$RunMLSelectionOnly" = true ]; then
    echo "Running sigma0 Analysis!"
    if [ "$UseJSON" = true ]; then
        export OPTIONS="-b --configuration json://${JSONPATH}SigmaAnalysisTest-config.json --shm-segment-size 10000000000000 --pipeline lambdakzero-mlselection:3 --aod-file @${InputFiles}.txt"
    else 
        export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline lambdakzero-mlselection:3 --aod-file @${InputFiles}.txt"
        
    fi
     
    o2-analysis-lf-lambdakzeromlselection ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} 
    mv dpl-config.json ${JSONPATH}SigmaAnalysisTest-config.json
fi

if [ "$RunSigma0BuilderOnly" = true ]; then
    echo "Work in progress! Nothing will happen :("
     
fi

if [ "$RunCompleteSigmaAnalysis" = true ]; then
    echo "Running sigma0 Analysis ans creating output Tree! Fasten seatbelts!"
    if [ "$UseJSON" = true ]; then
        export OPTIONS="-b --configuration json://${JSONPATH}SigmaCompleteAnalysis-config.json --shm-segment-size 10000000000000 --pipeline sigma-analysis:3 --aod-file @${InputFiles}.txt"
    else
        export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline sigma-analysis:3 --aod-file @${InputFiles}.txt"
        
    fi 
    if [ "$Useconverters" = true ]; then
        o2-analysis-lf-sigmaanalysis ${OPTIONS} | o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzeromlselection ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} | o2-analysis-lf-stradautracksextraconverter ${OPTIONS}
    else
        o2-analysis-lf-sigmaanalysis ${OPTIONS} | o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzeromlselection ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS}
    fi

    mv dpl-config.json ${JSONPATH}SigmaCompleteAnalysis-config.json
fi
