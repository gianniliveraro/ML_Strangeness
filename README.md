# Strangeness analysis with Machine Learning

This repository aims to store codes for processing/analyses of derived data inside PWGLF. The folders/files are structured as follows:

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
│           └── sigmaanalysisv2.cxx        <- Analysis task of sigma0 candidates (work in progress!!)
│
├── src                                    <- Installation info and instructions
│   ├── install_mlenv.sh                   <- script to install ML environment with miniconda
│   └── ML_Env.yml                         <- python packages to be installed 
│
└── assets                                 <- media files (images, plots, etc)
~~~
