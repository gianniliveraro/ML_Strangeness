import uproot
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator) 
import numpy as np

fPlotErrors = True

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

# Operations
print("FoundEdges_Centrality: ", FoundEdges_Centrality)
print("FoundEdges_PT: ", FoundEdges_PT)

# Calculate bin sizes based on FoundEdges_PT
bin_sizes = np.diff(FoundEdges_PT)/2

# # Calculate Efficiency and error propagation
# Efficiency = Foundbin_values[1]/Findbin_values[1]
# Efficiency_error = Efficiency * np.sqrt((Foundbin_errors[1] / Foundbin_values[1])**2 + (Findbin_errors[1] / Findbin_values[1])**2)

# Plot the histogram
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)

if fPlotErrors:
    cent_bin = 0 
    # Calculate Efficiency and error propagation
    Efficiency = Foundbin_values[cent_bin]/Findbin_values[cent_bin]
    Efficiency_error = Efficiency * np.sqrt((Foundbin_errors[cent_bin] / Foundbin_values[cent_bin])**2 + (Findbin_errors[cent_bin] / Findbin_values[cent_bin])**2)
    #ax.errorbar(FoundEdges_PT[:-1], Efficiency, yerr=Efficiency_error, xerr=bin_sizes, fmt='o', color='b', label='{}-{}\%'.format(FoundEdges_Centrality[i], FoundEdges_Centrality[i+1]), markersize=4)
    ax.errorbar(FoundEdges_PT[:-1], Efficiency, yerr=Efficiency_error, xerr=bin_sizes, fmt='o', label='{}-{}%'.format(FoundEdges_Centrality[cent_bin], FoundEdges_Centrality[cent_bin+1]), markersize=4)
else:
    # Plot the histogram
    ax.hist(FoundEdges_PT[:-1], bins=FoundEdges_PT, weights=Efficiency, histtype='step', fill=False, edgecolor='blue', align='mid', linewidth=1, density=False)

#------------------------------------------------
# Plot configs: 
plt.figtext(0.275, 0.470, r"$\bf{ALICE}$" + '\n Pb-Pb at $\sqrt{s}=5.36$ TeV', ha='center') # ALICE

ax.set_xlim((0,10.001))
ax.set_ylim((0,1.01))

ax.set_ylabel(r'Efficiency', fontsize=15, loc='top')
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
plt.savefig('Eff.png', bbox_inches='tight')
