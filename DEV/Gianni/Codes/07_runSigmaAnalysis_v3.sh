#!/bin/bash

# Define input and output names
InputFiles="AO2D_inputlist"
OutputName="SigmaCandidatesTree"
fIsSecondRun=false

# Function to set options
set_options() {
    local config_file="$1"
    if [ "$fIsSecondRun" = true ]; then
        export OPTIONS="-b --configuration json://$config_file --shm-segment-size 10000000000000 --aod-file @${InputFiles}.txt"
    else
        export OPTIONS="-b --shm-segment-size 10000000000000 --aod-file @${InputFiles}.txt"
        mv dpl-config.json "$config_file"
    fi
}

# Function to perform analysis
perform_analysis() {
    local config_file="$1"
    set_options "$config_file"
    o2-analysis-lf-sigmaanalysis ${OPTIONS} | o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzeromlselection ${OPTIONS}
}

# Function to handle output files
handle_output() {
    echo "Moving outputs to: ~/ML_Strangeness/Dataset/Processed..."
    mv AnalysisResults_trees.root ~/ML_Strangeness/Dataset/Processed/${OutputName}.root
    mv AnalysisResults.root ~/ML_Strangeness/Dataset/Processed/${OutputName}Histograms.root
    echo "Removing AnalysisResults_trees.root and AnalysisResults.root"
    rm AnalysisResults_trees.root AnalysisResults.root
}

# Perform analysis based on flags
if [ "$RunSigmaAnalysisOnly" = true ]; then
    echo "Running sigma0 Analysis!"
    perform_analysis "SigmaAnalysis-config.json"
elif [ "$RunSigmaBuilderOnly" = true ]; then
    echo "Creating dataset with sigma0 candidates"
    perform_analysis "SigmaBuilder-config.json"
    handle_output
elif [ "$RunCompleteSigmaAnalysis" = true ]; then
    echo "Running complete sigma0 Analysis!"
    perform_analysis "SigmaCompleteAnalysis-config.json"
fi

echo "Script execution complete."
