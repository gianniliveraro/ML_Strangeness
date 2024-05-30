import uproot
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator) 
import numpy as np

# Open the ROOT file and access the histogram
file = uproot.open("FindableSigma0Lambdas.root")
histoFindable = file["findable-study/h2dPtVsCentrality_All_Findable"]
histoFound = file["findable-study/h2dPtVsCentrality_All_Found"]

# Extract bin edges, values, and errors
## Findable
FindEdges_Centrality = histoFindable.axis(axis=0).edges()
FindEdges_PT = histoFindable.axis(axis=1).edges()
Findbin_values = histoFindable.values()
Findbin_errors = histoFindable.errors()

## Findable
FoundEdges_Centrality = histoFound.axis(axis=0).edges()
FoundEdges_PT = histoFound.axis(axis=1).edges()
Foundbin_values = histoFound.values()
Foundbin_errors = histoFound.errors()

print('FoundEdges_Centrality', FoundEdges_Centrality)
# Calculate bin sizes based on FoundEdges_PT
bin_sizes = np.diff(FoundEdges_PT)/2
FoundEdges_PT2 = FoundEdges_PT[:-1] + bin_sizes

# Calculating generated histos
fileGen = uproot.open("AnalysisResultsMerged_Reduced.root")
histoGen = fileGen["strangederivedbuilder/h2dGenLambda"]
GenEdges_Centrality = histoGen.axis(axis=0).edges()
GenEdges_PT = histoGen.axis(axis=1).edges()
Genbin_values = histoGen.values()
Genbin_errors = histoGen.errors()

# Calculate bin sizes based on FoundEdges_PT
Genbin_sizes = np.diff(GenEdges_PT)/2
GenEdges_PT2 = GenEdges_PT[:-1] + Genbin_sizes

#---------------------------------------------------
def plotEff(cent_bins, FoundEdges_PT, Foundbin_values, Findbin_values, FoundEdges_Centrality, Findbin_errors, Foundbin_errors, bin_sizes, plot_name, ylabel):
    # Plot the histogram
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)

    for cent_bin in cent_bins:
        # Calculate Efficiency and error propagation
        Efficiency = Foundbin_values[cent_bin]/Findbin_values[cent_bin]
        Efficiency_error = Efficiency * np.sqrt((Foundbin_errors[cent_bin] / Foundbin_values[cent_bin])**2 + (Findbin_errors[cent_bin] / Findbin_values[cent_bin])**2)
        #ax.errorbar(FoundEdges_PT[:-1], Efficiency, yerr=Efficiency_error, xerr=bin_sizes, fmt='o', color='b', label='{}-{}\%'.format(FoundEdges_Centrality[i], FoundEdges_Centrality[i+1]), markersize=4)
        ax.errorbar(FoundEdges_PT, Efficiency, yerr=Efficiency_error, xerr=bin_sizes, fmt='o', label='{}-{}%'.format(FoundEdges_Centrality[cent_bin], FoundEdges_Centrality[cent_bin+1]), markersize=4)

    #------------------------------------------------
    # Plot configs: 
    plt.figtext(0.275, 0.470, r"$\bf{ALICE}$" + '\n Pb-Pb at $\sqrt{s}=5.36$ TeV', ha='center') # ALICE

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
    ax.legend(loc='center right') # Legend
    plt.savefig('{}.png'.format(plot_name), bbox_inches='tight')    

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

    return New_Bin, New_Error 

# Found/Findable
cent_bins = [0, 5]
plotEff(cent_bins, FoundEdges_PT2, Foundbin_values, Findbin_values, 
        FoundEdges_Centrality, Findbin_errors, 
        Foundbin_errors, bin_sizes, "Accept_x_Findable", "Acceptably tracked / Findable")

# Efficiency

# Centrality rebinning!
NewCentralityBins = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Rebinning
NewBin_Values, NewError_Values = Rebin(NewCentralityBins, GenEdges_Centrality, Genbin_values)

cent_bins = [0, 1]
plotEff(cent_bins, GenEdges_PT2, Findbin_values, 
        NewBin_Values, NewCentralityBins, NewError_Values, 
        Findbin_errors, Genbin_sizes, "Efficiency", "Efficiency x Acceptance")