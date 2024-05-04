void DrawEfficiency01(TString lSpecies = "K0Short"){
  // Decide on binning, please
  Double_t centralityBins[] = { 0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90};
  Int_t nCentralityBins = sizeof(centralityBins)/sizeof(Double_t) - 1;
  
  gStyle->SetOptStat(0);
  TCanvas *c1 = new TCanvas("c1","c1",800,600);
  c1->SetTicks(1,1);
  c1->SetTopMargin(0.02);
  c1->SetBottomMargin(0.15);
  c1->SetLeftMargin(0.16);
  c1->SetRightMargin(0.19);
  c1->SetFrameFillStyle(0);
  c1->SetFillStyle(0);
  c1->SetLogy();
  
  //Color palette, please
  const int NRGBs = 5;
  double stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
  double red[NRGBs]   = { 0.00, 0.00, 0.9*0.87, 1.00, 0.51 };
  double green[NRGBs] = { 0.00, 0.81, 0.9*1.00, 0.20, 0.00 };
  double blue[NRGBs]  = { 0.51, 0.9*1.00, 0.12, 0.00, 0.00 };
  
  int FI = TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, 10);
  int color[300];
  for(int i=0; i<10;++i) color[i] = FI + 10 - 1 - i;
  
  Double_t lNormalization[10];
  TH1D *hK0Stat[10];
  TH1D *hSpectraData[10];
  for(Int_t ibin = 0; ibin < 10; ibin++)
  { // begin loop on centrality
    cout<<"Plot centrality: "<<centralityBins[ibin]<<"-"<<centralityBins[ibin+1]<<"%"<<endl;

    TFile *file = new TFile(Form("%s_MonteCarloNew_%.0f_%.0f.root", lSpecies.Data(), centralityBins[ibin], centralityBins[ibin+1]));
    TList *resultList = (TList*) file->Get("resultHistograms");
    resultList -> SetName("listMonteCarlo");
    
    hK0Stat[ibin] = (TH1D*)resultList->FindObject("fHistRawVsPt");
    hK0Stat[ibin]->SetName(Form("hK0Stat_%i", ibin));
    
    //Apply scaling factor, please
    //hK0Stat[ibin]->Scale(1./TMath::Power(2,ibin));
    hK0Stat[ibin]->SetLineColor(color[ibin]);
    hK0Stat[ibin]->SetMarkerStyle(20);
    hK0Stat[ibin]->SetMarkerColor(color[ibin]);

    TH1D* thisNormHisto = (TH1D*)resultList->FindObject("fNorm");
    lNormalization[ibin] = thisNormHisto->GetBinContent(1);
    cout<<"Normalization for this bin: "<<lNormalization[ibin]<<endl;
    
    // get data
    TFile *fileData = new TFile(Form("%s_Data_%.0f_%.0f.root", lSpecies.Data(), centralityBins[ibin], centralityBins[ibin+1]));
    TList *resultListData = (TList*) fileData->Get("resultHistograms");
    resultListData->SetName("listData");
    
    hSpectraData[ibin] = (TH1D*)resultListData->FindObject("fHistRawVsPt");
    hSpectraData[ibin]->SetName(Form("hSpectraData_%i", ibin));
    
    hSpectraData[ibin]->SetLineColor(color[ibin]);
    hSpectraData[ibin]->SetMarkerStyle(20);
    hSpectraData[ibin]->SetMarkerColor(color[ibin]);

  }
  
  TH1D *hDummy = new TH1D("hDummy", ";#it{p}_{T} (GeV/#it{c});1/#it{N}_{evt} d^{2}#it{N}_{raw}/(d#it{p}_{T}d#it{y}) (GeV/#it{c})^{-1}", 3000, 0, 20);
  hDummy->SetTitle("");
  hDummy->GetYaxis()->SetTitleSize(0.055);
  hDummy->GetXaxis()->SetTitleSize(0.055);
  hDummy->GetYaxis()->SetLabelSize(0.036);
  hDummy->GetXaxis()->SetLabelSize(0.036);
  hDummy->GetXaxis()->SetNdivisions(509);
  hDummy->GetYaxis()->SetNdivisions(509);
  hDummy->GetXaxis()->SetRangeUser(0, 13.5);
  hDummy->GetYaxis()->SetRangeUser(2e-8, 6);
  
  hDummy->Draw();
  for(Int_t ibin = 0; ibin < 10; ibin++){
    hK0Stat[ibin]->Draw("same");
  }
  Double_t lXspec = 0.7, lYspec = 0.8;
  TLatex *lat = new TLatex();
  lat->SetTextAlign(22);
  lat->SetTextFont(42);
  lat->SetTextSize(0.1);
  if(lSpecies == "K0Short") lat->DrawLatexNDC(lXspec,lYspec,"K^{0}_{S}");
  if(lSpecies == "Lambda") lat->DrawLatexNDC(lXspec,lYspec,"#Lambda");
  if(lSpecies == "AntiLambda") lat->DrawLatexNDC(lXspec,lYspec,"#bar{#Lambda}");
  
  
  lat->SetTextSize(0.05);
  lat->DrawLatexNDC(lXspec-0.1,lYspec+0.10,"ALICE Pb-Pb 5.36TeV");
  lat->SetTextSize(0.1);
  
  Double_t lGlobalYoffset = 0.035;
  
  c1->cd(2); //this is an empty canvas so far
  TLegend *legV0 = new TLegend(0.815, 0.15, 0.98,0.5);
  legV0->SetMargin(0.2);
  legV0->SetTextSize(0.030);
  legV0->SetFillStyle(0);
  
  for(Int_t i=0; i<10; i++){
      cout<<"adding legend entry with text: "<<Form("%1.f-%1.f%% #times 2^{-%i}", centralityBins[i],centralityBins[i+1], i )<<endl;
      if ( i!=0){
          legV0->AddEntry(hK0Stat[i], Form("%1.f-%1.f%% #times 2^{-%i}", centralityBins[i],centralityBins[i+1], i ) , "lp" );
      }else{
          legV0->AddEntry(hK0Stat[i], Form("%1.f-%1.f%%", centralityBins[i],centralityBins[i+1]) , "lp" );
      }
  }
  legV0->SetBorderSize(0);
  legV0->Draw();
  c1->SaveAs(Form("%s_montecarloraw.pdf", lSpecies.Data()));
  
  // ________________________________________________________________________
  // efficiency calculation
  TFile *file = new TFile("AnalysisResults.root");

  // control plot please
  TCanvas *cControlMCGen = new TCanvas("cControlMCGen","cControlMCGen",800,600);
  cControlMCGen->SetTicks(1,1);
  cControlMCGen->SetTopMargin(0.02);
  cControlMCGen->SetBottomMargin(0.15);
  cControlMCGen->SetLeftMargin(0.16);
  cControlMCGen->SetRightMargin(0.19);
  cControlMCGen->SetFrameFillStyle(0);
  cControlMCGen->SetFillStyle(0);
  cControlMCGen->SetLogy();
  
  
  
  TH1D *hGenerated[10];
  for(Int_t i=0; i<10; i++){
    TH2F* h2dGenerated = (TH2F*)file->Get(Form("derivedlambdakzeroanalysis/h2dGen%s", lSpecies.Data()));
    h2dGenerated->SetName(Form("hGenerated_%i", i));
                                          
    // project out the stuff we want only, please
    int ibLim1 = h2dGenerated->GetXaxis()->FindBin(centralityBins[i]+1e-5);
    int ibLim2 = h2dGenerated->GetXaxis()->FindBin(centralityBins[i+1]-1e-5);
    
    hGenerated[i] = (TH1D*) h2dGenerated->ProjectionY(Form("hGenerated_%i", i), ibLim1, ibLim2);
    
    hGenerated[i]->SetLineColor(color[i]);
    hGenerated[i]->SetMarkerStyle(20);
    hGenerated[i]->SetMarkerColor(color[i]);
    hGenerated[i]->Scale(1., "width");
    hGenerated[i]->Draw("same");
    
    hK0Stat[i]->Scale(lNormalization[i]);
    hK0Stat[i]->Divide(hGenerated[i]);
    
  }
  
  // control plot please
  TCanvas *cEfficiency = new TCanvas("cEfficiency","cEfficiency",800,600);
  cEfficiency->SetTicks(1,1);
  cEfficiency->SetTopMargin(0.02);
  cEfficiency->SetBottomMargin(0.15);
  cEfficiency->SetLeftMargin(0.16);
  cEfficiency->SetRightMargin(0.19);
  cEfficiency->SetFrameFillStyle(0);
  cEfficiency->SetFillStyle(0);
  
  
  TH1D *hDummy2 = new TH1D("hEff", ";#it{p}_{T} (GeV/#it{c});Efficiency #times acceptance", 3000, 0, 20);
  hDummy2->SetTitle("");
  hDummy2->GetYaxis()->SetTitleSize(0.055);
  hDummy2->GetXaxis()->SetTitleSize(0.055);
  hDummy2->GetYaxis()->SetLabelSize(0.036);
  hDummy2->GetXaxis()->SetLabelSize(0.036);
  hDummy2->GetXaxis()->SetNdivisions(509);
  hDummy2->GetYaxis()->SetNdivisions(509);
  
  
  hDummy2->GetXaxis()->SetRangeUser(0, 6.5);
  if(lSpecies.Contains("Lambda"))
    hDummy2->GetXaxis()->SetRangeUser(0, 3.9);
  hDummy2->GetYaxis()->SetRangeUser(0, 0.2399);
  hDummy2->Draw();
  
  for(Int_t i=0; i<10; i++){
    hK0Stat[i]->Draw("same");
  }

  lat->SetTextAlign(22);
  lat->SetTextFont(42);
  lat->SetTextSize(0.1);
  if(lSpecies == "K0Short") lat->DrawLatexNDC(lXspec,lYspec,"K^{0}_{S}");
  if(lSpecies == "Lambda") lat->DrawLatexNDC(lXspec,lYspec,"#Lambda");
  if(lSpecies == "AntiLambda") lat->DrawLatexNDC(lXspec,lYspec,"#bar{#Lambda}");
  lat->SetTextSize(0.05);
  lat->DrawLatexNDC(lXspec-0.1,lYspec+0.10,"ALICE Pb-Pb 5.36TeV");
  lat->SetTextSize(0.1);
  
  //Double_t lGlobalYoffset = 0.035;
  
  TLegend *legEff = new TLegend(0.815, 0.15, 0.98,0.5);
  legEff->SetMargin(0.2);
  legEff->SetTextSize(0.030);
  legEff->SetFillStyle(0);
  
  for(Int_t i=0; i<10; i++){
      cout<<"adding legend entry with text: "<<Form("%1.f-%1.f%% #times 2^{-%i}", centralityBins[i],centralityBins[i+1], i )<<endl;
        legEff->AddEntry(hK0Stat[i], Form("%1.f-%1.f%%", centralityBins[i],centralityBins[i+1]) , "lp" );
  }
  legEff->SetBorderSize(0);
  legEff->Draw();
  cEfficiency->SaveAs(Form("%s_montecarloefficiency.pdf", lSpecies.Data()));
  
  
} 