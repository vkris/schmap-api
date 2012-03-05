import unittest
import sys,os,re
import urllib
import mock
from mock_urllib import MockURLlib
import json

sys.path.append("..")
from schmap_api.exception import SchmapAPIException
from schmap_api.client import SchmapAPIClient
import schmap_api


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = SchmapAPIClient("test","pass")
        self.client.set_frequency(5)
        #self.file_reader_for_uri= open("/tmp/junk.out")

    def test_frequency(self):
        self.assertEqual(self.client.frequency,5)

    def test_base_uri(self):
        self.assertEqual(self.client.base_uri, "https://www.schmap.it/api/social_analysis/")

    def test_request_uri(self):
        url ="http://google.com/"
        response = self.client.request_uri(url)
        match = response.startswith("<!doctype html>")
        self.assertTrue(match)

    @mock.patch('urllib2.urlopen')
    def test_mock_uri(self, mock_uri_request):
        url ="google.com"
        mock_uri_request.return_value = MockURLlib(url)
        response = self.client.request_uri(url)
        self.assertTrue(response.startswith("<!doctype html>"))

    def test_get_response(self):
        response = ""
        self.assertRaises(SchmapAPIException,self.client.get_response,response)
        response = '{"code":0, "message": "processed_succesfully"}'
        reply_response = self.client.get_response(response)
        self.assertTrue(reply_response, response)
        response = "<!DOCTYPE HTML"
        self.assertRaises(SchmapAPIException, self.client.get_response,response)
        response = "{}"
        self.assertRaises(SchmapAPIException, self.client.get_response, response)

    @mock.patch.object(SchmapAPIClient, 'analyze')
    def test_analyze_account(self, mock_analyze):
        self.client.analyze_account(["user1","user2","user3"])
        self.assertEqual(3,mock_analyze.call_count)

    @mock.patch.object(SchmapAPIClient, 'analyze')
    def test_analyze_list(self, mock_analyze):
        self.client.analyze_list(["user1","user2","user3"],"some_name")
        self.assertEqual(1,mock_analyze.call_count)

    @mock.patch.object(SchmapAPIClient, 'request_uri')
    def test_check_status(self, mock_request):
        # If you make percent_value other than 100, it will get into an infinite loop
        mock_request.return_value = '{"code" : 0,"message" : "processed_succesfully", "percent_complete":100.00}'
        self.assertEqual(self.client.check_status(100) ,0)
        self.assertRaises(SchmapAPIException, self.client.check_status,-1)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestClient))
    return suite

if __name__ == "__main__":
    unittest.main()
