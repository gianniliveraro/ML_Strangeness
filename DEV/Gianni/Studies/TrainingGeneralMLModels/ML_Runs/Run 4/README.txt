Description: ML test run for AntiLambdas in MC PbPb - now, with the right dataset!
 
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
    "max_depth": 9,
    "learning_rate": 0.054813490973257585,
    "n_estimators": 361,
    "min_child_weight": 2,
    "gamma": 7.271743943811113e-05,
    "subsample": 0.13708887771123476,
    "colsample_bytree": 0.9701187315839469,
    "reg_alpha": 1.2825712240904708e-05,
    "reg_lambda": 5.917750409766319e-07
  }
}