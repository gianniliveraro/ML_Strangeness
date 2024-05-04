export OPTIONS="-b --configuration json://dpl-config.json --shm-segment-size 10000000000000 --pipeline sigma0-builder:3 --aod-writer-keep AOD/V0SIGMAS/0"
// export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline sigma0-builder:3 --aod-writer-keep AOD/V0SIGMAS/0 --aod-file @AO2D_inputlist.txt"

o2-analysis-lf-sigmaanalysis ${OPTIONS} | o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzeromlselection ${OPTIONS} 

echo "Moving outputs to: ~/ML_Strangeness/Dataset/Processed..."
mv AnalysisResults_trees.root ~/ML_Strangeness/Dataset/Processed/SigmaCandidatesTree.root
mv AnalysisResults.root ~/ML_Strangeness/Dataset/Processed/SigmaCandidatesHistograms.root
echo "Removing AnalysisResults_trees.root and AnalysisResults.root"
rm AnalysisResults_trees.root
rm AnalysisResults.root