# make TIMIT-sample dataset
from glob import glob
from pathlib import Path
import argparse

from pandas import DataFrame

EXCLUDE_FILES = ["sa1.wav", "sa2.wav"]

if __name__ == "__main__":
    #%% setup argument parser for CLI usage
    parser = argparse.ArgumentParser(description = "Prepare dataset by spliting TIMIT-Sample dataset for training and testing.")
    parser.add_argument("--training-set", dest = "trainingSet", 
                        metavar = 'TRAINING_SET', type = str, 
                        help = "an output contains meta data for training set in .csv format")
    parser.add_argument("--testing-set", dest = "testingSet", 
                        metavar = 'TESTING_SET', type = str, 
                        help = "an output contains meta data for testing set in .csv format")
    parser.add_argument("--wav-dir", dest = "wavDir", 
                        metavar = 'SPEAKER_DIRECTORY', type = str, 
                        help = "a directory contains speaker directories which each of them contains audio files in .wav format")
    parser.add_argument("--ratio", dest = "ratio", 
                        metavar = 'RATIO', type = float, default = 0.5,
                        help = "a train/test split ratio")
    args = parser.parse_args()
    
    # Initialize dataset
    trainIDList = []
    trainFileList = []
    testIDlist = []
    testFileList = []

    speakerDirectories = glob(args.wavDir + "/*/")

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

    print("Exporting enroll list to CSV:", args.trainingSet)
    trainingSet.to_csv(args.trainingSet, columns = ["filename", "speaker"], index = False)

    print("Exporting test list to CSV:", args.testingSet)
    testingSet.to_csv(args.testingSet, columns = ["filename", "speaker"], index = False)
        