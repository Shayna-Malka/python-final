import pytest
import os
from database import create_databases, extract_data_from_tagged_db, extract_data_from_untagged_db, add_data_to_databases, search_author

def test_api_request_random_success():
    create_databases()
    assert os.path.exists("quotes_without_tags.db")
    assert os.path.exists("quotes_with_tags.db")


def test_extract_data_from_tagged_db_success():
    add_data_to_databases()
    data = extract_data_from_tagged_db("inspirational")
    assert len(data) > 0
    assert data[0][0] == '“It is our choices, Harry, that show what we truly are, far more than our abilities.”'
    assert data[0][1] == "J.K. Rowling"

def test_extract_data_from_untagged_db_success():
    data = extract_data_from_untagged_db(10)
    assert len(data) == 10
    assert data[0][0] == "Your heart is the size of an ocean. Go find yourself in its hidden depths."
    assert data[0][1] == "Rumi"

def test_search_author_success():
    data = search_author("Albert Einstein")
    assert len(data) == 13
    assert "If You Are Out To Describe The Truth, Leave Elegance To The Tailor." in data[6]
    