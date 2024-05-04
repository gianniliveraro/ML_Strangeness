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
# 10_PlotEfficiency
# ================
#
# This script plots the efficiency for particle species (please, run it inside O2Physics environment)
# Original script by David Chinellato
# Modified by Gianni S. S. Liveraro
#
#    Comments, questions, complaints, suggestions?
#    Please write to:
#    gianni.shigeru.setoue.liveraro@cern.ch
#    david.dobrigkeit.chinellato@cern.ch
#____________________________
# Imports
import ROOT
import array

def DrawEfficiency01(lSpecies="K0Short"):
    # Decide on binning, please
    centralityBins = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    nCentralityBins = len(centralityBins) - 1
    
    ROOT.gStyle.SetOptStat(0)
    c1 = ROOT.TCanvas("c1", "c1", 800, 600)
    c1.SetTicks(1, 1)
    c1.SetTopMargin(0.02)
    c1.SetBottomMargin(0.15)
    c1.SetLeftMargin(0.16)
    c1.SetRightMargin(0.19)
    c1.SetFrameFillStyle(0)
    c1.SetFillStyle(0)
    c1.SetLogy()

    # Color palette, please
    NRGBs = 5
    stops = array.array('d', [0.00, 0.34, 0.61, 0.84, 1.00])
    red = array.array('d', [0.00, 0.00, 0.9*0.87, 1.00, 0.51])
    green = array.array('d', [0.00, 0.81, 0.9*1.00, 0.20, 0.00])
    blue = array.array('d', [0.51, 0.9*1.00, 0.12, 0.00, 0.00])

    FI = ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, 10)
    color = [FI + 10 - 1 - i for i in range(10)]

    lNormalization = []
    hK0Stat = []
    hSpectraData = []

    for ibin in range(10):
        print("Plot centrality:", centralityBins[ibin], "-", centralityBins[ibin + 1], "%")

        file = ROOT.TFile(f"{lSpecies}_MonteCarloNew_{centralityBins[ibin]}_{centralityBins[ibin + 1]}.root")
        resultList = file.Get("resultHistograms")
        resultList.SetName("listMonteCarlo")
        
        hK0Stat.append(resultList.FindObject("fHistRawVsPt"))
        hK0Stat[ibin].SetName(f"hK0Stat_{ibin}")
        
        hK0Stat[ibin].SetLineColor(color[ibin])
        hK0Stat[ibin].SetMarkerStyle(20)
        hK0Stat[ibin].SetMarkerColor(color[ibin])

        thisNormHisto = resultList.FindObject("fNorm")
        lNormalization.append(thisNormHisto.GetBinContent(1))
        print("Normalization for this bin:", lNormalization[ibin])

        fileData = ROOT.TFile(f"{lSpecies}_Data_{centralityBins[ibin]}_{centralityBins[ibin + 1]}.root")
        resultListData = fileData.Get("resultHistograms")
        resultListData.SetName("listData")
        
        hSpectraData.append(resultListData.FindObject("fHistRawVsPt"))
        hSpectraData[ibin].SetName(f"hSpectraData_{ibin}")
        
        hSpectraData[ibin].SetLineColor(color[ibin])
        hSpectraData[ibin].SetMarkerStyle(20)
        hSpectraData[ibin].SetMarkerColor(color[ibin])

    hDummy = ROOT.TH1D("hDummy", ";#it{p}_{T} (GeV/#it{c});1/#it{N}_{evt} d^{2}#it{N}_{raw}/(d#it{p}_{T}d#it{y}) (GeV/#it{c})^{-1}", 3000, 0, 20)
    hDummy.SetTitle("")
    hDummy.GetYaxis().SetTitleSize(0.055)
    hDummy.GetXaxis().SetTitleSize(0.055)
    hDummy.GetYaxis().SetLabelSize(0.036)
    hDummy.GetXaxis().SetLabelSize(0.036)
    hDummy.GetXaxis().SetNdivisions(509)
    hDummy.GetYaxis().SetNdivisions(509)
    hDummy.GetXaxis().SetRangeUser(0, 13.5)
    hDummy.GetYaxis().SetRangeUser(2e-8, 6)
    
    hDummy.Draw()
    for ibin in range(10):
        hK0Stat[ibin].Draw("same")

    lXspec, lYspec = 0.7, 0.8
    lat = ROOT.TLatex()
    lat.SetTextAlign(22)
    lat.SetTextFont(42)
    lat.SetTextSize(0.1)
    if lSpecies == "K0Short":
        lat.DrawLatexNDC(lXspec, lYspec, "K^{0}_{S}")
    if lSpecies == "Lambda":
        lat.DrawLatexNDC(lXspec, lYspec, "#Lambda")
    if lSpecies == "AntiLambda":
        lat.DrawLatexNDC(lXspec, lYspec, "#bar{#Lambda}")
    
    lat.SetTextSize(0.05)
    lat.DrawLatexNDC(lXspec - 0.1, lYspec + 0.10, "ALICE Pb-Pb 5.36TeV")
    lat.SetTextSize(0.1)
    
    c1.cd(2)  # this is an empty canvas so far
    legV0 = ROOT.TLegend(0.815, 0.15, 0.98, 0.5)
    legV0.SetMargin(0.2)
    legV0.SetTextSize(0.030)
    legV0.SetFillStyle(0)
    
    for i in range(10):
        print("adding legend entry with text:", f"{centralityBins[i]}-{centralityBins[i + 1]}% #times 2^{-i}")
        if i != 0:
            legV0.AddEntry(hK0Stat[i], f"{centralityBins[i]}-{centralityBins[i + 1]}% #times 2^{-i}", "lp")
        else:
            legV0.AddEntry(hK0Stat[i], f"{centralityBins[i]}-{centralityBins[i + 1]}%", "lp")
    
    legV0.SetBorderSize(0)
    legV0.Draw()
    c1.SaveAs(f"{lSpecies}_montecarloraw.pdf")

    # efficiency calculation
    file = ROOT.TFile("AnalysisResults_0.root")

    # control plot please
    cControlMCGen = ROOT.TCanvas("cControlMCGen", "cControlMCGen", 800, 600)
    cControlMCGen.SetTicks(1, 1)
    cControlMCGen.SetTopMargin(0.02)
    cControlMCGen.SetBottomMargin(0.15)
    cControlMCGen.SetLeftMargin(0.16)
    cControlMCGen.SetRightMargin(0.19)
    cControlMCGen.SetFrameFillStyle(0)
    cControlMCGen.SetFillStyle(0)
    cControlMCGen.SetLogy()

    hGenerated = []
    for i in range(10):
        h2dGenerated = file.Get("strangederivedbuilder/h2dGen{}".format(lSpecies))
        print(h2dGenerated)
        h2dGenerated.SetName(f"hGenerated_{i}")

        # project out the stuff we want only, please
        ibLim1 = h2dGenerated.GetXaxis().FindBin(centralityBins[i] + 1e-5)
        ibLim2 = h2dGenerated.GetXaxis().FindBin(centralityBins[i + 1] - 1e-5)
        
        hGenerated.append(h2dGenerated.ProjectionY(f"hGenerated_{i}", ibLim1, ibLim2))
        
        hGenerated[i].SetLineColor(color[i])
        hGenerated[i].SetMarkerStyle(20)
        hGenerated[i].SetMarkerColor(color[i])
        hGenerated[i].Scale(1., "width")
        hGenerated[i].Draw("same")
        
        hK0Stat[i].Scale(lNormalization[i])
        hK0Stat[i].Divide(hGenerated[i])

    # control plot please
    cEfficiency = ROOT.TCanvas("cEfficiency", "cEfficiency", 800, 600)
    cEfficiency.SetTicks(1, 1)
    cEfficiency.SetTopMargin(0.02)
    cEfficiency.SetBottomMargin(0.15)
    cEfficiency.SetLeftMargin(0.16)
    cEfficiency.SetRightMargin(0.19)
    cEfficiency.SetFrameFillStyle(0)
    cEfficiency.SetFillStyle(0)

    hDummy2 = ROOT.TH1D("hEff", ";#it{p}_{T} (GeV/#it{c});Efficiency #times acceptance", 3000, 0, 20)
    hDummy2.SetTitle("")
    hDummy2.GetYaxis().SetTitleSize(0.055)
    hDummy2.GetXaxis().SetTitleSize(0.055)
    hDummy2.GetYaxis().SetLabelSize(0.036)
    hDummy2.GetXaxis().SetLabelSize(0.036)
    hDummy2.GetXaxis().SetNdivisions(509)
    hDummy2.GetYaxis().SetNdivisions(509)

    hDummy2.GetXaxis().SetRangeUser(0, 6.5)
    if "Lambda" in lSpecies:
        hDummy2.GetXaxis().SetRangeUser(0, 3.9)
    hDummy2.GetYaxis().SetRangeUser(0, 0.2399)
    hDummy2.Draw()
    
    for i in range(10):
        hK0Stat[i].Draw("same")

    lat.SetTextAlign(22)
    lat.SetTextFont(42)
    lat.SetTextSize(0.1)
    if lSpecies == "K0Short":
        lat.DrawLatexNDC(lXspec, lYspec, "K^{0}_{S}")
    if lSpecies == "Lambda":
        lat.DrawLatexNDC(lXspec, lYspec, "#Lambda")
    if lSpecies == "AntiLambda":
        lat.DrawLatexNDC(lXspec, lYspec, "#bar{#Lambda}")
    lat.SetTextSize(0.05)
    lat.DrawLatexNDC(lXspec - 0.1, lYspec + 0.10, "ALICE Pb-Pb 5.36TeV")
    lat.SetTextSize(0.1)

    legEff = ROOT.TLegend(0.815, 0.15, 0.98, 0.5)
    legEff.SetMargin(0.2)
    legEff.SetTextSize(0.030)
    legEff.SetFillStyle(0)

    for i in range(10):
        print("adding legend entry with text:", f"{centralityBins[i]}-{centralityBins[i + 1]}%")
        legEff.AddEntry(hK0Stat[i], f"{centralityBins[i]}-{centralityBins[i + 1]}%", "lp")

    legEff.SetBorderSize(0)
    legEff.Draw()
    cEfficiency.SaveAs(f"{lSpecies}_montecarloefficiency.pdf")

DrawEfficiency01()
