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

3. Log out from your account and log in again. 

4. Activate the ML_Env environment with:
```c
     conda activate ML_Env
``` 

## Structure/organization:

~~~
├── Dataset
│   ├── Processed                          <- processed data for analysis
│   ├── Interim                            <- intermediate datasets
│   └── Raw                                <- raw AO2D/AR files
│
├── Codes                                  <- Basic scripts to perform complete analysis
|
├── src                                    <- Installation info and instructions
│   ├── install_mlenv.sh                   <- script to install ML environment with miniconda
│   └── ML_Env.yml                         <- python packages to be installed 
│
├── DEV                                    <- directory to include your dev codes! 
│
└── assets                                 <- media files (images, plots, etc)
~~~


## Execution workflow (Outdated!!):

This is the Workflow to execute the codes in order to reproduce results: 

<p align="center">
    <img src="../main/assets/StrangenessMLWorkflow.pptx.png" height="450">
</p>

