import atexit
import unittest
from unittest.mock import patch

from pact import Consumer, Provider

from .functions import request_app1, request_app2, request_two_apps

app1_pact = Consumer('Translator').has_pact_with(Provider('app1'), pact_dir='./pact')
app1_pact.start_service()
atexit.register(app1_pact.stop_service)

app2_pact = Consumer('Translator').has_pact_with(Provider('app2'), pact_dir='./pact')


class TranslateServiceContract(unittest.TestCase):

    mock_host = "http://localhost:1234"

    def test_app1_right(self):

        path = '/app1/api/'
        expected_body = {"en": "one", "de": "eins"}
        expected_status = 200

        (app1_pact
         .given('request app1 right')
         .upon_receiving('a request to app1 right')
         .with_request('get', path)
         .will_respond_with(expected_status, body=expected_body))

        with app1_pact:
            resp = request_app1(self.mock_host)

        self.assertEqual(resp, 'app1 right')

    def test_app1_wrong(self):
        path = '/app1/api/'
        expected_status = 404

        (app1_pact
         .given('request app1 wrong')
         .upon_receiving('a request to app1 wrong')
         .with_request('get', path)
         .will_respond_with(expected_status))

        with app1_pact:
            resp = request_app1(self.mock_host)

        self.assertEqual(resp, 'app1 wrong')

    def test_app2(self):

        path = '/app2/api/'
        expected_body = {"en": "one", "de": "eins"}
        expected_status = 200

        (app2_pact
         .given('request app2')
         .upon_receiving('a request to app2')
         .with_request('get', path)
         .will_respond_with(expected_status, body=expected_body))

        with app2_pact:
            resp = request_app2(self.mock_host)

        self.assertEqual(resp, 'app2')

    @patch('contract_tests.functions.request_app1')
    @patch('contract_tests.functions.request_app2')
    def test_two_apps(self, mock_request_app2, mock_request_app1):
        mock_request_app2.return_value = 'app2'
        mock_request_app1.return_value = 'app1'
        resp = request_two_apps(self.mock_host, self.mock_host)

        self.assertEqual(resp, 'app1app2')
