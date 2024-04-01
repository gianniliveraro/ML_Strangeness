// export OPTIONS="-b --configuration json://dpl-config.json --shm-segment-size 10000000000000 --pipeline lambdakzero-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0"
export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline lambdakzero-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0 --aod-file @inputlist_reduced.txt" 

o2-analysis-lf-lambdakzerotreecreator ${OPTIONS} 

echo "Moving outputs to: ~/ML_Strangeness/Dataset/Interim..."
mv AnalysisResults_trees.root ~/ML_Strangeness/Dataset/Interim/MCCandidatesTree.root
mv AnalysisResults.root ~/ML_Strangeness/Dataset/Interim/MCCandidatesHistograms.root
