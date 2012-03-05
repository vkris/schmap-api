import unittest
import test_api_client
import test_api_exception

suite_exception = test_api_exception.suite()
suite_client = test_api_client.suite()

suite = unittest.TestSuite()
suite.addTest(suite_exception)
suite.addTest(suite_client)
unittest.TextTestRunner().run(suite)
