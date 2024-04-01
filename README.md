# Strangeness analysis with Machine Learning

This repository aims to store codes for processing/analyses of derived data inside PWGLF. 

## Installation and usage:
0. An updated version of O2 software is required
   
1. Clone this repository in a local machine:
```c
git clone https://github.com/gianniliveraro/ML_Strangeness.git
``` 
2. Navigate to the top level of the repository and run:
```c   
./src/install_mlenv.sh
``` 
this creates an environment (called "ML_Env") with miniconda to run python codes for ML analysis. 

3. Activate the ML_Env environment with:
```c
     conda activate ML_Env
``` 

## Structure/organization:

~~~
├── Dataset
│   ├── Processed                          <- processed data for analysis
│   ├── Interim                            <- intermediate datasets
│   └── Raw                                <- raw AO2D files
│
├── Workflow_Scripts      
│   ├── Tree_Creator                       <- scripts to execute lambdakzeroTreeCreator.cxx
│   ├── ML_Analysis                        <- scripts to process root files, train, test and analyze ML models.
│   └── Sigma0_Analysis                    <- 
|
├── PWGLF                                  <- same structure of PWGLF directory inside O2Physics.  
│   ├── DataModel
│       └── LFStrangenessMLTables.h        <- declares the main tables for ML analysis
│   ├── TableProducer
│       ├── lambdakzeromlselection.cxx     <- Load trained BDT models and creates the V0MLOutput Table
│       ├── lambdakzeroTreeCreator.cxx     <- Creates a simple TTree with MC data to train/test ML models
│       └── sigma0builder.cxx              <- Combine Gammas and Lambdas, based on ML selection, to create sigma0 candidates for analysis.
│   └── Tasks
│       └── Strangeness
│           └── sigmaanalysis.cxx        <- Analysis task of sigma0 candidates (work in progress!!)
│
├── src                                    <- Installation info and instructions
│   ├── install_mlenv.sh                   <- script to install ML environment with miniconda
│   └── ML_Env.yml                         <- python packages to be installed 
│
└── assets                                 <- media files (images, plots, etc)
~~~


## Execution workflow:

This is the Workflow to execute the codes in order to reproduce results: 

<p align="center">
    <img src="../main/assets/StrangenessMLWorkflow.pptx.png" height="450">
</p>

