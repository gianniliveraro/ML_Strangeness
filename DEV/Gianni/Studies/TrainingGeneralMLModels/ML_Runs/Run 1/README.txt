Description: ML test run for Lambdas in MC PbPb
 
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
    "max_depth": 9,
    "learning_rate": 0.08227968742947257,
    "n_estimators": 390,
    "min_child_weight": 8,
    "gamma": 0.19033682394962478,
    "subsample": 0.09125676673835433,
    "colsample_bytree": 0.690962274710252,
    "reg_alpha": 0.00013221342694672662,
    "reg_lambda": 4.412597327261236e-05
  }
}