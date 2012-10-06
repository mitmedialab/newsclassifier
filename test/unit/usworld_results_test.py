import unittest
import test_common 
import os
from usworld_results import *

class USWorldResultsTest(unittest.TestCase):

  def testUSWorldResults(self):
    #import pdb;pdb.set_trace()
    usworld = USWorldResults("test/fixtures/mock_training/", ["love", "snow"])
    usworld.setup_evaluation("test/fixtures/mock_evaluation/")
 
    #verify that the proper number of rows are imported
    self.assertEqual(2, len(usworld.categories["love"]["documents"]))
    self.assertEqual(2, len(usworld.categories["snow"]["documents"]))

    self.assertEqual("love", usworld.classifier.classify(usworld.extract_features(["love"])))
    self.assertEqual("snow", usworld.classifier.classify(usworld.extract_features(["snow"])))

    self.assertEqual("love", usworld.classifier.classify(usworld.extract_features(["love", "falling", "snow"])))
    self.assertEqual("snow", usworld.classifier.classify(usworld.extract_features(["love", "falling", "snow", "dark"])))

  def testCreateTrainingTestDatasets(self):
    categories = ["local", "sports"]
    source_folder = "test/fixtures/evaluation/"
    dest_folder = "test/tmp/"

    USWorldResults.create_training_test_datasets(source_folder, dest_folder, categories)

    self.assertEqual(22, self.file_len(dest_folder + "training/local.csv"))
    self.assertEqual(9, self.file_len(dest_folder + "evaluation/local.csv"))
    self.assertEqual(13, self.file_len(dest_folder + "training/sports.csv"))
    self.assertEqual(6, self.file_len(dest_folder + "evaluation/sports.csv"))

    for f in categories:
      os.remove("test/tmp/training/" + f + ".csv")
      os.remove("test/tmp/evaluation/" + f + ".csv")

  def file_len(self, fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

test_common.ALL_TESTS.append(USWorldResultsTest)

if __name__ == '__main__':
  unittest.main()
