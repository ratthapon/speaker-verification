# Enroll speaker 
import argparse
from pathlib import Path

from model import vggvox_model
from scoring import build_buckets, get_embeddings_from_list_file
import constants as c

if __name__ == "__main__":
    #%% setup argument parser for CLI usage
    parser = argparse.ArgumentParser(description = "Extract speech feature from given dataset.")
    parser.add_argument("--dataset", dest = "dataset", 
                        metavar = 'DATASET', type = str, 
                        help = "an input dataest in .csv format.")
    parser.add_argument("--feature-set", dest = "featureSet", 
                        metavar = 'FEATURE_SET', type = str, 
                        help = "an output contains speech feature vectors in .csv format.")
    parser.add_argument("--model", dest = "model", 
                        metavar = 'MODEL', type = str, 
                        help = "a deep model for feature extraction.")
    args = parser.parse_args()

    print("Loading model")
    model = vggvox_model()
    model.load_weights(args.model)
    
    print("Extracting features")
    featuresSet = get_embeddings_from_list_file(model, args.dataset, c.MAX_SEC)
    print(featuresSet.dtypes)

    print("Exporting feature set to CSV:", args.featureSet)
    Path(args.featureSet).parents[0].mkdir(parents = True, exist_ok = True)
    featuresSet.to_pickle(args.featureSet)

        