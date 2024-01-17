"""
Author: Eyal Roginski
Description: Cardazim server.
"""

import socket
import struct
import argparse


RECV_BUFSIZE = 4096


def run_server(ip: str, port: str | int):
    """
    Infinitely listens for data being sent to the server and prints it
    to the terminal.
    """
    with socket.socket() as sock:
        sock.bind((ip, int(port)))
        sock.listen()
        while True:
            connection, address = sock.accept()
            with connection:
                data = connection.recv(RECV_BUFSIZE)
                try:
                    message_length: int = struct.unpack("<I", data[:4])[0]
                    message: bytes = struct.unpack(
                        f"{message_length}s", data[4:])[0]
                except struct.error:
                    print(
                        f"Invalid packet format from address {address[0]}:{address[1]}. \
                        Packet is: {data}")
                    continue
                message = message.decode(encoding="utf-8")
                print(f"Received message: {message}")


def get_args():
    """
    Get <ip> and <port> command line arguments.
    """
    parser = argparse.ArgumentParser(description='Receive data from clients.')
    parser.add_argument('ip', type=str,
                        help='the ip to listen on')
    parser.add_argument('port', type=int,
                        help='the port to listen on')
    return parser.parse_args()


def main():
    """
    Implementation of the server CLI.
    """
    args = get_args()
    try:
        run_server(args.ip, args.port)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
