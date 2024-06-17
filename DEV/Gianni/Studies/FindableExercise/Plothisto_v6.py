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
Species = "Gammas"
Species2 = "Gamma"
Mother = "Sigma0"

#____________________________
# Opening files
#fileFindMotherSpecies = uproot.open("Findable{}{}.root".format(Mother, Species))
fileFindSpeciesAll = uproot.open("Findable{}.root".format(Species))
fileGen = uproot.open("AnalysisResultsMerged_MLInputList.root") # generated

#____________________________
# Getting relevant histograms 
#hFindMotherSpecies = fileFindMotherSpecies["findable-study/h2dPtVsCentrality_All_Findable"]
#hFoundMotherSpecies = fileFindMotherSpecies["findable-study/h2dPtVsCentrality_All_Found"]
#hGenMotherSpecies = fileGen["strangederivedbuilder/hGenSigma0"]
hFindSpeciesAll = fileFindSpeciesAll["findable-study/h2dPtVsCentrality_Findable"]
hFoundSpeciesAll = fileFindSpeciesAll["findable-study/h2dPtVsCentrality_Found"]
hAccTrackSpeciesAll = fileFindSpeciesAll["findable-study/h2dPtVsCentrality_AcceptablyTracked"]
hGenSpecies = fileGen["strangederivedbuilder/h2dGen{}".format(Species2)]


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

def Rebin(NewBins, OldBins, Histobinsvalues):

    for i in range(0, len(NewBins)-1):
        inf_lim, sup_lim = -1, -1
        inf_lim = np.where(OldBins==NewBins[i])[0][0]
        sup_lim = np.where(OldBins==NewBins[i+1])[0][0]

        if (inf_lim==-1) or (sup_lim==-1):
            print('Bin didnt match! Please, modify the rebin array!')
            print("Available bins edges: \n")
            print(OldBins)
            break

        if i==0:
            New_Bin = np.sum(Histobinsvalues[inf_lim:sup_lim, :], axis=0) #Centrality x pT
            New_Error = np.sqrt(New_Bin)
        else:
            summed_array = np.sum(Histobinsvalues[inf_lim:sup_lim, :], axis=0) #Centrality x pT
            summedError_array = np.sqrt(summed_array)
            New_Bin = np.concatenate((New_Bin, summed_array), axis=0)
            New_Error = np.concatenate((New_Error, summedError_array), axis=0)

    N = len(NewBins)-1
    M = len(Histobinsvalues[0])  # Assuming all arrays have the same length

    New_Bin = New_Bin.reshape(N, M)
    New_Error = New_Error.reshape(N, M)

    # print("Old bins values:", Histobinsvalues)
    # print("New bins:", New_Bin)

    return New_Bin, New_Error 

#---------------------------------------------------

def calcEff(cent_bins, hNumerator, hDenominator):
    hDenoEdges_Centrality, Denominator, Denominator_errors, DenPoint_positions, Denbin_sizes = ProcessHistos(hDenominator)
    hNumEdges_Centrality, Numerator, Numerator_errors, NumPoint_positions, Numbin_sizes = ProcessHistos(hNumerator)

    ## Rebinning
    CustomBins = [0, 90]
    UseCustom = False
    if UseCustom:
        print("------------------------------------------")
        print("Rebinning process activated!")
        Point_positions, bin_sizes = NumPoint_positions, Numbin_sizes
        HistoEdges_Centrality = CustomBins
        Denominator, Denominator_errors = Rebin(CustomBins, hDenoEdges_Centrality, Denominator)
        Numerator, Numerator_errors = Rebin(CustomBins, hNumEdges_Centrality, Numerator)
        
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
        # if Efficiency>0.64:
        #     print("")
        # print("Numerator[{}]".format(cent_bin), Numerator[cent_bin])
        # print("Denominator[{}]".format(cent_bin), Denominator[cent_bin])
        # print("Efficiency[{}]".format(cent_bin), Efficiency)
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
        print("Processing {}".format(labels_list[i]))
        cent_bins = cent_bins_list[i]
        histograms = histograms_list[i]
        # print("histograms_list[i]", histograms_list[i])
        # print("histograms[0]", histograms[0][0])
        Point_positions, Eff_List, EffError_List, CentralityLabel, bin_sizes = calcEff(cent_bins, histograms[0][0], histograms[0][1])
        print("Point_positions: {}, Eff: {}".format(Point_positions, Eff_List))
        for j in range(len(Eff_List)):    
            
            #ax.errorbar(Point_positions, Eff_List[j], yerr=EffError_List[j], xerr=bin_sizes, fmt='o', label=r'{}'.format(labels_list[i][0])+', {}'.format(CentralityLabel[j]), markersize=4)    
            ax.errorbar(Point_positions, Eff_List[j], yerr=EffError_List[j], xerr=bin_sizes, fmt='o', label=r'{}'.format(labels_list[i][0])+'{}'.format(CentralityLabel[j]), markersize=4)    
            #ax.errorbar(Point_positions, Eff_List[j], yerr=EffError_List[j], xerr=bin_sizes, fmt='o', label=r'{}'.format(labels_list[i][0]), markersize=4)    

    #------------------------------------------------
    # Plot configs: 
    #plt.figtext(0.275, 0.670, r"$\bf{ALICE}$  $\bf{MC}$" + '\n Pb-Pb at $\sqrt{s}=5.36$ TeV \n $|\mathrm{y}|<0.5$', ha='center') # ALICE
    #plt.figtext(0.275, 0.670, r"$\bf{ALICE}$  $\bf{MC}$" + '\n 0-90% Pb-Pb, $\sqrt{s}=5.36$ TeV \n $|\mathrm{y}|<0.5$', ha='center') # ALICE
    #plt.figtext(0.275, 0.670, r"$\bf{ALICE}$  $\bf{MC}$" + '\n Pb-Pb, $\sqrt{s}=5.36$ TeV \n Primary $\Lambda^0$, $|\mathrm{y}|<0.5$', ha='center') # ALICE
    plt.figtext(0.275, 0.670, r"$\bf{ALICE}$  $\bf{MC}$" + '\n Pb-Pb, $\sqrt{s}=5.36$ TeV \n Photons, $|\mathrm{y}|<0.5$', ha='center') # ALICE

    # ax.set_xlim((0,10.001))
    # ax.set_ylim((0,0.2))
    ax.set_xlim((0,10.001))
    ax.set_ylim((0,1.0))

    ax.set_ylabel(r'{}'.format(ylabel), fontsize=15, loc='top')
    ax.set_xlabel(r'$p_{T}$ (GeV/c)', fontsize=15, loc='right')

    # Ticks configuration
    ax.yaxis.set_ticks_position('both')                                                                                                                                                                                                                                  
    ax.xaxis.set_ticks_position('both')
    # ax.set_xticks(np.arange(0, 10.001, 1.0))
    # ax.set_yticks(np.arange(0, 0.2, 0.02))
    ax.set_xticks(np.arange(0, 10.001, 1.0))
    ax.set_yticks(np.arange(0, 1.0, 0.1))
    ax.xaxis.set_major_locator(MultipleLocator(1.0))                                                                                                                                                                                             
    ax.xaxis.set_minor_locator(AutoMinorLocator())                                                                                                                                                                                
    #ax.yaxis.set_major_locator(MultipleLocator(0.02))                                                                                                                                                                          
    ax.yaxis.set_major_locator(MultipleLocator(0.1))                                                                                                                                                                          
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.xaxis.set_tick_params(direction='in', which='both', length=6)
    ax.yaxis.set_tick_params(direction='in', which='both', length=6)
    ax.xaxis.set_tick_params(which='major', length=9)
    ax.yaxis.set_tick_params(which='major', length=9)

    plt.grid(linestyle="--")
    ax.legend(loc='upper right') # Legend
    plt.savefig('Results/{}.png'.format(plot_name), bbox_inches='tight', dpi=300)    



def plotShared(cent_bins_list, histograms_list):
    fig, axs = plt.subplots(3, 1, sharex=True)
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)


    for i in range(len(histograms_list)):
        print("Processing {}".format(labels_list[i]))
        cent_bins = cent_bins_list[i]
        histograms = histograms_list[i]
        Point_positions, Eff_List, EffError_List, CentralityLabel, bin_sizes = calcEff(cent_bins, histograms[0][0], histograms[0][1])
    
        for j in range(len(Eff_List)):    
            
            #ax.errorbar(Point_positions, Eff_List[j], yerr=EffError_List[j], xerr=bin_sizes, fmt='o', label=r'{}'.format(labels_list[i][0])+', {}'.format(CentralityLabel[j]), markersize=4)    
            ax.errorbar(Point_positions, Eff_List[j], yerr=EffError_List[j], xerr=bin_sizes, fmt='o', label=r'{}'.format(labels_list[i][0])+'{}'.format(CentralityLabel[j]), markersize=4)    
            #ax.errorbar(Point_positions, Eff_List[j], yerr=EffError_List[j], xerr=bin_sizes, fmt='o', label=r'{}'.format(labels_list[i][0]), markersize=4)    


    # Plot each graph, and manually set the y tick values
    axs[0].plot(t, s1)
    axs[1].plot(t, s2)
    axs[2].plot(t, s3)

    ##############################

    axs[0].set_xlabel(r'$p_{T}$ (GeV/c)', fontsize=15, loc='right')
    axs[0].set_xlim((0,10.001))
    axs[0].xaxis.set_ticks_position('both')
    axs[0].set_xticks(np.arange(0, 10.001, 1.0))
    axs[0].xaxis.set_major_locator(MultipleLocator(1.0))                                                                                                                                                                                             
    axs[0].xaxis.set_minor_locator(AutoMinorLocator())
    axs[0].xaxis.set_tick_params(direction='in', which='both', length=6)
    axs[0].xaxis.set_tick_params(which='major', length=9)

    YLabels = ['Efficiency x Acceptance', 'Acceptably tracked / Findable', 'Found/Acceptably tracked']
    for yxis in range(3):
        axs[yxis].set_ylim(0, 1.0)
        axs[yxis].set_ylabel(YLabels[yxis], fontsize=15, loc='top')

        axs[yxis].yaxis.set_ticks_position('both')
        axs[yxis].set_yticks(np.arange(0, 1.0, 0.1))
        axs[yxis].yaxis.set_major_locator(MultipleLocator(0.1))                                                                                                                                                                          
        axs[yxis].yaxis.set_minor_locator(AutoMinorLocator())
        axs[yxis].yaxis.set_tick_params(direction='in', which='both', length=6)
        axs[yxis].yaxis.set_tick_params(which='major', length=9)

    plt.grid(linestyle="--")

    plt.show()


##################### V6 plots

cent_bins_list = [[0, 5],
                  [0, 5],
                  [0, 5]]  # List of lists of centrality bin indices

labels_list = [["Findable"],
              ["Found"],
              ["Accept. tra."]] # prefix


efficiency_histos = [[[hFindSpeciesAll, hGenSpecies]],
                  [[hFoundSpeciesAll, hGenSpecies]],
                  [[hAccTrackSpeciesAll, hGenSpecies]]]  



histograms_list = [[[hFindSpeciesAll, hGenSpecies]],
                  [[hFoundSpeciesAll, hGenSpecies]],
                  [[hAccTrackSpeciesAll, hGenSpecies]]]  # List of lists of histograms


#plotEff(cent_bins_list, histograms_list, labels_list, "Efficiency2_{}".format(Species), "Efficiency x Acceptance")
