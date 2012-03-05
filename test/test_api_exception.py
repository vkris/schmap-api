import unittest
import sys,os,re

sys.path.append("..")
from schmap_api.exception import SchmapAPIException
import mock

class TestError(unittest.TestCase):
    def test_message(self):
        try:
            raise SchmapAPIException(-1) 
        except SchmapAPIException,e:
            self.assertEqual(str(e),"-1 (Unknown error.)")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestError))
    return suite

if __name__ == "__main__":
    unittest.main()
