"""
Author: Eyal Roginski
Description: Cardazim server.
"""

import socket
import struct
import argparse
import threading


RECV_BUFSIZE = 4096


def handle_connection(connection: socket.socket, address, printing_lock: threading.Lock):
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
        data = connection.recv(RECV_BUFSIZE)
        try:
            message_length: int = struct.unpack("<I", data[:4])[0]
            message: bytes = struct.unpack(
                f"{message_length}s", data[4:])[0]
        except struct.error:
            print(
                f"Invalid packet format from address {address[0]}:{address[1]}.\n \
                Packet is: {data}")
            return
        message = message.decode(encoding="utf-8")
        with printing_lock:
            # Locking printing to not print garbled junk.
            print(f"Received message: {message}")


def run_server(ip: str, port: str | int):
    """
    Infinitely listens for data being sent to the server and prints it
    to the terminal.
    """
    printing_lock = threading.Lock()
    with socket.socket() as sock:
        sock.bind((ip, int(port)))
        sock.listen()
        while True:
            connection, address = sock.accept()
            handle_thread = threading.Thread(target=handle_connection, args=[
                                             connection, address, printing_lock])
            handle_thread.start()


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
