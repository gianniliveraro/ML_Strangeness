# MASTER SWITCHES
UseJSON=true
StudyName="FindableExercise"
OutputName="FindableLambdas"

# Define input and output names
InputFiles="AO2Ds_MLInputListReduced3"
JSONPATH="FindablesLambdas-config"

if [ "$UseJSON" = true ]; then
    export OPTIONS="-b --configuration json://${JSONPATH}.json --shm-segment-size 10000000000000 --pipeline findable-study:3"
else 
    export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline findable-study:3 --aod-file @${InputFiles}.txt" 
fi

o2-analysis-lf-findable-study ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} | o2-analysis-lf-lambdakzeropid ${OPTIONS} 

mv dpl-config.json ${JSONPATH}.json
echo "Moving analysis results..."
mv AnalysisResults.root ${OutputName}.root



