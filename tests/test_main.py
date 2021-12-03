import pytest
import json

from src.utils.request import Request
from requests.exceptions import HTTPError
from src.main import lambda_handler

mockPokemon = { "name": "ivysaur", "abilities": [{"ability": {"name": "overgrow" }}]}
scenarios = {
    'success': [{
        'name': '1. should return fibonacci index 2 and pokemon id 1',
        'payload': { 'pathParameters': { 'id': '2'  }},
        'expect': 1
    },
    {
        'name': '2. should return fibonacci index 20 and pokemon id 20',
        'payload': { 'pathParameters': { 'id': '20'  }},
        'expect': 6765
    },
    {
        'name': '3. should return fibonacci index 2000 and pokemon id 2000',
        'payload': { 'pathParameters': { 'id': '2000'  }},
        'expect': 4224696333392304878706725602341482782579852840250681098010280137314308584370130707224123599639141511088446087538909603607640194711643596029271983312598737326253555802606991585915229492453904998722256795316982874482472992263901833716778060607011615497886719879858311468870876264597369086722884023654422295243347964480139515349562972087652656069529806499841977448720155612802665404554171717881930324025204312082516817125
    }],
    'invalid_payload': [{
        'name': '4. if payload is - { \'some\': "abc" }',
        'payload': {
            'some': 'abc'
        },
        'expect': "'pathParameters'"
    },
    {
        'name': '5. if payload is number and missing data property',
        'payload': 234,
        'expect': "'int' object is not subscriptable"
    },
    {
        'name': '6. if payload is an empty list "[]"',
        'payload': [],
        'expect': "list indices must be integers or slices, not str"
    },
    {
        'name': '7. if payload is an emoty dict "{}"',
        'payload': {},
        'expect': "'pathParameters'"
    },
    {
        'name': '8. if payload is a boolean value "True"',
        'payload': True,
        'expect': "'bool' object is not subscriptable"
    },
    {
        'name': '9. if payload is a string',
        'payload': 'string',
        'expect': "string indices must be integers"
    }]
}

@pytest.fixture
def mock_response_success(monkeypatch):
    def mock_get(*args, **kwargs):
        return mockPokemon

    monkeypatch.setattr(Request, "get", mock_get)

@pytest.fixture
def mock_response_not_found(monkeypatch):
    def mock_get(*args, **kwargs):
        return HTTPError('404 not found')

    monkeypatch.setattr(Request, "get", mock_get)

def test_lambda_handler_success(mock_response_success):
    events = scenarios['success']
    for i in range(len(events)):
        print(events[i]['name'])
        statusCode, body = lambda_handler(events[i]['payload'], {}).values()

        assert statusCode == 200
        assert json.loads(body)['pokemon'] == {'abilities': ['overgrow'], 'name': 'ivysaur'}
        assert json.loads(body)['fibonacci'] == events[i]['expect']

def test_lambda_handler_pokemon_not_found(mock_response_not_found):
    statusCode, body = lambda_handler({ 'pathParameters': { 'id': '20' } }, {}).values()
    print('returns fibonacci and error instead of pokemon')
    
    assert statusCode == 200
    assert body == '{"fibonacci": 6765, "pokemon": "404 not found"}'

def test_lambda_handler_pokemon_and_fibonaci_throws(mock_response_not_found):
    statusCode, body = lambda_handler({ 'pathParameters': { 'id': 'abc' } }, {}).values()
    print('expect fibonacci to be 0 and pokemon should contain an error message')

    assert statusCode == 200
    assert body == '{"fibonacci": 0, "pokemon": "404 not found"}'
    


def test_lambda_handler_invalid_payload():
    events = scenarios['invalid_payload']
    for i in range(len(events)):
        print(events[i]['name'])
        statusCode, error = lambda_handler(events[i]['payload'], {}).values()

        assert statusCode == 500
        assert error == events[i]['expect']
