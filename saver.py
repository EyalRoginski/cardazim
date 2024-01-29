from furl import furl
from card import Card
from file_saver import FileSaver
from mongo_saver import MongoSaver
from card_id import CardID

SAVER_DRIVERS: dict[str, type] = {"file": FileSaver, "mongodb": MongoSaver}


class Saver:
    """Saver for Cards."""

    def __init__(self, path: str):
        furl_path = furl(path)
        self.driver = SAVER_DRIVERS[furl_path.scheme](path)

    def save(self, card: Card):
        """
        Save the card using the driver.
        """
        self.driver.save(card)

    def load(self, card_id: CardID) -> Card:
        """
        Load a card via `CardID` using the driver.
        """
        return self.driver.load(card_id)
