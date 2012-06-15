import unittest
import sys,os,re
import urllib
import mock
from mock_urllib import MockURLlib
try:
    import json
except ImportError, e:
    import simplejson as json

sys.path.append("..")
from schmap_api.exception import SchmapAPIException
from schmap_api.client_api import SchmapAPIClient
import schmap_api


class TestClient(unittest.TestCase):
    def setUp(self):
        logger = schmap_api.getLog()
        logger.setLevel("CRITICAL")
        self.client = SchmapAPIClient("test","pass","clientid",logger)
        self.client.set_frequency(5)

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
        mock_analyze.retrun_value = 0
        ret = self.client.analyze_account(["user1","user2","user3"])
        self.assertEqual(3,mock_analyze.call_count)
        self.assertEqual(0,ret)

    @mock.patch.object(SchmapAPIClient, 'analyze')
    def test_analyze_list(self, mock_analyze):
        mock_analyze.retrun_value = 0
        analysis_type = "full_analysis"
        ret = self.client.analyze_list(["user1","user2","user3"],"some_name", analysis_type)
        self.assertEqual(1,mock_analyze.call_count)
        self.assertEqual(0,ret)

    @mock.patch.object(SchmapAPIClient, 'save_to_file')
    @mock.patch.object(SchmapAPIClient, 'request_uri')
    @mock.patch.object(SchmapAPIClient, 'get_response')
    def test_analyze(self, mock_get_response, mock_request_uri, mock_save_to_file):
        # Test 1
        mock_request_uri.return_value = '{}'
        mock_get_response.retrun_value = {"request_id":100}
        self.client.analyze("http://sample.com",{"list_name":"GSList", "analysis":"profiled_dataset"})
        self.assertEqual(1, mock_get_response.call_count)
        self.assertTrue(mock_request_uri.called)
        self.assertTrue(mock_save_to_file.called)
        self.assertTrue(self.client.request_queue.get().endswith("##GSList"))


    @mock.patch.object(SchmapAPIClient, 'request_uri')
    @mock.patch.object(schmap_api, 'getLog')
    def test_check_status(self, mock_log, mock_request):
        # If you make percent_value other than 100, it will get into an infinite loop
        mock_request.return_value = '{"code" : 0,"message" : "processed_succesfully", "percent_complete":100.00}'
        mock_log.return_value =""
        self.assertEqual(self.client.check_status(100) ,0)
        self.assertRaises(SchmapAPIException, self.client.check_status,-1)

    @mock.patch('threading.Thread')
    def test_get_data(self, mock_thread):
        # Make sure you are running only a fixed size of thread pool
        ret = self.client.get_data()
        self.assertEqual(self.client.no_of_threads, mock_thread.call_count)
        self.assertEqual(0,ret)

    @mock.patch('__builtin__.open')
    def test_save_to_file(self, mock_file):
        self.client.save_to_file("data","test.json")
        mock_file.assert_called_with(self.client.out_dir+"/test.json", "a")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestClient))
    return suite

if __name__ == "__main__":
    unittest.main()
