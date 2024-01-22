import struct
from crypt_image import CryptImage, BYTES_PER_UINT


class Card:
    def __init__(
        self,
        name: str,
        creator: str,
        image: CryptImage,
        riddle: str,
        solution: str = None,
    ) -> None:
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    @classmethod
    def create_from_path(
        cls, name: str, creator: str, path: str, riddle: str, solution: str = None
    ):
        """Create a non-encrypted Card from a path to an image in memory."""
        crypt_image = CryptImage.create_from_path(path)
        return Card(name, creator, crypt_image, riddle, solution)

    def __repr__(self) -> str:
        return f"<Card name={self.name}, creator={self.creator}>"

    def __str__(self) -> str:
        return (
            f"Card {self.name} by {self.creator}\n"
            f"  riddle: {self.riddle}\n"
            f"  solution: {self.solution if self.solution else 'unsolved'}"
        )

    def serialize(self) -> bytes:
        """
        Serialize the Card into bytes.
        """
        packed_image = self.image.serialize()
        return struct.pack(
            f"<I{len(self.name)}s"
            f"I{len(self.creator)}s"
            f"I{len(packed_image)}s"
            f"I{len(self.riddle)}s",
            len(self.name),
            self.name.encode(),
            len(self.creator),
            self.creator.encode(),
            len(packed_image),
            packed_image,
            len(self.riddle),
            self.riddle.encode(),
        )

    @classmethod
    def deserialize(cls, serialization: bytes):
        """
        Deserialize the Card from bytes.
        """
        offset = 0
        (name_len,) = struct.unpack_from("<I", serialization, offset)
        offset += BYTES_PER_UINT
        (name,) = struct.unpack_from(f"{name_len}s", serialization, offset)
        name = name.decode()
        offset += name_len
        (creator_len,) = struct.unpack_from("<I", serialization, offset)
        offset += BYTES_PER_UINT
        (creator,) = struct.unpack_from(f"{creator_len}s", serialization, offset)
        creator = creator.decode()
        offset += creator_len
        (image_len,) = struct.unpack_from("<I", serialization, offset)
        offset += BYTES_PER_UINT
        image = CryptImage.deserialize(serialization[offset : offset + image_len])
        offset += image_len
        (riddle_len,) = struct.unpack_from("<I", serialization, offset)
        offset += BYTES_PER_UINT
        (riddle,) = struct.unpack_from(f"{riddle_len}s", serialization, offset)
        riddle = riddle.decode()

        return Card(name, creator, image, riddle)
