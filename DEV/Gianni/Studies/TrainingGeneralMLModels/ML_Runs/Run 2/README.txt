Description: ML test run for AntiLambdas in MC PbPb
 
------------------------------------------------------- 
 
Run configurations: 
 
{
  "Dataset": {
    "DatasetName": "AntiLambda",
    "Class": "fIsAntiLambda",
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
    "max_depth": 6,
    "learning_rate": 0.6850957436050974,
    "n_estimators": 350,
    "min_child_weight": 2,
    "gamma": 0.0005985836362477447,
    "subsample": 0.2151191572281935,
    "colsample_bytree": 0.2546548474351868,
    "reg_alpha": 0.004629121313882806,
    "reg_lambda": 3.1006638283952975e-07
  }
}