"""
Author: Eyal Roginski
Description: Cardazim client.
"""

import argparse
from connection import Connection
from card import Card


def send_card(connection: Connection, card: Card):
    """Send the `card` to server in address represented by `connection`."""
    packet = card.serialize()
    print(packet[:100])
    print(len(packet))
    print(len(packet) / 4096)
    connection.send_message(packet)


def get_args():
    """Get command line arguments."""
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    parser.add_argument("card_name", type=str, help="the card name")
    parser.add_argument("card_creator", type=str, help="the card creator")
    parser.add_argument("card_riddle", type=str, help="the card riddle")
    parser.add_argument("card_solution", type=str, help="the card solution")
    parser.add_argument("image_path", type=str, help="path to the card image on disk")
    return parser.parse_args()


def main():
    """Implementation of CLI and sending data to server."""
    args = get_args()
    with Connection.connect(args.server_ip, args.server_port) as connection:
        card = Card.create_from_path(
            args.card_name,
            args.card_creator,
            args.image_path,
            args.card_riddle,
            args.card_solution,
        )
        card.image.encrypt(card.riddle)
        send_card(connection, card)
    print("Done.")


if __name__ == "__main__":
    main()
