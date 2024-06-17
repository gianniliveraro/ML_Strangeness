# Copyright 2019-2020 CERN and copyright holders of ALICE O2.
# See https:#alice-o2.web.cern.ch/copyright for details of the copyright holders.
# All rights not expressly granted are reserved.
#
# This software is distributed under the terms of the GNU General Public
# License v3 (GPL Version 3), copied verbatim in the file "COPYING".
#
# In applying this license CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.
#
# 00_CreateNewStudy
# ================
#
# This code creates a new study
#
#    Comments, questions, complaints, suggestions?
#    Please write to:
#    gianni.shigeru.setoue.liveraro@cern.ch

#____________________________
# Imports
import os
    
#____________________________
# Folder structure
StudyName = "TrainingGeneralMLModels"
StudyDescription = "Diretório para estudar algoritmos de ML treinados para selecionar gammas/lambdas em análises gerais."
DatasetsNames = "LF_LHC24d2b_pass3_Strangeness"

# Diretórios principais
MAIN_PATH = '/storage1/liveraro/ML_Strangeness/DEV/Gianni/'
STUDY_PATH = MAIN_PATH+'Studies/{}/'.format(StudyName) # nome do projeto
os.makedirs(STUDY_PATH, exist_ok=True) # criando pasta de trabalho
os.makedirs(STUDY_PATH+"Results/", exist_ok=True)

# Create readme
file = open(STUDY_PATH+"/README.txt", "w")
file.write('Description: ' + StudyDescription + '\n \n')
file.write('------------------------------------------------------- \n \n')
file.write('Datasets: {} \n \n'.format(DatasetsNames))
file.close()

# Updating studies list:
with open(MAIN_PATH+"Studies/StudiesList.txt", "a+") as file_object:
    file_object.seek(0)
    # If file is not empty then append '\n'
    data = file_object.read(100)
    if len(data) > 0 :
        file_object.write("\n")
    # Append text at the end of file
    file_object.write("{}: {}".format(StudyName, StudyDescription))