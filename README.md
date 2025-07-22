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
│   ├── Processed                          <- processed data for ML analysis
│   └── Raw                                <- raw AO2D/DATA files
│
├── Codes                                  <- Basic scripts to perform ML analysis
|
├── src                                    <- Installation info and instructions
│   ├── install_mlenv.sh                   <- script to install ML environment with miniconda
│   └── ML_Env.yml                         <- python packages to be installed 
│
├── Results                                <- directory that saves your ML runs + results
│
└── assets                                 <- media files (images, plots, etc)
~~~

