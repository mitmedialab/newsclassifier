import unittest
import test_common 
from usworld_results import *

class USWorldResultsTest(unittest.TestCase):

  def testLoadCSVFiles(self):
    #import pdb;pdb.set_trace()
    USWorldResults("test/fixtures/")
    

test_common.ALL_TESTS.append(USWorldResultsTest)

if __name__ == '__main__':
  unittest.main()
