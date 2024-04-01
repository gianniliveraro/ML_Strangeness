export OPTIONS="-b --configuration json://dpl-config.json --shm-segment-size 10000000000000 --pipeline sigma0-builder:3 --aod-writer-keep AOD/V0MLSIGMAS/0"
// export OPTIONS="-b --shm-segment-size 10000000000000 --pipeline sigma0-builder:3"

o2-analysis-lf-sigma0builder ${OPTIONS} | o2-analysis-lf-lambdakzeromlselection ${OPTIONS} //--aod-file AO2D_derived_0.root

