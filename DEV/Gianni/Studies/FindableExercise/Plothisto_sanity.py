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
import uproot
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator) 
import numpy as np

#____________________________
# Configurations
Species = "Lambdas"
Mother = "Sigma0"

#____________________________
# Opening files
fileFindSpeciesAll = uproot.open("Dummy_Findable.root")
fileGen = uproot.open("Dummy_Generated.root") # generated

#____________________________
# Getting relevant histograms 
hFindSpeciesAll = fileFindSpeciesAll["h2dPtVsCentrality_All_Findable"]
#hFoundSpeciesAll = fileFindSpeciesAll["findable-study/h2dPtVsCentrality_All_Found"]
hGenSpecies = fileGen["h2dGenLambda"]

def ProcessHistos(histo):
    ## Centrality
    print('DIM', histo.values().ndim)
    if histo.values().ndim == 1:
        # For 1D histogram, set HistoEdges_Centrality to contain only one bin
        HistoEdges_Centrality = np.array([0, 90])  # Adjust the range as needed
        #____________________________
        # Extract bin edges, values, and errors
        HistoEdges_PT = histo.axis(axis=0).edges()

        Histo_values = histo.values().reshape(1, -1)
        Histo_errors = histo.errors().reshape(1, -1)
    else:
        HistoEdges_Centrality = histo.axis(axis=0).edges()
        #____________________________
        # Extract bin edges, values, and errors
        HistoEdges_PT = histo.axis(axis=1).edges()
        Histo_values = histo.values()
        Histo_errors = histo.errors()

    # Calculate bin sizes based on FoundEdges_PT
    bin_sizes = np.diff(HistoEdges_PT)/2
    Point_positions = HistoEdges_PT[:-1] + bin_sizes

    return HistoEdges_Centrality, Histo_values, Histo_errors, Point_positions, bin_sizes 

def Rebin(NewBins, OldBins, Histobinsvalues, axis=None):
    if not isinstance(NewBins, np.ndarray) or not isinstance(OldBins, np.ndarray):
        raise ValueError("NewBins and OldBins must be numpy arrays")

    if axis is None and Histobinsvalues.ndim > 1:
        raise ValueError("Please specify the axis to rebin for multidimensional histograms")

    return rebin_nd(NewBins, OldBins, Histobinsvalues, axis if axis is not None else 0)

def rebin_nd(NewBins, OldBins, Histobinsvalues, axis):
    # Determine the dimensionality
    ndim = Histobinsvalues.ndim
    axis = axis % ndim  # Ensure the axis is within the correct range

    # Initialize empty arrays for the new bins
    new_shape = list(Histobinsvalues.shape)
    new_shape[axis] = len(NewBins) - 1
    New_Bin = np.zeros(new_shape)
    New_Error = np.zeros(new_shape)

    for i in range(len(NewBins) - 1):
        print("np.where(OldBins == NewBins[i])", np.where(OldBins == NewBins[i])[0][0])
        inf_lim = np.where(OldBins == NewBins[i])[0][0]
        sup_lim = np.where(OldBins == NewBins[i + 1])[0][0]

        if inf_lim == -1 or sup_lim == -1:
            raise ValueError('Bin didn\'t match! Please, modify the rebin array!')

        slices = [slice(None)] * ndim
        slices[axis] = slice(inf_lim, sup_lim)
        summed_array = np.sum(Histobinsvalues[tuple(slices)], axis=axis)
        summedError_array = np.sqrt(summed_array)

        slices[axis] = i
        New_Bin[tuple(slices)] = summed_array
        New_Error[tuple(slices)] = summedError_array

    return New_Bin, New_Error

#---------------------------------------------------

def calcEff(cent_bins, hNumerator, hDenominator):
    hDenoEdges_Centrality, Denominator, Denominator_errors, DenPoint_positions, Denbin_sizes = ProcessHistos(hDenominator)
    hNumEdges_Centrality, Numerator, Numerator_errors, NumPoint_positions, Numbin_sizes = ProcessHistos(hNumerator)

    ## Rebinning
    CustomBins = np.array([0, 90])
    UseCustom = True
    if UseCustom:
        print("------------------------------------------")
        print("Rebinning process activated!")
        Point_positions, bin_sizes = NumPoint_positions, Numbin_sizes
        HistoEdges_Centrality = CustomBins
        Denominator, Denominator_errors = Rebin(CustomBins, np.array(hDenoEdges_Centrality), Denominator, axis=0)
        Numerator, Numerator_errors = Rebin(CustomBins, np.array(hNumEdges_Centrality), Numerator, axis=0)
        
    elif len(hDenoEdges_Centrality)!=len(hNumEdges_Centrality):
        
        if (len(hNumEdges_Centrality)<len(hDenoEdges_Centrality)):
            #print('Histos will be rebinned from: ', hDenoEdges_Centrality)
            #print('to: ', hNumEdges_Centrality)
            Point_positions, bin_sizes = NumPoint_positions, Numbin_sizes
            HistoEdges_Centrality = hNumEdges_Centrality
            Denominator, Denominator_errors = Rebin(hNumEdges_Centrality, hDenoEdges_Centrality, Denominator)
        else:
            #print('Histos will be rebinned from: ', hNumEdges_Centrality)
            #print('to: ', hDenoEdges_Centrality)
            Point_positions, bin_sizes = DenPoint_positions, Denbin_sizes
            HistoEdges_Centrality = hDenoEdges_Centrality
            Numerator, Numerator_errors = Rebin(hDenoEdges_Centrality, hNumEdges_Centrality, Numerator)
    
    else:
        Point_positions, bin_sizes = NumPoint_positions, Numbin_sizes
        HistoEdges_Centrality = hNumEdges_Centrality

    Eff_List = []
    EffError_List = []
    CentralityLabel = []

    for cent_bin in cent_bins:
        # Calculate Efficiency and error propagation
        Efficiency = Numerator[cent_bin]/Denominator[cent_bin]
        Efficiency_error = Efficiency * np.sqrt((Numerator_errors[cent_bin] /   Numerator[cent_bin])**2 + (Denominator_errors[cent_bin] / Denominator[cent_bin])**2)

        Eff_List.append(Efficiency)
        EffError_List.append(Efficiency_error)
        CentralityLabel.append('{}-{}%'.format(HistoEdges_Centrality[cent_bin], HistoEdges_Centrality[cent_bin+1]))

    return Point_positions, Eff_List, EffError_List, CentralityLabel, bin_sizes

def plotEff(cent_bins_list, histograms_list, labels_list, plot_name, ylabel):
    # Plot the histogram
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    # print("histograms_list", histograms_list)
    for i in range(len(histograms_list)):
        cent_bins = cent_bins_list[i]
        histograms = histograms_list[i]
        # print("histograms_list[i]", histograms_list[i])
        # print("histograms[0]", histograms[0][0])
        Point_positions, Eff_List, EffError_List, CentralityLabel, bin_sizes = calcEff(cent_bins, histograms[0][0], histograms[0][1])
        for j in range(len(Eff_List)):    
            #ax.errorbar(Point_positions, Eff_List[j], yerr=EffError_List[j], xerr=bin_sizes, fmt='o', label=r'{}'.format(labels_list[i][0])+', {}'.format(CentralityLabel[j]), markersize=4)    
            ax.errorbar(Point_positions, Eff_List[j], yerr=EffError_List[j], xerr=bin_sizes, fmt='o', label=r'{}'.format(labels_list[i][0]), markersize=4)    

    #------------------------------------------------
    # Plot configs: 
    #plt.figtext(0.275, 0.670, r"$\bf{ALICE}$  $\bf{MC}$" + '\n Pb-Pb at $\sqrt{s}=5.36$ TeV \n $|\mathrm{y}|<0.5$', ha='center') # ALICE
    plt.figtext(0.275, 0.670, r"$\bf{ALICE}$  $\bf{MC}$" + '\n 0-90% Pb-Pb, $\sqrt{s}=5.36$ TeV \n $|\mathrm{y}|<0.5$', ha='center') # ALICE

    ax.set_xlim((0,10.001))
    ax.set_ylim((0,1.01))

    ax.set_ylabel(r'{}'.format(ylabel), fontsize=15, loc='top')
    ax.set_xlabel(r'$p_{T}$ (GeV/c)', fontsize=15, loc='right')

    # Ticks configuration
    ax.yaxis.set_ticks_position('both')                                                                                                                                                                                                                                  
    ax.xaxis.set_ticks_position('both')
    ax.set_xticks(np.arange(0, 10.001, 1.0))
    ax.set_yticks(np.arange(0, 1.01, 0.1))
    ax.xaxis.set_major_locator(MultipleLocator(1.0))                                                                                                                                                                                             
    ax.xaxis.set_minor_locator(AutoMinorLocator())                                                                                                                                                                                
    ax.yaxis.set_major_locator(MultipleLocator(0.1))                                                                                                                                                                          
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.xaxis.set_tick_params(direction='in', which='both', length=6)
    ax.yaxis.set_tick_params(direction='in', which='both', length=6)
    ax.xaxis.set_tick_params(which='major', length=9)
    ax.yaxis.set_tick_params(which='major', length=9)

    plt.grid(linestyle="--")
    ax.legend(loc='upper right') # Legend
    plt.savefig('Results/{}_Sanity.png'.format(plot_name), bbox_inches='tight')    


#######

# # Found/Findable
# cent_bins = [0, 4, 7] # centrality bin indices: 
# plotEff(cent_bins, hFoundSpeciesAll, hFindSpeciesAll, 
#         "Accept_x_Findable", "Acceptably tracked / Findable")

# # # Efficiency (all particles)
# cent_bins = [0, 4, 7] # centrality bin indices
# plotEff(cent_bins, hFindSpeciesAll, hGenSpecies, 
#         "Efficiency_{}".format(Species), "Efficiency x Acceptance")

# # # Efficiency (sigma0 only)
# cent_bins = [0] # centrality bin indices
# plotEff(cent_bins, hFindMotherSpecies, hGenMotherSpecies, 
#         "Efficiency_{}{}".format(Mother, Species), "Efficiency x Acceptance")

##################### V5 plots

cent_bins_list = [[0]]  # List of lists of centrality bin indices

labels_list = [["Sanity test"]] # prefix


histograms_list = [[[hFindSpeciesAll, hGenSpecies]]]  # List of lists of histograms

# histograms_list = [[[hFindSpeciesAll, hGenSpecies]],
#                   [[hFoundSpeciesAll, hGenSpecies]], 
#                   [[hFindMotherSpecies, hGenMotherSpecies]], 
#                   [[hFoundMotherSpecies, hGenMotherSpecies]]]  # List of lists of histograms

plotEff(cent_bins_list, histograms_list, labels_list, "Efficiency_{}".format(Species), "Efficiency x Acceptance")

