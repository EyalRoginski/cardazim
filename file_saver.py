from pathlib import Path
from os import mkdir
import json
from furl import furl
from card import Card
from card_id import CardID


class FileSaver:
    """
    Driver for saving and loading Cards from the file system.
    """

    def __init__(self, path: str = "."):
        self.path = Path(furl(path).path)
        if not self.path.exists():
            mkdir(self.path)
        elif not self.path.is_dir():
            raise TypeError(f"{self.path} isn't a directory.")

    def save(self, card: Card):
        """
        Saves the `card` including its metadata to a new directory under `dir_path`.
        Overrides existing data.
        """
        card_dir = self.path / f"{CardID.from_card(card).resolve()}"
        if not card_dir.exists():
            mkdir(card_dir)

        with open(
            card_dir / "metadata.json", mode="w", encoding="utf-8"
        ) as metadata_file:
            json.dump(
                {
                    "card.name": card.name,
                    "card.creator": card.creator,
                    "card.riddle": card.riddle,
                    "card.solution": card.solution,
                    "card.image_path": card.image_path,
                },
                metadata_file,
            )

        image_path = card_dir / "image.jpg"
        image_path.unlink(missing_ok=True)
        card.save_image(image_path, "RGB")

    def load(self, card_id: CardID):
        """
        Load a card by CardID.
        Overwrites `<image_dir>/<card_id>.jpg`
        """
        card_dir = self.path / f"{card_id.resolve()}"
        if not card_dir.is_dir():
            raise TypeError(f"{card_dir} isn't a directory.")

        with open(card_dir / "metadata.json", encoding="utf-8") as metadata_file:
            metadata = json.load(metadata_file)

        return Card.create_from_path(
            metadata["card.name"],
            metadata["card.creator"],
            card_dir / "image.jpg",
            metadata["card.riddle"],
            metadata["card.solution"],
        )
