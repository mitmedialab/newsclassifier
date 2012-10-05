import unittest
import test_common 
from usworld_results import *

class USWorldResultsTest(unittest.TestCase):

  def preprocess_article_assertions(self, key, category):
    for value in [ (key in row) for row in category]:
      self.assertTrue(value)
    

  def testLoadCSVFiles(self):
    #import pdb;pdb.set_trace()
    results = USWorldResults("test/fixtures/training/")
    results.setup_evaluation("test/fixtures/evaluation/")
 
    #verify that the proper number of rows are imported
    self.assertEqual(26, len(results.categories["sports"]["documents"]))
    self.assertEqual(73, len(results.categories["local"]["documents"]))
 
    #test that the headline and content of every row is imported
    [self.preprocess_article_assertions(field, results.categories[category]["documents"]) 
      for category in results.categories for field in results.frequencies]
    import pdb; pdb.set_trace()
    #results.classifier.classify(results.extract_content_features(results.eval_categories["sports"]["documents"][10]["content"]))
    

test_common.ALL_TESTS.append(USWorldResultsTest)

if __name__ == '__main__':
  unittest.main()
