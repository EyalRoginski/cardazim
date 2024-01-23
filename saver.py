from pathlib import Path
import json
from card import Card


class Saver:
    """Saver for Cards."""

    def save(self, card: Card, dir_path="."):
        """Saves the `card` including its metadata to a new directory under `dir_path`."""
        dir_path = Path(dir_path)
        card_dir = dir_path / f"{card.name}"
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
        card.save_image(image_path)
