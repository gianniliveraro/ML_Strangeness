import ROOT

oldstatus = ROOT.TH1.AddDirectoryStatus()
ROOT.TH1.AddDirectory(False)

ccdb_path_production = "Users/g/gsetouel/MLModels2"
ccdb_url_production = "https://alice-ccdb.cern.ch"

ccdb_path = ccdb_path_production
ccdb_url = ccdb_url_production

ccdb = ROOT.o2.ccdb.CcdbApi()
ccdb.init(ccdb_url)

def uploadONNXToCCDB(description, onnx_file_path, start, stop):
    metadata = ROOT.std.map(ROOT.std.string, ROOT.std.string)()

    metadata.clear()
    metadata.insert(ROOT.std.pair(ROOT.std.string, ROOT.std.string)("Description", "%s" % description))
    metadata.insert(ROOT.std.pair(ROOT.std.string, ROOT.std.string)("Author", "Gianni Shigeru Setoue Liveraro"))

    # Read ONNX file as binary
    with open(onnx_file_path, 'rb') as file:
        onnx_data = file.read()

    # Store ONNX data as TNamed in CCDB
    #onnx_content = ROOT.TNamed("BDTModel", onnx_data)

    # Store ONNX content as TNamed in CCDB
    #ccdb.storeAsTFileAny(onnx_content, ccdb_path, metadata, start, stop)
    ccdb.storeAsBinaryFile(onnx_data, len(onnx_data), onnx_file_path, "ONNX Model | file read as binary string", ccdb_path, metadata, start, stop)
    

# Usage
sor = 1695750422702
eor = 1698617337860

onnx_file_name = "Gamma_BDTModel"
onnx_file_path = onnx_file_name+".onnx"
description = onnx_file_name+"first test!"
uploadONNXToCCDB(description, onnx_file_path, int(int(sor) / 1000 - 2) * 1000, int(int(eor) / 1000 + 10) * 1000)


