# MASTER SWITCHES
UseJSON=true

# Define input and output names
InputFiles="AO2Ds_ReducedList"
OutputName="MCSigma0GammasTree"


if [ "$UseJSON" = true ]; then
    export OPTIONS="-b --configuration json://TreeCreator-config.json --shm-segment-size 10000000000000 --pipeline lambdakzeromlselection-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0"
else 
    export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline lambdakzeromlselection-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0 --aod-file @${InputFiles}.txt" 
fi

o2-analysis-lf-lambdakzeromlselectiontreecreator ${OPTIONS} | o2-analysis-lf-lambdakzeropid ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} | o2-analysis-lf-cascadespawner ${OPTIONS} | o2-analysis-lf-stradautracksextraconverter ${OPTIONS} | o2-analysis-lf-stradautrackstofpidconverter ${OPTIONS} | o2-analysis-lf-v0coresconverter ${OPTIONS}

mv dpl-config.json TreeCreator-config.json
echo "Moving outputs to: ~/ML_Strangeness/Dataset/Interim..."
mv AnalysisResults_trees.root ~/ML_Strangeness/Dataset/Interim/${OutputName}.root
mv AnalysisResults.root ~/ML_Strangeness/Dataset/Interim/${OutputName}Histograms.root



