//export OPTIONS="-b --configuration json://dpl-config.json --aod-memory-rate-limit 2000000000 --shm-segment-size 16000000000 --pipeline lambdakzero-mlselection:3 --aod-writer-keep AOD/V0MLOUTPUTS/0"
export OPTIONS="-b --aod-memory-rate-limit 2000000000 --shm-segment-size 16000000000 --aod-file AO2D_derived_0.root"
o2-analysis-lf-lambdakzeromlselection ${OPTIONS} 

