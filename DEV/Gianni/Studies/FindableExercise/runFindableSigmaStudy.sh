# MASTER SWITCHES
UseJSON=true
StudyName="FindableExercise"
OutputName="FindablesSigma0"

# Define input and output names
InputFiles="AO2Ds_MLInputListReduced"
JSONPATH="FindablesSigma0-config"

if [ "$UseJSON" = true ]; then
    export OPTIONS="-b --configuration json://${JSONPATH}.json --shm-segment-size 10000000000000 --pipeline findable-sigma-study:3"
else 
    export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline findable-sigma-study:3 --aod-file @${InputFiles}.txt" 
fi

o2-analysis-lf-findable-sigmastudy ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} | o2-analysis-lf-lambdakzeropid ${OPTIONS}

mv dpl-config.json ${JSONPATH}.json
echo "Moving analysis results..."
mv AnalysisResults.root ${OutputName}.root



