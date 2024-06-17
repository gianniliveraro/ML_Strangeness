# MASTER SWITCHES
# Execute it in O2 env
StudyName="FindableExercise"
OutputName="AnalysisResultsMerged"
InputFiles="$HOME/ML_Strangeness/DEV/Gianni/Studies/${StudyName}/AnalysisResults_MLInputList3"

hadd ${OutputName}.root @${InputFiles}.txt

mv AnalysisResultsMerged.root ~/ML_Strangeness/DEV/Gianni/Studies/${StudyName}/AnalysisResultsMerged_MLInputList.root