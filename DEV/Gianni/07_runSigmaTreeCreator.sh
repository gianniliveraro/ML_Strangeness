# MASTER SWITCHES
UseJSON=false
OutputName="SigmaAnalysisTree"
StudyName="TrainingGeneralMLModels"
# Define input and output names
InputFiles="Studies/${StudyName}/AO2Ds_MLInputListReduced"
JSONPATH="Studies/${StudyName}/SigmaTreeCreator-config"

if [ "$UseJSON" = true ]; then
    export OPTIONS="-b --configuration json://${JSONPATH}.json --shm-segment-size 10000000000000 --pipeline sigma0-builder:5  --aod-writer-keep AOD/V0SIGMAPHOTON/0"
else 
    export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline sigma0-builder:5 --aod-writer-keep AOD/V0SIGMAPHOTON/0 --aod-file @${InputFiles}.txt" 
fi

o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS}

mv dpl-config.json ${JSONPATH}.json
echo "Moving analysis results..."
mv AnalysisResults.root ${OutputName}.root

mv AnalysisResults_trees.root ~/ML_Strangeness/Dataset/Interim/${StudyName}/${OutputName}.root
mv AnalysisResults.root ~/ML_Strangeness/Dataset/Interim/${StudyName}/${OutputName}Histograms.root



