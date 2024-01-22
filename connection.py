import socket

RECV_BUFSIZE = 4096


class Connection:
    """Represents a connection that can read/receive formatted data over a socket."""

    def __init__(self, sock=None):
        if sock is None:
            self.socket = socket.socket()
        else:
            self.socket = sock

    @classmethod
    def connect(cls, host: str, port: str | int):
        """Create a new Connection to `(host, port)`."""
        connection = Connection()
        connection.socket.connect((host, int(port)))
        return connection

    def send_message(self, data: bytes):
        """Send data through the socket."""
        self.socket.sendall(data)

    def receive_message(self) -> bytes:
        """Receives a message from the socket. If it is malformed, raises `RuntimeError`."""
        part = self.socket.recv(RECV_BUFSIZE)
        data = part
        count = 1
        # Just using RECV_BUFSIZE left the loop early because of smaller chunks.
        while len(part) >= RECV_BUFSIZE // 2:
            count += 1
            part = self.socket.recv(RECV_BUFSIZE)
            data += part
        return data

    def close(self):
        """Close the connection."""
        self.socket.close()

    def __repr__(self) -> str:
        return f"<Connection from {self.socket.getsockname()} to {self.socket.getpeername()}>"

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.close()
