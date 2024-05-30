import ROOT
import random

# Number of random values to generate
N = 50000

# Set a random seed for reproducibility
seed = 42
random.seed(seed)
save2D = True
fGen = False

if fGen:
    file = ROOT.TFile("Dummy_Generated.root", "RECREATE")
    if save2D: hist = ROOT.TH2F("h2dGenLambda", "Random Values Histogram", 10, 0, 10, 50, 0, 50)
    else: hist = ROOT.TH1F("h2dGenLambda", "Random Values Histogram", 10, 0, 10)
else:
    file = ROOT.TFile("Dummy_Findable.root", "RECREATE")
    if save2D: hist = ROOT.TH2F("h2dPtVsCentrality_All_Findable", "Random Values Histogram", 10, 0, 10, 50, 0, 50)
    else: hist = ROOT.TH1F("h2dPtVsCentrality_All_Findable", "Random Values Histogram", 10, 0, 10)

# Fill the histogram with N random values
for _ in range(N):
    valuex = random.gauss(0, 10)  # Gaussian distributed random number (mean=0, sigma=1)
    valuey = random.gauss(0, 50)  # Gaussian distributed random number (mean=0, sigma=1)

    if save2D:
        hist.Fill(valuex, valuey)
    else:
        hist.Fill(valuex)
    # for value in range(0, 10):
    #     hist.Fill(value)

# Write the histogram to the ROOT file and close the file
hist.Write()
file.Close()
