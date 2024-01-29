from typing import NamedTuple
from card import Card


class CardID(NamedTuple):
    """
    An ID for cards, consisting of the name and creator.
    """

    name: str
    creator: str

    def resolve(self) -> str:
        """
        Resolve this ID into a string of the form `<card.creator>_<card.name>`.
        """
        return f"{self.creator}_{self.name}"

    @classmethod
    def from_card(cls, card: Card):
        """
        Create `CardID(name=card.name, creator=card.creator)` from `card`.
        """
        return CardID(name=card.name, creator=card.creator)
