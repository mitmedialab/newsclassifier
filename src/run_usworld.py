from usworld_results import *

#import pdb;pdb.set_trace()
usworld = USWorldResults("test/fixtures/mock_training/", ["love", "snow"])
usworld.setup_evaluation("test/fixtures/mock_evaluation/")

#verify that the proper number of rows are imported

usworld.classifier.classify(usworld.extract_features(["love", "falling", "snow"]))
usworld.classifier.classify(usworld.extract_features(["love", "falling", "snow", "dark"]))
