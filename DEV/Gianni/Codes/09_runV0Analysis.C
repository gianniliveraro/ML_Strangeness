#include "TList.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH1D.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TF1.h"
#include "TMath.h"
#include "TVirtualFitter.h"
#include "TFitResult.h"
#include "TFitResultPtr.h"
#include "TStopwatch.h"
#include <iostream>
#include <TROOT.h>
#include <TSystem.h>
#include "strangenessModule.h"
using namespace std;

int 09_runV0Analysis(){
  cout<<"----------------------------------------------------"<<endl;
  cout<<"               V0 Analysis Macro "<<endl;
  cout<<"----------------------------------------------------"<<endl;
  // //Initialize Analysis Object
  strangenessModule *mod = new strangenessModule("module", "");

  // Decide on binning, please 
  Double_t centralityBins[] = { 0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90};
  Int_t nCentralityBins = sizeof(centralityBins)/sizeof(Double_t) - 1;

  Double_t ptBins[] = {0.0f, 0.1f, 0.2f, 0.3f, 0.4f, 0.5f, 0.6f, 0.7f, 0.8f, 0.9f, 1.0f, 1.1f, 1.2f, 1.3f, 1.4f, 1.5f, 1.6f, 1.7f, 1.8f, 1.9f, 2.0f, 2.2f, 2.4f, 2.6f, 2.8f, 3.0f, 3.2f, 3.4f, 3.6f, 3.8f, 4.0f, 4.4f, 4.8f, 5.2f, 5.6f, 6.0f, 6.5f, 7.0f, 7.5f, 8.0f, 9.0f, 10.0f, 11.0f, 12.0f, 13.0f, 14.0f, 15.0f, 17.0f, 19.0f, 21.0f, 23.0f, 25.0f, 30.0f, 35.0f, 40.0f, 50.0f};

  //Double_t ptBins[] = {0.0f, 0.1f, 0.2f, 0.3f, 0.4f, 0.5f, 0.6f, 0.7f, 0.8f, 0.9f, 1.0f, 1.1f, 1.2f, 1.3f, 1.4f, 1.5f, 1.6f, 1.7f, 1.8f, 1.9f, 2.0f, 2.2f, 2.4f, 2.6f, 2.8f, 3.0f, 3.2f, 3.4f, 3.6f, 3.8f, 4.0f};
  
  // Double_t ptBins[] = {0.8f, 0.9f, 1.0f, 1.1f, 1.2f, 1.3f, 1.4f, 1.5f, 1.6f, 1.7f, 1.8f, 1.9f, 2.0f, 2.2f, 2.4f, 2.6f, 2.8f, 3.0f, 3.2f, 3.4f, 3.6f, 3.8f, 4.0f, 4.4f, 4.8f, 5.2f, 5.6f, 6.0f, 6.5f, 7.0f, 7.5f, 8.0f, 9.0f, 10.0f}; 

  //Double_t ptBins[] = {1, 2}; 
  
  const Int_t nPtBins = sizeof(ptBins)/sizeof(Double_t) - 1;

  // process this bin? 
  Bool_t workBin[nPtBins];


  //Double_t ptBins[] = {1, 2}; 

  cout<<"Setting binning..."<<endl; 
  mod->SetPtBinning(nPtBins, ptBins);
  mod->SetMassGuess(0.497);
  mod->SetMassOffset(0.0425);
  mod->SetSigExtRanges(-8, -4, -4, +4, +4, +8);
  
  // Open output file
  //  TFile *file = new TFile("AnalysisResults-001-new.root","READ");
  //  mod->SetSignalExtractionMethod("linear"); // if data
  
  TFile *file = new TFile("AnalysisResultsMC-new.root","READ");
  mod->SetSignalExtractionMethod("MC"); // if MC
  
  TH1F *hEventCentrality = (TH1F*) file->Get("derivedlambdakzeroanalysis/hEventCentrality"); 
  cout<<"Total events in this file: "<<hEventCentrality->GetEntries()<<endl;

  TH3F *h3dA = (TH3F*) file->Get("derivedlambdakzeroanalysis/h3dMassK0Short");
  //TH3F *h3dA = (TH3F*) file->Get("derivedlambdakzeroanalysis_Lambda/h3dMassLambda");
  //TH3F *h3dA = (TH3F*) file->Get("derivedlambdakzeroanalysis/h3dMassAntiLambda");
  
  //TH3F *h3dA = (TH3F*) file->Get("derivedlambdakzeroanalysis_Lambda/h3dMassLambda");
  //TH3F *h3dA = (TH3F*) file->Get("derivedlambdakzeroanalysis_Lambda_WithTOFsel/h3dMassLambda");

  for(Int_t ic=0; ic<nCentralityBins; ic++){
    int centBin1 = hEventCentrality->FindBin(centralityBins[ic]+1e-6); 
    int centBin2 = hEventCentrality->FindBin(centralityBins[ic+1]-1e-6); 
    Double_t norm = hEventCentrality->Integral(centBin1, centBin2); 
    cout<<"Events in this centrality bin: "<<norm<<endl;

    for( Int_t ib=0; ib<nPtBins; ib++) { 
      workBin[ib] = true;
    }
    mod->SetWorkingBins(nPtBins, workBin);
//
//    mod->SetMassGuess(0.497);
//    mod->SetMassOffset(0.0425);
//    mod->DoAnalysis(h3dK, centralityBins[ic], centralityBins[ic+1], Form("K0Short_MonteCarloNew_%.0f_%.0f.root", centralityBins[ic], centralityBins[ic+1]), norm);

    // don't attempt the same thing
    for( Int_t ib=0; ib<nPtBins; ib++) { 
      workBin[ib] = true;
      if (0.5f*(ptBins[ib]+ptBins[ib+1]) < 0.8 ) workBin[ib] = false;
      if (0.5f*(ptBins[ib]+ptBins[ib+1]) > 5.0 ) workBin[ib] = false;
    }
    mod->SetWorkingBins(nPtBins, workBin);

    mod->SetMassGuess(0.497);
    mod->SetMassOffset(0.0425);
    mod->DoAnalysis(h3dA, centralityBins[ic], centralityBins[ic+1], Form("K0Short_MonteCarloNew2_%.0f_%.0f.root", centralityBins[ic], centralityBins[ic+1]), norm);
    //mod->DoAnalysis(h3dA, centralityBins[ic], centralityBins[ic+1], Form("Lambda_WithTOF_%.0f_%.0f.root", centralityBins[ic], centralityBins[ic+1]), norm);
  }
  return 0;
}
