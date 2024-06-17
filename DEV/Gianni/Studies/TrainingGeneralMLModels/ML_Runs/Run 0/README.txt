Description: ML test run for Gammas in MC PbPb
 
------------------------------------------------------- 
 
Run configurations: 
 
{
  "Dataset": {
    "DatasetName": "Gamma",
    "Class": "fIsGamma",
    "Features": [
      "fV0radius",
      "fPA",
      "fDCApostopv",
      "fDCAnegtopv",
      "fDCAV0daughters",
      "fDCAv0topv"
    ]
  },
  "BDT": {
    "max_depth": 9,
    "learning_rate": 0.019627415489918115,
    "n_estimators": 409,
    "min_child_weight": 10,
    "gamma": 5.376118823645962e-08,
    "subsample": 0.398831772511779,
    "colsample_bytree": 0.7926080830987957,
    "reg_alpha": 0.005825725757185355,
    "reg_lambda": 0.41367307253069946
  }
}