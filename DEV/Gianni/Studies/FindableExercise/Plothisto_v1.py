import uproot
import matplotlib.pyplot as plt

fPlotErrors = False

# Open the ROOT file and access the histogram
file = uproot.open("FindableSigma0Lambdas.root")
histogram = file["findable-study/hCentrality"]

# Extract bin edges, values, and errors
bin_edges = histogram.axis(axis=0).edges()
bin_values = histogram.values()
bin_errors = histogram.errors()

# Plot the histogram

if fPlotErrors:
    plt.figure(figsize=(8, 6))
    plt.errorbar(bin_edges[:-1], bin_values, yerr=bin_errors, fmt='o', color='b', label='Data', markersize=1)
    plt.xlabel('X axis label')
    plt.ylabel('Y axis label')
    plt.title('Histogram Title')
    plt.legend()
    plt.grid(linestyle="--")
    plt.savefig('hCentrality.png', bbox_inches='tight')

else:
    print("bin_values: ", bin_values)
    # Plot the histogram
    plt.figure(figsize=(8, 6))
    plt.hist(bin_edges[:-1], bins=bin_edges, weights=bin_values, histtype='step', fill=False, edgecolor='blue', align='mid', linewidth=1, density=False)
    plt.xlabel('X axis label')
    plt.ylabel('Y axis label')
    plt.title('Histogram Title')
    plt.grid(linestyle="--")
    plt.savefig('hCentrality.png', bbox_inches='tight')
