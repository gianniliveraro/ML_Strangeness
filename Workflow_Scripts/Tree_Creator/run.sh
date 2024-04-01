export OPTIONS="-b --configuration json://dpl-config.json --shm-segment-size 10000000000000 --pipeline lambdakzero-treecreator:3 --aod-writer-keep AOD/V0MLCANDIDATES/0"

o2-analysis-lf-lambdakzerotreecreator ${OPTIONS} //--aod-file @inputsigma_reduced.txt

