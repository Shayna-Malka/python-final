import pytest
from api import api_request_random_quote, quotes_from_api

def test_api_request_random_success():
    data=api_request_random_quote()
    assert data["quote"] is not None
    assert data["author"]  is not None

def test_quotes_from_api_success():
    data=quotes_from_api()
    assert len(data) == 300
    assert data[0][0] is not None
    assert data[0][1] is not None
    assert data[299][0] is not None
    assert data[299][1] is not None

