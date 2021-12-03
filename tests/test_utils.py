import pytest
import requests

from unittest.mock import Mock

from requests.exceptions import HTTPError
from src.utils.fibonacci import get_fibonacci
from src.utils.request import Request

mock = Mock()

test_cases = [ 
    { 'index': 2, 'expect': 1 }, 
    { 'index': 21, 'expect': 10946 }, 
    { 'index': 25, 'expect': 75025 }, 
    { 'index': -2, 'expect': 0 }, 
    { 'index': 20, 'expect': 6765 }, 
    { 'index': 400, 'expect': 176023680645013966468226945392411250770384383304492191886725992896575345044216019675 }, 
]

@pytest.fixture
def mock_request_get(monkeypatch):
    def mock_get(*args, **kwargs):
        mock.raise_for_status = Mock(return_value=True)
        mock.json = Mock(return_value={ 'data': 'some response' })

        return mock

    monkeypatch.setattr(requests, "get", mock_get)

@pytest.fixture
def mock_request_get_error(monkeypatch):
    def mock_get(*args, **kwargs):
        mock.raise_for_status = Mock(side_effect=HTTPError('403 http errror'))

        return mock

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_fibonacci():
    for case in test_cases:
        index, expect = case.values()
        
        assert get_fibonacci(index) == expect

def test_requests_wrapper_constructor():
    req_mock = Request('url://test')

    assert req_mock.__getattribute__('url') == 'url://test'
    assert req_mock.__getattribute__('headers') == {'content-type': 'application/json'}

def test_requests_wrapper_custom_headers():
    mock_headers = { 'x-api-key': '1sometoken1', 'content-type': 'text/html' }
    req_mock = Request('url://test', mock_headers)

    assert req_mock.__getattribute__('headers') == mock_headers

def test_requests_get_method(mock_request_get):
    req_mock = Request('url://test')

    assert req_mock.get('/test') == { 'data': 'some response' }

def test_requests_http_errors(mock_request_get_error):
    req_mock = Request('http://test.com')

    res = req_mock.get('/test')
    assert '403 http errror' in str(res)

# TODO unit tests for post method
