import pytest
import sys

# pylint: disable=missing-class-docstring, missing-function-docstring, invalid-name

sys.path.append("/home/roginski/arazim/cardazim/")
import client
from connection import Connection
from card import Card
from crypt_image import CryptImage

sent_data = []


@pytest.fixture
def mock_connection(monkeypatch):
    def mock_send_message(data: bytes):
        sent_data.append(data)

    monkeypatch.setattr(Connection, "send_message", mock_send_message)


@pytest.fixture
def mock_card(monkeypatch):
    def mock_serialize():
        return b"abcdef"

    monkeypatch.setattr(Card, "serialize", mock_serialize)


def test_send_message(mock_connection, mock_card):
    client.send_card(Connection, Card)
    assert sent_data[0] == b"abcdef"
