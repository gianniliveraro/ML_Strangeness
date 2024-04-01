// export OPTIONS="-b --configuration json://dpl-config.json --shm-segment-size 10000000000000 --pipeline sigma0-builder:3 --aod-writer-keep AOD/V0MLSIGMAS/0"
export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline sigma0-builder:3 --aod-writer-keep AOD/V0MLSIGMAS/0 --aod-file ~/ML_Strangeness/Dataset/AO2D_derived_0.root"

o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzeromlselection ${OPTIONS} //--aod-file AO2D_derived_0.root

o2-aod-merger --input ao2dstomerge.txt --output SigmaCandidatesTree.root

echo "Moving to: ~/ML_Strangeness/Dataset/Interim/SigmaCandidatesTree.root..."
mv SigmaCandidatesTree.root ~/ML_Strangeness/Dataset/Interim/SigmaCandidatesTree.root