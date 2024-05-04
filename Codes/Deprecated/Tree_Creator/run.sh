// export OPTIONS="-b --configuration json://dpl-config.json"
export OPTIONS="-b --configuration json://dpl-config.json --shm-segment-size 10000000000000 --pipeline lambdakzeromlselection-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0"
// export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline lambdakzeromlselection-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0 --aod-file @inputlist_reduced.txt" 

o2-analysis-lf-lambdakzeromlselectiontreecreator ${OPTIONS} 

echo "Moving outputs to: ~/ML_Strangeness/Dataset/Interim..."
mv AnalysisResults_trees.root ~/ML_Strangeness/Dataset/Interim/MCCandidatesTree_QAOnly.root
mv AnalysisResults.root ~/ML_Strangeness/Dataset/Interim/MCCandidatesHistograms_QAOnly.root
