import socket
import struct

RECV_BUFSIZE = 4096


class Connection:
    """Represents a connection that can read/receive formatted data over a socket."""

    def __init__(self):
        self.socket = socket.socket()

    @classmethod
    def connect(cls, host: str, port: str | int):
        """Create a new Connection to `(host, port)`."""
        connection = Connection()
        connection.socket.connect((host, int(port)))
        return connection

    def send_message(self, message):
        """Send a message through the socket."""
        packet = struct.pack(
            f"<I{len(message)}s",
            len(message),
            bytes(message, encoding="utf-8")
        )
        self.socket.sendall(packet)

    def receive_message(self) -> str:
        """Receives a message from the socket. If it is malformed, raises `RuntimeError`."""
        data = self.socket.recv(RECV_BUFSIZE)
        try:
            message_length: int = struct.unpack("<I", data[:4])[0]
            message: bytes = struct.unpack(
                f"{message_length}s", data[4:])[0]
        except struct.error as exc:
            raise RuntimeError(
                f"Received malformed message from {self.socket.getpeername()}.\n\
                    Message was: {data}") \
                from exc
        message = message.decode(encoding="utf-8")
        return message

    def close(self):
        """Close the connection."""
        self.socket.close()

    def __repr__(self) -> str:
        return f"<Connection from {self.socket.getsockname()} to {self.socket.getpeername()}>"

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.close()
