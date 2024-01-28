from pathlib import Path
from os import mkdir
import json
from furl import furl
from card import Card
from file_saver import FileSaver

SAVER_DRIVERS: dict[str, type] = {"file": FileSaver}


class Saver:
    """Saver for Cards."""

    def __init__(self, path: str):
        furl_path = furl(path)
        self.driver = SAVER_DRIVERS[furl_path.scheme](path)

    def save(self, card: Card):
        self.driver.save(card)

    def load(self, card_id: str) -> Card:
        return self.driver.load(card_id)
