Description: ML test run for Lambdas in MC PbPb - now, with the right dataset!
 
------------------------------------------------------- 
 
Run configurations: 
 
{
  "Dataset": {
    "DatasetName": "Lambda",
    "Class": "fIsLambda",
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
    "max_depth": 7,
    "learning_rate": 0.0968269862141397,
    "n_estimators": 412,
    "min_child_weight": 6,
    "gamma": 0.11493495198934917,
    "subsample": 0.5195676721522766,
    "colsample_bytree": 0.9537819590934331,
    "reg_alpha": 1.7343351487479738e-06,
    "reg_lambda": 0.14884776325771465
  }
}