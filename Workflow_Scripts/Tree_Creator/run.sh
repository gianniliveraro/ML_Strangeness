// export OPTIONS="-b --configuration json://dpl-config.json --shm-segment-size 10000000000000 --pipeline lambdakzero-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0"
export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline lambdakzero-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0 --aod-file @inputsigma_reduced.txt"

o2-analysis-lf-lambdakzerotreecreator ${OPTIONS} 

echo "Moving to: ~/ML_Strangeness/Dataset/Interim/MCCandidatesTree.root..."
mv AnalysisResults_trees.root ~/ML_Strangeness/Dataset/Interim/MCCandidatesTree.root
