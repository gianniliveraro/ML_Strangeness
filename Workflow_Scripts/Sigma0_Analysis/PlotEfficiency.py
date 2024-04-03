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
# ================
#
# Code to plot efficiencies
#
#    Comments, questions, complaints, suggestions?
#    Please write to:
#    gianni.shigeru.setoue.liveraro@cern.ch
#    romain.schotter@cern.ch
#    david.dobrigkeit.chinellato@cern.ch

#____________________________
# Imports
import uproot
import numpy as np
import matplotlib.pyplot as plt


#---------------------------  MAIN CONFIGURATIONS -----------------------------

##--------------------------------- PATHS ------------------------------------
MAIN_PATH = '/storage1/liveraro/ML_Strangeness/'
DATA_PATH = MAIN_PATH+'Dataset/Processed/'


def PlotEfficiency(hReco, hGen, rebin_factor = 10):

    # Rebin histograms
    hReco = hReco.rebin(rebin_factor)
    hGen = hGen.rebin(rebin_factor)
    # Calculate efficiency
    efficiency = hReco.values / hGen.values
    bin_centers = hReco.edges[:-1] + np.diff(hReco.edges) / 2

    return efficiency, bin_centers

file = uproot.open(DATA_PATH+'SigmaCandidatesHistograms.root')
hRecoLambda = file["sigma0builder/ptHistogramLambda"].to_hist()
hGenLambda = file["sigma0builder/ptGeneratedLambda"].to_hist()

# Create canvas
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlabel(r'$p_{T}$ (GeV/c)')
ax.set_ylabel('Acceptance x efficiency')
ax.set_title('Efficiency')

efficiency_lambda, bincenters_lambda = PlotEfficiency(hRecoLambda, hGenLambda, rebin_factor = 10)

# Plot histograms
ax.errorbar(bincenters_lambda, efficiency_lambda, yerr=np.sqrt(hRecoLambda.variances) / hGenLambda.values, label=r'$\pi$', fmt='o', color='g')

# Add legend
ax.legend()

# Save figure
plt.savefig("Lambda_Efficiency.pdf")
plt.show()
