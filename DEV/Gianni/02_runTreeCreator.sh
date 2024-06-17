# MASTER SWITCHES
UseJSON=true
Useconverters=false
StudyName="TrainingGeneralMLModels"
OutputName="MCNewLambdasOnlyTree"
InputFiles="Studies/${StudyName}/AO2Ds_MLInputList"
JSONPATH="Studies/${StudyName}/TreeCreator-config"

if [ "$UseJSON" = true ]; then
    export OPTIONS="-b --configuration json://${JSONPATH}.json --shm-segment-size 10000000000000 --pipeline lambdakzeromlselection-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0"
else 
    export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline lambdakzeromlselection-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0 --aod-file @${InputFiles}.txt" 
fi

if [ "$Useconverters" = true ]; then
    o2-analysis-lf-lambdakzeromlselectiontreecreator ${OPTIONS} | o2-analysis-lf-lambdakzeropid ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} | o2-analysis-lf-cascadespawner ${OPTIONS} | o2-analysis-lf-stradautracksextraconverter ${OPTIONS} | o2-analysis-lf-stradautrackstofpidconverter ${OPTIONS} | o2-analysis-lf-v0coresconverter ${OPTIONS}
else
    o2-analysis-lf-lambdakzeromlselectiontreecreator ${OPTIONS} | o2-analysis-lf-lambdakzeropid ${OPTIONS} | o2-analysis-lf-lambdakzerospawner ${OPTIONS} 
fi

mv dpl-config.json ${JSONPATH}.json
echo "Moving outputs to: ~/ML_Strangeness/Dataset/Interim..."
mv AnalysisResults_trees.root ~/ML_Strangeness/Dataset/Interim/${StudyName}/${OutputName}.root
mv AnalysisResults.root ~/ML_Strangeness/Dataset/Interim/${StudyName}/${OutputName}Histograms.root



