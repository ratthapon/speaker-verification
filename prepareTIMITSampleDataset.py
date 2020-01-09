# make TIMIT-sample dataset
from glob import glob
from pathlib import Path
import argparse

from pandas import DataFrame

EXCLUDE_FILES = ["sa1.wav", "sa2.wav"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Prepare dataset by spliting TIMIT-Sample dataset for training and testing.")
    parser.add_argument("--indir", metavar = 'indir', type = str, 
                        help = "input directory")
    parser.add_argument("--outdir", metavar = 'outdir', type = str, 
                        help = "output directory")
    args = parser.parse_args()
    
    trainIDList = []
    trainFileList = []
    testIDlist = []
    testFileList = []

    speakerDirectories = glob("/home/ratthapon/TIMIT/timit/train/*/")

    for speakerDirectory in speakerDirectories:
        speakerID = Path(speakerDirectory).name
        print("Speaker:", speakerID)
        
        wavFiles = glob(speakerDirectory + "/*.wav")
        nWavFile = len(wavFiles)
        
        fileIndex = 0
        for wavFile in wavFiles:
            if Path(wavFile).name in EXCLUDE_FILES:
                # skip this files
                continue
                
            if fileIndex < (nWavFile-2)/2:
                trainIDList += [speakerID]
                trainFileList += [wavFile]
                print("    Train:", Path(wavFile).name)
                
            if fileIndex >= (nWavFile-2)/2:
                testIDlist += [speakerID]
                testFileList += [wavFile]
                print("    Test:", Path(wavFile).name)
                
            fileIndex += 1
            
    trainingSet = DataFrame({
        "speaker": trainIDList,
        "filename": trainFileList
    }) 
    testingSet = DataFrame({
        "speaker": testIDlist,
        "filename": testFileList
    })
    
    import os
    
    print(os.getcwd())

    print("Exporting enroll list to CSV:", "cfg/enroll_list_timit.csv")
    trainingSet.to_csv(args.outdir + "/cfg/enroll_list_timit.csv", columns = ["filename", "speaker"], index = False)

    print("Exporting test list to CSV:", "cfg/test_list_timit.csv")
    testingSet.to_csv(args.outdir + "/cfg/test_list_timit.csv", columns = ["filename", "speaker"], index = False)
        