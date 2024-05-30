# MASTER SWITCHES
UseJSON=true
Specie="Lambdas"
StudyName="FindableExercise"
OutputName="FindableSigma0${Specie}"
MAINPATH="$HOME/ML_Strangeness/DEV/Gianni/Studies/"

# Define input and output names
InputFiles="${StudyName}/AO2Ds_MLInputList"
JSONPATH="${StudyName}/Findables${Specie}-config"

if [ "$UseJSON" = true ]; then
    export OPTIONS="-b --configuration json://${MAINPATH}${JSONPATH}.json --shm-segment-size 10000000000000 --pipeline findable-study:10"
else 
    export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline findable-study:10 --aod-file @${MAINPATH}/${InputFiles}.txt" 
fi

o2-analysis-lf-findable-study ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS}

mv dpl-config.json ${MAINPATH}${JSONPATH}.json
echo "Moving analysis results..."
mv AnalysisResults.root ${MAINPATH}/${StudyName}/${OutputName}.root



