//+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
//
// General class to do weak decay analysis
//
// Please send any questions, etc to:
//    david.dobrigkeit.chinellato@cern.ch
//
//+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#ifndef strangenessModule_H
#define strangenessModule_H
#include <TNamed.h>
#include <TList.h>
#include <TH3F.h>

using namespace std;

class strangenessModule : public TNamed {
    
public:
    //Simple constructor
    strangenessModule();
    
    //TNamed-inspired constructor with title
    strangenessModule(const char * name, const char * title = "Result");
    
    //Simple destructor
    ~strangenessModule();
    
    void Clear(Option_t* = "") {};

    //Configuration
    void SetPtBinning   ( Long_t lRecNPtBins, Double_t *lRecPtBins );
    void SetWorkingBins ( Long_t lRecNPtBins, Bool_t *lWorkBins );

    void SetVerbose     ( Bool_t lVerb = kTRUE ) { lVerbose = lVerb; }
    void SetDoOnlyData  ( Bool_t lDoOnlyDataRec = kTRUE ) { lDoOnlyData = lDoOnlyDataRec; }
    void SetMassGuess   ( Double_t lMassGuess ) { massGuess = lMassGuess; }
    void SetMassOffset  ( Double_t lMassOffset ) { massOffset = lMassOffset; }

    // set signal extraction method
    void SetSignalExtractionMethod ( TString method ) { lSigExtMethod = method.Data(); }

    // in number of sigmas
    void SetSigExtRanges (Double_t lRLoLeftBg, Double_t lRHiLeftBg,  Double_t lRLoPeak,
                          Double_t lRHiPeak,   Double_t lRLoRightBg, Double_t lRHiRightBg);
    
    //Do analysis based on a specific configuration
    //Return corrected result right away
    void DoAnalysis(TH3F *histogram, Double_t lLoMult, Double_t lHiMult, TString outputFilename, Double_t norm);

    
    
    //Helper functions
    Bool_t CheckCompatibleMultiplicity(TH3F *histogram, Double_t lLoMult, Double_t lHiMult); // useful to check if histogram is able to provide requested centrality binning
    Bool_t CheckCompatiblePt          (TH3F *histogram); // useful to check if histogram is able to provide requested pT binning
    Bool_t PerformInitialFit( TH1D *lHisto, Int_t nBin, TH1D *fHistMeanVsPt, TH1D *fHistSigmaVsPt, TList *outputList, TString lOption = "linear" );
    Bool_t PerformSignalExtraction( TH1D *lHisto, Int_t nBin, TH1D *fHistRawVsPt, TH1D *fHistBgVsPt, TH1D *fHistMeanVsPt, TH1D *fHistSigmaVsPt, TList *lControlList, TString lOption = "linear");
    // TString GetGoodFitOption( TH1D *lHisto, Int_t ilow, Int_t ihigh );
    Double_t BgPol1(const Double_t *x, const Double_t *par);
    Double_t BgPol2(const Double_t *x, const Double_t *par);
    Double_t BgPol3(const Double_t *x, const Double_t *par);
    
private:
    //Multiplicity / Centrality boundaries to use if requested to do so
    Bool_t lUseIntegratedMultForFirstFit;
    Double_t lLoMultIntegrated;
    Double_t lHiMultIntegrated;
  
    //Number of sigmas to do background/peak sampling
    Double_t lLoLeftBg;
    Double_t lHiLeftBg;
    Double_t lLoPeak;
    Double_t lHiPeak;
    Double_t lLoRightBg;
    Double_t lHiRightBg;

    //Pt Bins to use
    Long_t lNPtBins;
    Double_t lPtBins[100];
    Bool_t lWorkingBins[100];
    
    //Verbosity boolean
    Bool_t lVerbose;
    
    //Other control booleans
    Bool_t lDoOnlyData; //process only the data part and break without using MC 

    // Initial fit parameters 
    Double_t massGuess; // estimate of peak value
    Double_t massOffset; // safe offset outside of peak region 

    // signal extraction (universal) 
    TString lSigExtMethod; // standard: linear
    
    ClassDef(strangenessModule, 0)
};
#endif
