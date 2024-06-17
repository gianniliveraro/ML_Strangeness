# MASTER SWITCHES
UseJSON=true
OutputName="Studies/${StudyName}/SigmaAnalysisResults"
StudyName="TrainingGeneralMLModels"
# Define input and output names
InputFiles="Studies/${StudyName}/AO2Ds_MLInputList"
JSONPATH="Studies/${StudyName}/SigmaAnalysis-config"

if [ "$UseJSON" = true ]; then
    export OPTIONS="-b --configuration json://${JSONPATH}.json --shm-segment-size 10000000000000 --pipeline sigma-analysis:5"
else 
    export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline sigma-analysis:5 --aod-file @${InputFiles}.txt" 
fi

o2-analysis-lf-sigmaanalysis ${OPTIONS} | o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS}

mv dpl-config.json ${JSONPATH}.json
echo "Moving analysis results..."
mv AnalysisResults.root ${OutputName}.root



