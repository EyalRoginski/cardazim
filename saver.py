from pathlib import Path
from os import mkdir
import json
from card import Card


class Saver:
    """Saver for Cards."""

    def save(self, card: Card, dir_path="."):
        """
        Saves the `card` including its metadata to a new directory under `dir_path`.
        Overrides existing data.
        """
        dir_path = Path(dir_path)
        card_dir = dir_path / f"{card.name}"
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

    def load(self, card_dir: str | Path):
        """Load a card from directory `card_dir`."""
        card_dir = Path(card_dir)
        if not card_dir.is_dir():
            raise TypeError("card_dir isn't a directory.")

        with open(card_dir / "metadata.json", encoding="utf-8") as metadata_file:
            metadata = json.load(metadata_file)

        return Card.create_from_path(
            metadata["card.name"],
            metadata["card.creator"],
            card_dir / "image.jpg",
            metadata["card.riddle"],
            metadata["card.solution"],
        )


if __name__ == "__main__":
    card = Card.create_from_path(
        "street", "eyal", "/home/roginski/street.jpg", "How?", "this"
    )
    card.encrypt()
    with open("./unsolved_cards/street", "bw") as file:
        file.write(card.serialize())
