from pathlib import Path
from pymongo import MongoClient
from furl import furl
from card import Card
from card_id import CardID
from os import makedirs


class MongoSaver:
    """
    Driver for saving Cards to a MongoDB database. You need to run a MongoDB database
    before using this.
    """

    def __init__(
        self, mongo_path: str, image_dir: str | Path = Path("~/cardazim_images")
    ):
        furl_path = furl(mongo_path)
        host = furl_path.host
        port = furl_path.port

        self.client = MongoClient(host, port)
        self.client.server_info()  # Check if the server really exists.
        self.database = self.client.cardazim_db
        self.collection = self.database.cardazim_collection
        self.image_dir = Path(image_dir).expanduser().resolve()
        if not self.image_dir.exists():
            makedirs(self.image_dir)

    def save(self, card: Card):
        """
        Save a card to the database. Overwrites `<image_dir>/<card_id>.jpg`
        """
        image_path = self.image_dir / f"{CardID.from_card(card).resolve()}.jpg"

        metadata = {
            "name": card.name,
            "creator": card.creator,
            "riddle": card.riddle,
            "solution": card.solution,
            "image_path": str(image_path),
        }
        self.collection.insert_one(metadata)
        image_path.unlink(missing_ok=True)
        card.save_image(str(image_path), "RGB")

    def load(self, card_id: CardID) -> Card:
        """
        Load a card from the database.
        """
        metadata: dict = self.collection.find_one(
            {"name": card_id.name, "creator": card_id.creator}
        )

        return Card.create_from_path(
            metadata["name"],
            metadata["creator"],
            metadata["image_path"],
            metadata["riddle"],
            metadata["solution"],
        )
