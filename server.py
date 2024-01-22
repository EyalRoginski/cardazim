"""
Author: Eyal Roginski
Description: Cardazim server.
"""

import argparse
import threading
from connection import Connection
from listener import Listener
from card import Card


RECV_BUFSIZE = 4096


def handle_connection(connection: Connection, printing_lock: threading.Lock):
    """
    Handle the connection: receives data from the connection, parses it,
    and prints the message to the screen.

    ### Parameters

    :param connection: the connection to handle.

    :type connection: socket.socket

    :param address: the address from which the connection came.

    :param printing_lock: a threading.Lock to prevent simultaneous printing.
    """
    with connection:
        try:
            packet = connection.receive_message()
            card = Card.deserialize(packet)
        except RuntimeError:
            print(f"Got malformed message from {connection}")
            return
        with printing_lock:
            print(f"Received card '{card.name}' by {card.creator}")


def run_server(ip: str, port: str | int):
    """
    Infinitely listens for data being sent to the server and prints it
    to the terminal.
    """
    printing_lock = threading.Lock()
    with Listener(port, ip) as listener:
        while True:
            connection = listener.accept()
            handle_thread = threading.Thread(
                target=handle_connection, args=[connection, printing_lock]
            )
            handle_thread.start()


def get_args():
    """
    Get <ip> and <port> command line arguments.
    """
    parser = argparse.ArgumentParser(description="Receive data from clients.")
    parser.add_argument("ip", type=str, help="the ip to listen on")
    parser.add_argument("port", type=int, help="the port to listen on")
    return parser.parse_args()


def main():
    """
    Implementation of the server CLI.
    """
    args = get_args()
    try:
        run_server(args.ip, args.port)
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
