# Enroll speaker 
import argparse
import ast
from pathlib import Path

import numpy
import pandas 
from pandas import DataFrame
from scipy.spatial.distance import cdist, euclidean, cosine

from model import vggvox_model
from scoring import build_buckets, get_embeddings_from_list_file
import constants as c

if __name__ == "__main__":
    #%% setup argument parser for CLI usage
    parser = argparse.ArgumentParser(description = "Extract speech feature from given dataset.")
    parser.add_argument("--enroll-feature-set", dest = "enrollFeatureSet", 
                        metavar = "ENROLL_FEATURESET", type = str, 
                        help = "a featureset for enrollment in .csv format.")
    parser.add_argument("--test-feature-set", dest = "testFeatureSet", 
                        metavar = "TEST_FEATURESET", type = str, 
                        help = "a featureset for testing in .csv format.")
    parser.add_argument("--result-path", dest = "resultPath", 
                        metavar = "RESULT_PATH", type = str, 
                        help = "an output path for identification result.")
    args = parser.parse_args()

    print("Loading featureset")
    enrollFeatureSet = pandas.read_pickle(args.enrollFeatureSet)
    enrollFeatures = numpy.array([emb for emb in enrollFeatureSet["embedding"]])
    # enrollFeatures = enrollFeatureSet["embedding"]
    speakers = enrollFeatureSet["speaker"]

    testFeatureSet = pandas.read_pickle(args.testFeatureSet)
    testFeatures = numpy.array([emb for emb in testFeatureSet["embedding"]])
    # testFeatures = testFeatureSet["embedding"]

    print("Computing pairwise distance")
    distances = DataFrame(cdist(enrollFeatures, testFeatures, metric=c.COST_METRIC), columns=speakers)

    print("Predict speaker from computed distances")
    results = pandas.read_pickle(args.testFeatureSet)
    results.drop(columns = ["embedding"], inplace = True)

    results = pandas.concat([results, distances],axis=1)
    results["predict"] = results[speakers].idxmin(axis=1)
    results["correct"] = (results["predict"] == results["speaker"])*1. # bool to int

    print("Exporting feature set to CSV:", args.resultPath)
    Path(args.resultPath).parents[0].mkdir(parents = True, exist_ok = True)
    results.to_csv(args.resultPath, index = False)

        