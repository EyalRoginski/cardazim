"""
Author: Eyal Roginski
Description: Cardazim client.
"""

import argparse
import sys
from connection import Connection


def send_data(connection: Connection, data: str):
    """
    Send data to server in address (server_ip, server_port).
    """
    connection.send_message(data)


def get_args():
    """Get command line arguments `server_ip`, `server_port`, `data`."""
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    parser.add_argument("data", type=str, help="the data")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    with Connection.connect(args.server_ip, args.server_port) as connection:
        send_data(connection, args.data)
    print("Done.")


if __name__ == "__main__":
    sys.exit(main())
