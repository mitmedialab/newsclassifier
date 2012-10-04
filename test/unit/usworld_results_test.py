import unittest
import test_common 
from usworld_results import *

class USWorldResultsTest(unittest.TestCase):

  def preprocess_article_assertions(self, key, category):
    for value in [ (key in row) for row in category]:
      self.assertTrue(value)
    

  def testLoadCSVFiles(self):
    #import pdb;pdb.set_trace()
   results = USWorldResults("test/fixtures/")
   categories = [results.sports, results.local]

   [self.assertEqual(19, len(category)) for category in categories]

   [self.preprocess_article_assertions("content_tokens", category) 
     for category in categories]

   [self.preprocess_article_assertions("headline_tokens", category) 
     for category in categories]


   import pdb; pdb.set_trace()
    

test_common.ALL_TESTS.append(USWorldResultsTest)

if __name__ == '__main__':
  unittest.main()
