import socket
from connection import Connection


class Listener:
    """Represents a listener on a port."""

    def __init__(self, port: str | int, host: str, backlog: int = 1000) -> None:
        self.socket = socket.socket()
        self.socket.bind((host, int(port)))
        self.backlog = backlog

    def start(self):
        """Start listening for connections."""
        self.socket.listen()

    def stop(self):
        """Stop listening for connections."""
        self.socket.close()

    def accept(self) -> Connection:
        """Accept a connection."""
        connection, address = self.socket.accept()
        connection.close()
        return Connection.connect(address[0], address[1])

    def __repr__(self) -> str:
        host, port = self.socket.getsockname()
        return f"Listener(port={port}, host='{host}', backlog={self.backlog})"

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.socket.close()
