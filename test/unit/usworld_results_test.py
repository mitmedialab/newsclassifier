import unittest
import test_common 
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
    

test_common.ALL_TESTS.append(USWorldResultsTest)

if __name__ == '__main__':
  unittest.main()
