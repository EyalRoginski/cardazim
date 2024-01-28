from pathlib import Path
from os import mkdir
import json
from furl import furl
from card import Card


class FileSaver:
    """
    Driver for saving and loading Cards from the file system.
    """

    def __init__(self, path: str = "."):
        self.path: Path = furl(path).path

    def save(self, card: Card):
        """
        Saves the `card` including its metadata to a new directory under `dir_path`.
        Overrides existing data.
        """
        card_dir = self.path / f"{card.name}"
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

    def load(self, card_id: str):
        """Load a card from directory `card_dir`."""
        card_dir = self.path / card_id
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
