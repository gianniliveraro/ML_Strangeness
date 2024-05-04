//+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
//
// General class to do weak decay analysis
//
// WARNING: THIS IS EXPERIMENTAL!
//
// Please send any questions, etc to:
//    david.dobrigkeit.chinellato@cern.ch
//
//+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

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
#include "strangenessModule.h"
using namespace std;

ClassImp(strangenessModule);

//________________________________________________________________
strangenessModule::strangenessModule() :
TNamed()
{
  
}

//________________________________________________________________
strangenessModule::strangenessModule(const char * name, const char * title) :
TNamed(name,title)
{
  
}

//________________________________________________________________
strangenessModule::~strangenessModule(){
  // Nothing to delete
}

//________________________________________________________________
void strangenessModule::SetPtBinning(  Long_t lRecNPtBins, Double_t *lRecPtBins  ){
  //Function to set pt binning. First argument is the number of pt bins, second is
  //an array with bin limits.
  lNPtBins = lRecNPtBins;
  for(int ix = 0;ix<lNPtBins+1;ix++){
    lPtBins[ix] = lRecPtBins[ix];
  }
}

//________________________________________________________________
void strangenessModule::SetWorkingBins(  Long_t lRecNPtBins, Bool_t *lWorkBins  ){
  //Function to set bins to be processed. First argument is the number of pt bins, second is
  //an array with bin limits.
  if(lRecNPtBins != lNPtBins)
    cout<<"YOU'RE DOING SOMETHING FISHY"<<endl;
  for(int ix = 0;ix<lNPtBins+1;ix++){
    lWorkingBins[ix] = lWorkBins[ix];
  }
}

//________________________________________________________________
void strangenessModule::SetSigExtRanges( Double_t lRLoLeftBg, Double_t lRHiLeftBg,  Double_t lRLoPeak,
                                        Double_t lRHiPeak,   Double_t lRLoRightBg, Double_t lRHiRightBg ){
  //Function to set signal extraction ranges (in sigmas!)
  lLoLeftBg  = lRLoLeftBg;
  lHiLeftBg  = lRHiLeftBg;
  lLoPeak    = lRLoPeak;
  lHiPeak    = lRHiPeak;
  lLoRightBg = lRLoRightBg;
  lHiRightBg = lRHiRightBg;
}

//________________________________________________________________
Bool_t strangenessModule::CheckCompatibleMultiplicity(TH3F *histogram, Double_t lLoMult, Double_t lHiMult){
  Bool_t lLoMultMatch = kFALSE;
  Bool_t lHiMultMatch = kFALSE;
  for( Long_t ibin = 1; ibin<histogram->GetNbinsX()+2; ibin++){
    Double_t lLowEdge = histogram->GetXaxis()->GetBinLowEdge(ibin);
    if( TMath::Abs( lLowEdge - lLoMult) < 1e-5 ) lLoMultMatch = kTRUE;
    if( TMath::Abs( lLowEdge - lHiMult) < 1e-5 ) lHiMultMatch = kTRUE;
  }
  Bool_t lReturnValue = kFALSE;
  if ( lLoMultMatch && lHiMultMatch ) lReturnValue = kTRUE;
  return lReturnValue;
}

//________________________________________________________________
Bool_t strangenessModule::CheckCompatiblePt(TH3F *histogram){
  Bool_t lMatchFound = kFALSE;
  Bool_t lReturnValue = kTRUE;
  for( Long_t iptbin = 0; iptbin<lNPtBins+1; iptbin++){
    lMatchFound = kFALSE;
    for( Long_t ibin = 1; ibin<histogram->GetNbinsY()+2; ibin++){
      Double_t lLowEdge = histogram->GetYaxis()->GetBinLowEdge(ibin);
      if( TMath::Abs( lLowEdge - lPtBins[iptbin]) < 1e-5 ) lMatchFound = kTRUE;
    }
    if ( ! lMatchFound ){
      cout<<"Incompatible binning for requested boundary #"<<iptbin<<": "<<lPtBins[iptbin]<<endl;
      lReturnValue = kFALSE;
    }
  }
  return lReturnValue;
}

//________________________________________________________________
Bool_t strangenessModule::PerformInitialFit( TH1D *lHisto, Int_t nBin, TH1D *fHistMeanVsPt, TH1D *fHistSigmaVsPt, TList *outputList, TString lOption){
  //Helper function to perform initial gaussian + linear fit
  Double_t integralInRange = lHisto->Integral(lHisto->FindBin(massGuess-massOffset), lHisto->FindBin(massGuess+massOffset));
  if ( lVerbose ) cout<<"Initial fit: histogram received with "<<lHisto->GetEntries()<<" entries, in range: "<<integralInRange<<". Processing."<<endl;
  
  Bool_t lReturnValue = kTRUE; //everything ok = kTRUE
  
  //Will expect to have mass received as mean value here
  TString lName = lHisto->GetName();
  lName.Append("_InitialFit");
  TF1 *fit = 0x0;
  if( lOption == "linear"){
    fit = new TF1(lName.Data(),"[0]+[1]*(x-[5])+[2]*TMath::Gaus(x, [3], [4])", massGuess-massOffset, massGuess+massOffset);
  }else{
    fit = new TF1(lName.Data(),"[0]*TMath::Gaus(x, [1], [2])", massGuess-massOffset, massGuess+massOffset);
  }
  
  //Guess linear parameters
  Double_t lAverageBg = 0.5*(lHisto->GetBinContent(lHisto->GetXaxis()->FindBin(massGuess-massOffset) )
                             +lHisto->GetBinContent(lHisto->GetXaxis()->FindBin(massGuess+massOffset) ));
  Double_t lGuessedSlope = (lHisto->GetBinContent(lHisto->GetXaxis()->FindBin(massGuess+0.010) ) -
                            lHisto->GetBinContent(lHisto->GetXaxis()->FindBin(massGuess-0.010) ) ) /
  ( 0.020 ) ;
  
  if( lOption == "linear"){
    //constant at zero: lAverageBg - lMean*lGuessedSlope
    fit->SetParameter(0, lAverageBg);
    fit->SetParameter(1, lGuessedSlope);
    
    //Guess Gaussian Parameters
    fit->SetParameter(2, lHisto->GetBinContent(lHisto->GetXaxis()->FindBin(massGuess) ) - lAverageBg );
    fit->SetParLimits(2, 1, 50*(lHisto->GetBinContent(lHisto->GetXaxis()->FindBin(massGuess) ) - lAverageBg));
    fit->SetParameter(3, massGuess);
    fit->SetParLimits(3, massGuess-0.006,massGuess+0.006); //ALICE is never off by that much
    fit->SetParameter(4,0.003);
    fit->SetParLimits(4,0.001, 0.015); //ALICE tracking is (usually) never worse than this
    fit->FixParameter(5,massGuess);
  }else{
    //Guess Gaussian Parameters
    fit->SetParameter(0, lHisto->GetBinContent(lHisto->GetXaxis()->FindBin(massGuess) ) - lAverageBg );
    fit->SetParLimits(0, 1, 50*(lHisto->GetBinContent(lHisto->GetXaxis()->FindBin(massGuess) ) - lAverageBg));
    fit->SetParameter(1, massGuess);
    fit->SetParLimits(1, massGuess-0.006,massGuess+0.006); //ALICE is never off by that much
    fit->SetParameter(2,0.003);
    fit->SetParLimits(2,0.001, 0.015); //ALICE tracking is (usually) never worse than this
  }
  
  //Fit options
  TString lFitOptions = "IREM0S";
  if (!lVerbose) lFitOptions.Append("Q") ;
  
  if(integralInRange < 100){
    if ( lVerbose ) cout<<"Fit skipped, too few counts"<<endl;
    return false;
  }
  
  //Printout options used for the fit
  if ( lVerbose ) cout<<"Initial fit to histogram "<<lHisto->GetName()<<" will be carried out with options: "<<lFitOptions.Data()<<", integral here is: "<<integralInRange<<" and mass guess is "<<massGuess<<endl;
  
  //Perform fit
  TFitResultPtr fitResultPtr = lHisto->Fit( lName.Data(), lFitOptions.Data());
  if ( !fitResultPtr ) return false;
  if ( !fitResultPtr->IsValid() ) return false;
  
  //Store to control output
  outputList->Add(fit);
  
  //Provide output variables
  if(lOption == "linear"){
    fHistMeanVsPt->SetBinContent(nBin, fit->GetParameter(3) );
    fHistMeanVsPt->SetBinError(nBin, fit->GetParError(3) );
    fHistSigmaVsPt->SetBinContent(nBin, fit->GetParameter(4) );
    fHistSigmaVsPt->SetBinError(nBin, fit->GetParError(4) );
  }else{
    fHistMeanVsPt->SetBinContent(nBin, fit->GetParameter(1) );
    fHistMeanVsPt->SetBinError(nBin, fit->GetParError(1) );
    fHistSigmaVsPt->SetBinContent(nBin, fit->GetParameter(2) );
    fHistSigmaVsPt->SetBinError(nBin, fit->GetParError(2) );
    
  }
  
  return lReturnValue;
}

//________________________________________________________________
Bool_t strangenessModule::PerformSignalExtraction( TH1D *lHisto, Int_t nBin, TH1D *fHistRawVsPt, TH1D *fHistBgVsPt, TH1D *fHistMeanVsPt, TH1D *fHistSigmaVsPt, TList *lControlList, TString lOption){
  //Helper function to perform actual signal extraction
  Double_t integralInRange = lHisto->Integral(lHisto->FindBin(massGuess-massOffset), lHisto->FindBin(massGuess+massOffset));
  if ( lVerbose ) cout<<"Extract signal: histogram received with "<<lHisto->GetEntries()<<" entries, in range: "<<integralInRange<<". Processing."<<endl;
  if( integralInRange<200) return false;
  
  Bool_t lReturnValue = kTRUE; //everything went alright -> kTRUE
  
  TString lFitOptions = "R0S";
  if (!lVerbose) lFitOptions.Append("Q");
  
  // This could be still improved
  Double_t lMean = fHistMeanVsPt -> GetBinContent(nBin);
  Double_t lSigma = fHistSigmaVsPt -> GetBinContent(nBin);
  
  // sanity check
  if ( TMath::Abs(lMean - massGuess) > 0.03 ) return false; // go home, you're drunk
  if ( TMath::Abs(lSigma) > 0.03 ) return false; // go home, you're drunk
  
  
  //Find bins in which signal extraction is to be performed
  Long_t lBinPeakLo = lHisto->GetXaxis()->FindBin ( lMean + lLoPeak*lSigma );
  Long_t lBinPeakHi = lHisto->GetXaxis()->FindBin ( lMean + lHiPeak*lSigma );
  Long_t lBinLeftBgLo = lHisto->GetXaxis()->FindBin ( lMean + lLoLeftBg*lSigma );
  Long_t lBinLeftBgHi = lHisto->GetXaxis()->FindBin ( lMean + lHiLeftBg*lSigma );
  Long_t lBinRightBgLo = lHisto->GetXaxis()->FindBin ( lMean + lLoRightBg*lSigma );
  Long_t lBinRightBgHi = lHisto->GetXaxis()->FindBin ( lMean + lHiRightBg*lSigma );
  
  //Inclusive on lower and upper limits
  //Get values and use these values for fit ranges: meant to harmonize bin counting wrt fitting
  Double_t lValPeakLo = lHisto->GetBinLowEdge( lBinPeakLo   );
  Double_t lValPeakHi = lHisto->GetBinLowEdge( lBinPeakHi+1 );
  Double_t lValLeftBgLo = lHisto->GetBinLowEdge( lBinLeftBgLo   );
  Double_t lValLeftBgHi = lHisto->GetBinLowEdge( lBinLeftBgHi+1 );
  Double_t lValRightBgLo = lHisto->GetBinLowEdge( lBinRightBgLo   );
  Double_t lValRightBgHi = lHisto->GetBinLowEdge( lBinRightBgHi+1 );
  
  //Get very first guess for linear background
  Double_t lAverageBg = lHisto->Integral(lBinLeftBgLo,lBinLeftBgHi )+lHisto->Integral(lBinRightBgLo,lBinRightBgHi) ;
  lAverageBg = lAverageBg / ( lBinLeftBgHi - lBinLeftBgLo + lBinRightBgHi - lBinRightBgLo + 2);
  
  Double_t lLeftY = lHisto->Integral(lBinLeftBgLo, lBinLeftBgHi  ) / (lBinLeftBgHi - lBinLeftBgLo + 1 );
  Double_t lLeftX = 0.5*(lValLeftBgHi+lValLeftBgLo );
  
  Double_t lRightY = lHisto->Integral(lBinRightBgLo,lBinRightBgHi ) / (lBinRightBgHi - lBinRightBgLo + 1 );
  Double_t lRightX = 0.5*(lValRightBgHi+lValRightBgLo );
  
  Double_t lGuessedSlope = (lRightY-lLeftY)/(lRightX-lLeftX);
  
  Double_t lBgConst = lAverageBg - lMean*lGuessedSlope;
  Double_t lBgSlope = lGuessedSlope;
  
  //Check if this is a low-statistics bin and if so use either "L" or "LL" fit options
  if(integralInRange<200)
    lFitOptions.Append( "L" );
  
  if ( lVerbose ) cout<<"Signal extration fit to histogram "<<lHisto->GetName()<<" will be carried out with options: "<<lFitOptions.Data()<<", integral here is: "<<integralInRange<<" and mass guess is "<<massGuess<<endl;
  
  //Clone histogram and create a control histogram with the peak ranges highlighted
  TString lNameHistoPeak = lHisto->GetName();
  lNameHistoPeak.Append("_Peak");
  TH1D *lHistoPeak = (TH1D*) lHisto->Clone(lNameHistoPeak.Data());
  //lHistoPeak->SetDirectory(0);
  lHistoPeak->Reset();
  for(Long_t ibin=lBinPeakLo; ibin<lBinPeakHi+1; ibin++){
    lHistoPeak->SetBinContent(ibin, lHisto->GetBinContent(ibin));
    lHistoPeak->SetBinError(ibin, lHisto->GetBinError(ibin));
  }
  lControlList->Add(lHistoPeak);
  
  //Pointer to fit (if it exists)
  TF1 *fit           = 0x0;
  TF1 *fitToSubtract = 0x0;
  
  //N.B. if option "MC" is chosen, background will be assumed zero!
  Double_t lSignal = 0.0;
  Double_t lSignalErr = 0.0;
  Double_t lBgEstimate = 0;
  Double_t lBgEstimateError = 0;
  
  if( lOption.Contains("linear") ){
    //Step 1: Perform Linear Fit to start with
    TString lName = lHisto->GetName();
    lName.Append("_LinearFit");
    fit = new TF1(lName.Data(), this, &strangenessModule::BgPol1,
                  lMean + lLoLeftBg*lSigma, lMean + lHiRightBg*lSigma, 4 , "strangenessModule", "BgPol1");
    
    //Start with parameters from initial fit: probably a good initial guess
    fit->FixParameter(0, lMean + lHiLeftBg*lSigma );
    fit->FixParameter(1, lMean + lLoRightBg*lSigma);
    fit->SetParameter(2, lBgConst);
    fit->SetParameter(3, lBgSlope);
    
    //Perform fit
    
    TFitResultPtr fitResultPtr = lHisto->Fit( lName.Data(), lFitOptions.Data());
    if ( !fitResultPtr->IsValid() ) lReturnValue = kFALSE; //went bad
    
    TString lNameToSubtract = lHisto->GetName();
    lNameToSubtract.Append("_FitToSubtract");
    fitToSubtract = new TF1(lNameToSubtract.Data(), "[0]+[1]*x",
                            lMean + lLoLeftBg*lSigma, lMean + lHiRightBg*lSigma);
    fitToSubtract->SetParameter( 0, fit->GetParameter(2) );
    fitToSubtract->SetParameter( 1, fit->GetParameter(3) );
    
    lBgEstimate      = fitToSubtract->Integral     ( lValPeakLo, lValPeakHi );
    lBgEstimate     /= lHisto->GetBinWidth(lBinPeakLo); //Transform into counts!
    lBgEstimateError = TMath::Sqrt(lBgEstimate); //fit->IntegralError( lValPeakLo, lValPeakHi );
  }
  
  if ( lOption.Contains("quadratic") ){
    //Step 2: Perform Quadratic Fit to improve results
    TString lNameQuad = lHisto->GetName();
    lNameQuad.Append("_QuadraticFit");
    fit = new TF1(lNameQuad, this, &strangenessModule::BgPol2,
                  lMean + lLoLeftBg*lSigma, lMean + lHiRightBg*lSigma, 5 , "strangenessModule", "BgPol2");
    
    //Start with parameters from initial fit: probably a good initial guess
    fit->FixParameter(0, lMean + lHiLeftBg*lSigma );
    fit->FixParameter(1, lMean + lLoRightBg*lSigma);
    fit->SetParameter(2, lBgConst );
    fit->SetParameter(3, lBgSlope );
    fit->SetParameter(4, 0.000 );
    
    //Perform fit - otherwise stick to initial (linear) guess
    TFitResultPtr fitResultPtr = lHisto->Fit( lNameQuad.Data(), lFitOptions.Data());
    if ( !fitResultPtr->IsValid() ) lReturnValue = kFALSE; //went bad
    
    TString lNameToSubtract = lHisto->GetName();
    lNameToSubtract.Append("_FitToSubtract");
    fitToSubtract = new TF1(lNameToSubtract.Data(), "[0]+[1]*x+[2]*x*x",
                            lMean + lLoLeftBg*lSigma, lMean + lHiRightBg*lSigma);
    fitToSubtract->SetParameter( 0, fit->GetParameter(2) );
    fitToSubtract->SetParameter( 1, fit->GetParameter(3) );
    fitToSubtract->SetParameter( 2, fit->GetParameter(4) );
    
    lBgEstimate      = fitToSubtract->Integral     ( lValPeakLo, lValPeakHi );
    lBgEstimate     /= lHisto->GetBinWidth(lBinPeakLo); //Transform into counts!
    lBgEstimateError = TMath::Sqrt(lBgEstimate); //fit->IntegralError( lValPeakLo, lValPeakHi );
  }
  
  if ( lOption.Contains("cubic") ){
    //Step 2: Perform Quadratic Fit to improve results
    TString lNameCubic = lHisto->GetName();
    lNameCubic.Append("_CubicFit");
    fit = new TF1(lNameCubic, this, &strangenessModule::BgPol3,
                  lMean + lLoLeftBg*lSigma, lMean + lHiRightBg*lSigma, 6 , "strangenessModule", "BgPol3");
    
    //Start with parameters from initial fit: probably a good initial guess
    fit->FixParameter(0, lMean + lHiLeftBg*lSigma );
    fit->FixParameter(1, lMean + lLoRightBg*lSigma);
    fit->SetParameter(2, lBgConst );
    fit->SetParameter(3, lBgSlope );
    fit->SetParameter(4, 0.000 );
    fit->SetParameter(5, 0.000 );
    
    //Perform fit - otherwise stick to initial (linear) guess
    TFitResultPtr fitResultPtr = lHisto->Fit( lNameCubic.Data(), lFitOptions.Data());
    if ( !fitResultPtr->IsValid() ) lReturnValue = kFALSE; //went bad
    
    TString lNameToSubtract = lHisto->GetName();
    lNameToSubtract.Append("_FitToSubtract");
    fitToSubtract = new TF1(lNameToSubtract.Data(), "[0]+[1]*x+[2]*x*x+[3]*x*x*x",
                            lMean + lLoLeftBg*lSigma, lMean + lHiRightBg*lSigma);
    fitToSubtract->SetParameter( 0, fit->GetParameter(2) );
    fitToSubtract->SetParameter( 1, fit->GetParameter(3) );
    fitToSubtract->SetParameter( 2, fit->GetParameter(4) );
    fitToSubtract->SetParameter( 3, fit->GetParameter(5) );
    
    lBgEstimate      = fitToSubtract->Integral     ( lValPeakLo, lValPeakHi );
    lBgEstimate     /= lHisto->GetBinWidth(lBinPeakLo); //Transform into counts!
    lBgEstimateError = TMath::Sqrt(lBgEstimate); //fit->IntegralError( lValPeakLo, lValPeakHi );
  }
  
  if ( lOption.Contains("bincounting") || lOption.Contains("MC") ){
    //Check if possible
    if((lLoLeftBg + lHiRightBg > 1e-6 ||
        lHiLeftBg + lLoRightBg > 1e-6 ||
        lLoPeak   + lHiPeak    > 1e-6 ) && !lOption.Contains("MC") ){
      printf("!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!");
      printf(" Cannot perform bin counting with asymmetric peak and bg regions!");
      printf("   In this case, please prefer the \'linear\' sig. ext. option");
      printf("                  Will not produce spectra");
      printf("!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!");
      lSignal = 0.0;
      lSignalErr = 0.0;
      return kFALSE;
    }
    
    //Sum up yields in corresponding bins
    for( Long_t ibin=lBinLeftBgLo; ibin<lBinLeftBgHi+1; ibin++)
      lBgEstimate += lHisto->GetBinContent(ibin);
    for( Long_t ibin=lBinRightBgLo; ibin<lBinRightBgHi+1; ibin++)
      lBgEstimate += lHisto->GetBinContent(ibin);
    
    //Error: sqrt(counts)
    //lBgEstimateError = TMath::Sqrt(lBgEstimate);
    
    //Error: Sum of errors
    lBgEstimateError = 0;
    for( Long_t ibin=lBinLeftBgLo; ibin<lBinLeftBgHi+1; ibin++)
      lBgEstimateError += lHisto->GetBinError(ibin)*lHisto->GetBinError(ibin);
    for( Long_t ibin=lBinRightBgLo; ibin<lBinRightBgHi+1; ibin++)
      lBgEstimateError += lHisto->GetBinError(ibin)*lHisto->GetBinError(ibin);
    lBgEstimateError = TMath::Sqrt(lBgEstimateError);
    
    //Scale according to number of bins
    Double_t lNBinsSummed = lBinLeftBgHi - lBinLeftBgLo + lBinRightBgHi - lBinRightBgLo + 2;
    Double_t lNBinsPeak   = lBinPeakHi - lBinPeakLo + 1;
    Double_t lScalingFactor = lNBinsPeak / lNBinsSummed;
    
    //Scale everything to match the current area of the peak
    lBgEstimate      = lBgEstimate      * lScalingFactor;
    lBgEstimateError = lBgEstimateError * lScalingFactor;
  }
  
  //Save a fit if there is one
  if ( fit           ) lControlList->Add(fit          );
  if ( fitToSubtract ) lControlList->Add(fitToSubtract);
  
  //Provide background information to the outside scope
  fHistBgVsPt -> SetBinContent(nBin, lBgEstimate);
  fHistBgVsPt -> SetBinError(nBin, lBgEstimateError);
  
  Double_t lPeakPlusBg      = 0;
  Double_t lPeakPlusBgError = 0;
  lPeakPlusBg = lHisto->IntegralAndError(lBinPeakLo,lBinPeakHi,lPeakPlusBgError);
  //lPeakPlusBgError = TMath::Sqrt(lPeakPlusBg);
  
  lSignal = lPeakPlusBg - lBgEstimate;
  lSignalErr = TMath::Sqrt( lPeakPlusBgError*lPeakPlusBgError + lBgEstimateError*lBgEstimateError );
  
  fHistRawVsPt -> SetBinContent(nBin, lSignal);
  fHistRawVsPt -> SetBinError(nBin, lSignalErr);
  
  return lReturnValue;
}

//________________________________________________________________
Double_t strangenessModule::BgPol1(const Double_t *x, const Double_t *par)
{
  //Function for background fitting, rejects peak region
  //Parameter [0] -> Hi LeftBg Boundary
  //Parameter [1] -> Lo RightBg Boundary
  if ( x[0] > par[0] && x[0] < par[1]) {
    TF1::RejectPoint();
    return 0;
  }
  return par[2] + par[3]*x[0];
}

//________________________________________________________________
Double_t strangenessModule::BgPol2(const Double_t *x, const Double_t *par)
{
  //Function for background fitting, rejects peak region
  //Parameter [0] -> Hi LeftBg Boundary
  //Parameter [1] -> Lo RightBg Boundary
  if ( x[0] > par[0] && x[0] < par[1]) {
    TF1::RejectPoint();
    return 0;
  }
  return par[2] + par[3]*x[0] + par[4]*x[0]*x[0];
}

//________________________________________________________________
Double_t strangenessModule::BgPol3(const Double_t *x, const Double_t *par)
{
  //Function for background fitting, rejects peak region
  //Parameter [0] -> Hi LeftBg Boundary
  //Parameter [1] -> Lo RightBg Boundary
  if ( x[0] > par[0] && x[0] < par[1]) {
    TF1::RejectPoint();
    return 0;
  }
  return par[2] + par[3]*x[0] + par[4]*x[0]*x[0] + par[5]*x[0]*x[0]*x[0];
}


//________________________________________________________________
void strangenessModule::DoAnalysis(TH3F *histogram, Double_t lLoMult, Double_t lHiMult, TString outputFilename, Double_t norm){
  cout<<"\e[1;31m+-~-+-~-+-~-+-~-+-~-+-~-+-~-+-~-+-~-+-~-+-~-+-~-+\e[0;00m"<<endl;
  cout<<"\e[1;31m  --- Strangeness Module execution starting ---\e[0;00m"<<endl;
  cout<<"\e[1;31m+-~-+-~-+-~-+-~-+-~-+-~-+-~-+-~-+-~-+-~-+-~-+-~-+\e[0;00m"<<endl;
  cout<<"Centrality: "<<lLoMult<<" - "<<lHiMult<<"%, output file: "<<outputFilename.Data()<<endl;
  cout<<"Mass guess: "<<massGuess<<", offset "<<massOffset<<endl;
  
  //Main analysis code
  if(!histogram){
    cout<<"\e[1;31mstrangenessModule\e[0;00m -> Please remember to give me data!"<<endl;
    return;
  }
  
  //Report time at the end
  TStopwatch* timer = new TStopwatch();
  timer->Start ( kTRUE );
  
  cout<<"\e[1;31mstrangenessModule\e[0;00m -> Checking multiplicity binning compatibility..."<<endl;
  if(!CheckCompatibleMultiplicity(histogram, lLoMult, lHiMult)){
    cout<<"\e[1;31mstrangenessModule\e[0;00m -> Multiplicity binning incompatible! Stopping."<<endl;
    return;
  }
  
  cout<<"\e[1;31mstrangenessModule\e[0;00m -> Checking momentum binning compatibility..."<<endl;
  if(!CheckCompatiblePt(histogram)){
    cout<<"\e[1;31mstrangenessModule\e[0;00m -> Momentum binning incompatible! Stopping."<<endl;
    return;
  }
  cout<<"\e[1;31mstrangenessModule\e[0;00m -> Binning matters are settled. Information available. Fasten seatbelts, please"<<endl;
  
  //"Die hard" fitting, please
  TVirtualFitter::SetMaxIterations( 50000 );
  
  // setup
  TList *lListHistograms = new TList();
  lListHistograms->SetName("massHistograms");
  lListHistograms->SetOwner(kTRUE);
  
  //_____________________________________________________________________________
  // Step zero: project histograms
  const int lNPtBinsConst = lNPtBins;
  TH1D *histoPtBin[lNPtBinsConst];
  
  for( Long_t ibin = 0; ibin<lNPtBins; ibin++){
    histoPtBin[ibin] = histogram->ProjectionZ( Form("massPtBin_%.1f_%.1f", lPtBins[ibin], lPtBins[ibin+1]),
                                              histogram->GetXaxis()->FindBin( lLoMult+1e-5 ),
                                              histogram->GetXaxis()->FindBin( lHiMult-1e-5 ),
                                              histogram->GetYaxis()->FindBin( lPtBins[ibin  ]+1e-5 ),
                                              histogram->GetYaxis()->FindBin( lPtBins[ibin+1]-1e-5 )
                                              );
    //lHistoLSData[ibin]->SetDirectory(0);
    lListHistograms->Add(histoPtBin[ibin]);
  }
  
  //_____________________________________________________________________________
  // First step: attempt a mass fit, please
  
  TList *lListPeakHistograms = new TList();
  lListPeakHistograms->SetName("peakHistograms");
  lListPeakHistograms->SetOwner(kTRUE);
  
  TH1D* fHistMeanVsPt  = new TH1D("fHistMeanVsPt", "",lNPtBins,lPtBins);
  TH1D* fHistSigmaVsPt = new TH1D("fHistSigmaVsPt","",lNPtBins,lPtBins);
  
  for(Long_t ibin = 0; ibin<lNPtBins; ibin++){
    if(!lWorkingBins[ibin]) continue;
    PerformInitialFit( histoPtBin[ibin], ibin+1, fHistMeanVsPt, fHistSigmaVsPt, lListPeakHistograms, lSigExtMethod.Data() );
  }
  lListPeakHistograms->Add(fHistMeanVsPt);
  lListPeakHistograms->Add(fHistSigmaVsPt);
  
  //_____________________________________________________________________________
  // Second step: do what you must
  TList *lListResultHistograms = new TList();
  lListResultHistograms->SetName("resultHistograms");
  lListResultHistograms->SetOwner(kTRUE);
  
  TH1D* fHistRawVsPt  = new TH1D("fHistRawVsPt", "",lNPtBins,lPtBins);
  TH1D* fHistBgVsPt  = new TH1D("fHistBgVsPt", "",lNPtBins,lPtBins);
  TH1D* fNorm = new TH1D("fNorm","", 1, 0, 1);
  
  for(Long_t ibin = 0; ibin<lNPtBins; ibin++){
    if(!lWorkingBins[ibin]) continue;
    PerformSignalExtraction( histoPtBin[ibin], ibin+1, fHistRawVsPt, fHistBgVsPt, fHistMeanVsPt, fHistSigmaVsPt, lListResultHistograms, lSigExtMethod.Data());
  }
  
  if( lVerbose){
    cout<<"---] Signal Extraction summary [----------------------------"<<endl;
    for(Long_t ibin = 0; ibin<lNPtBins; ibin++){
      if( lVerbose ) cout<<"Bin #"<<ibin<<Form("\t%.1f-%.1f",lPtBins[ibin],lPtBins[ibin+1])<<" Signal: "<<fHistRawVsPt->GetBinContent(ibin+1)<<" +/- "<<fHistRawVsPt->GetBinError(ibin+1) <<" via technique: "<<lSigExtMethod.Data()<<endl;
    }
    cout<<"---] End Signal Extraction summary [------------------------"<<endl;
  }
  
  // renormalize
  fHistRawVsPt->Scale(1./norm, "width");
  fHistBgVsPt->Scale(1./norm, "width");
  fNorm->SetBinContent(1, norm);
  
  lListResultHistograms->Add(fHistRawVsPt);
  lListResultHistograms->Add(fHistBgVsPt);
  lListResultHistograms->Add(fNorm);
  
  
  //_____________________________________________________________________________
  // Save!
  TFile *fileOut = new TFile(outputFilename.Data(), "RECREATE");
  fileOut->cd();
  //Save all objects owned by the TLists
  lListHistograms        ->Write("massHistograms",         TObject::kSingleKey);
  lListPeakHistograms    ->Write("peakHistograms",         TObject::kSingleKey);
  lListResultHistograms  ->Write("resultHistograms",       TObject::kSingleKey);
  fileOut->Write();
  fileOut->Close();
  
}
