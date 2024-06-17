# MASTER SWITCHES
UseJSON=true
StudyName="FindableExercise"
OutputName="FindableTreeGammasReduced"

# Define input and output names
InputFiles="AO2Ds_MLInputListReduced2"
JSONPATH="FindablesTreeGammas-config"

if [ "$UseJSON" = true ]; then
    export OPTIONS="-b --configuration json://${JSONPATH}.json --shm-segment-size 10000000000000 --pipeline findable-treecreator:6 --aod-writer-keep AOD/V0FINDCAND/0"
else 
    export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline findable-treecreator:6 --aod-writer-keep AOD/V0FINDCAND/0 --aod-file @${InputFiles}.txt" 
fi

o2-analysis-lf-findable-treecreator ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} | o2-analysis-lf-lambdakzeropid ${OPTIONS} | o2-analysis-lf-strarawcentsconverter ${OPTIONS} 

mv dpl-config.json ${JSONPATH}.json
echo "Moving analysis results..."
mv AnalysisResults.root ${OutputName}.root

mv AnalysisResults_trees.root AnalysisResults_${OutputName}.root



