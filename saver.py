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

    def get_creators(self) -> list[str]:
        """
        Get a list of all creators' names.
        """
        return self.driver.get_creators()

    def get_cards(self, creator: str) -> list[str]:
        """
        Get a list of the names of all the cards a creator has submitted.
        """
        return self.driver.get_cards(creator)

    def get_card_metadata(self, card_id: CardID) -> dict:
        """
        Get a card's metadata via its ID.
        """
        return self.driver.get_card_metadata(card_id)
