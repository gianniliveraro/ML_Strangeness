#!/bin/bash

# MASTER SWITCHES
UseJSON=false

RunSigmaAnalysisOnly=true
RunSigmaBuilderOnly=false
RunCompleteSigmaAnalysis=false

# Define input and output names
InputFiles="AO2Ds_ReducedList"
OutputName="SigmaCandidatesTree"

if [ "$RunSigmaAnalysisOnly" = true ]; then
    echo "Running sigma0 Analysis!"
    if [ "$UseJSON" = true ]; then
        export OPTIONS="-b --configuration json://SigmaAnalysis-config.json --shm-segment-size 10000000000000 --pipeline sigma-analysis:3 --aod-file @${InputFiles}.txt"
    else 
        export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline sigma-analysis:3 --aod-file @${InputFiles}.txt"
        mv dpl-config.json SigmaAnalysis-config.json
    fi
     
    o2-analysis-lf-sigmaanalysis ${OPTIONS} | o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzeromlselection ${OPTIONS} | o2-analysis-lf-lambdakzeropid ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} | o2-analysis-lf-stradautracksconverter ${OPTIONS} | o2-analysis-lf-cascadespawner ${OPTIONS}
    
fi 
if [ "$RunSigmaBuilderOnly" = true ]; then
    echo "Creating dataset with sigma0 candidates"

    if [ "$UseJSON" = true ]; then
        export OPTIONS="-b --configuration json://SigmaBuilder-config.json --shm-segment-size 10000000000000 --pipeline sigma-builder:3 --aod-writer-keep AOD/V0SIGMAS/0 --aod-file @${InputFiles}.txt"
    else
        export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline sigma-builder:3 --aod-writer-keep AOD/V0SIGMAS/0 --aod-file @${InputFiles}.txt"
        mv dpl-config.json SigmaBuilder-config.json
    fi

    o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzeromlselection ${OPTIONS}

    echo "Moving outputs to: ~/ML_Strangeness/Dataset/Processed..."
    mv AnalysisResults_trees.root ~/ML_Strangeness/Dataset/Processed/${OutputName}.root
    mv AnalysisResults.root ~/ML_Strangeness/Dataset/Processed/${OutputName}Histograms.root
    echo "Removing AnalysisResults_trees.root and AnalysisResults.root"
    rm AnalysisResults_trees.root
    rm AnalysisResults.root
fi
if [ "$RunCompleteSigmaAnalysis" = true ]; then
    echo "Running sigma0 Analysis ans creating output Tree! Fasten seatbelts!"
    if [ "$UseJSON" = true ]; then
        export OPTIONS="-b --configuration json://SigmaCompleteAnalysis-config.json --shm-segment-size 10000000000000 --pipeline sigma-analysis:3 --aod-writer-keep AOD/V0SIGMAS/0 --aod-file @${InputFiles}.txt"
    else
        export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline sigma-analysis:3 --aod-writer-keep AOD/V0SIGMAS/0 --aod-file @${InputFiles}.txt"
        mv dpl-config.json SigmaCompleteAnalysis-config.json
    fi 
    o2-analysis-lf-sigmaanalysis ${OPTIONS} | o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzeromlselection ${OPTIONS}
fi
