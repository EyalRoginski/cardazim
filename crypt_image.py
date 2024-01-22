import hashlib
import struct
from PIL import Image
from Crypto.Cipher import AES

NONCE = b"arazim"
BYTES_PER_PIXEL = 4
BYTES_PER_UINT = 4


class CryptImage:
    """Represents an encrypted RGBA image."""

    def __init__(self, image: Image):
        self.image: Image = image
        self.key_hash = None

    @classmethod
    def create_from_path(cls, path: str):
        """Create a non-encrypted CryptImage from a given path."""
        image = Image.open(path)
        crypt_image = CryptImage(image)
        return crypt_image

    def encrypt(self, key: bytes | str):
        """Encrypt the image data using `key`."""

        try:
            key = key.encode()
        except AttributeError:
            pass

        image_data: bytes = self.image.tobytes()
        single_hash_key: bytes = hashlib.sha256(key).digest()
        cipher = AES.new(single_hash_key, AES.MODE_EAX, nonce=NONCE)
        encrypted_image_data = cipher.encrypt(image_data)
        self.image.frombytes(encrypted_image_data)
        double_hash_key = hashlib.sha256(single_hash_key).digest()
        self.key_hash = double_hash_key

    def decrypt(self, key: bytes | str) -> bool:
        """
        Decrypts the image if `key` is correct. Returns whether or not decryption was successful.
        """

        try:
            key = key.encode()
        except AttributeError:
            pass

        single_hash_key: bytes = hashlib.sha256(key).digest()
        double_hash_key = hashlib.sha256(single_hash_key).digest()
        if self.key_hash != double_hash_key:
            return False

        cipher = AES.new(single_hash_key, AES.MODE_EAX, nonce=NONCE)
        encrypted_image_data = self.image.tobytes()
        decrypted_image_data = cipher.decrypt(encrypted_image_data)
        self.image.frombytes(decrypted_image_data)
        self.key_hash = None
        return True

    def serialize(self) -> bytes:
        """
        Serialize the CryptImage into the format:

        `<uint key_hash_length>` `<bytes key_hash>` `<uint width>`
        `<uint height>` `<bytes image data>`

        with uints in Little-Endian
        """

        width, height = self.image.size
        image_data = self.image.tobytes()
        serialization = struct.pack(
            f"<I{len(self.key_hash)}sII{len(image_data)}s",
            len(self.key_hash),
            self.key_hash,
            width,
            height,
            image_data,
        )
        return serialization

    @classmethod
    def deserialize(cls, serialization: bytes):
        """
        Deserialize a CryptImage object of the format:

        `<uint key_hash_length>` `<bytes key_hash>` `<uint width>`
        `<uint height>` `<bytes image data>`

        Raises a `RuntimeError` if malformed object received.
        """
        try:
            (key_hash_length,) = struct.unpack_from("<I", serialization)
            (key_hash,) = struct.unpack_from(
                f"{key_hash_length}s", serialization, BYTES_PER_UINT
            )

            width, height = struct.unpack_from(
                "<II", serialization, BYTES_PER_UINT + key_hash_length
            )

            (image_data,) = struct.unpack_from(
                f"{width * height * BYTES_PER_PIXEL}s",
                serialization,
                BYTES_PER_UINT + key_hash_length + 2 * BYTES_PER_UINT,
            )

            image = Image.frombytes("RGBA", (width, height), image_data)
        except struct.error as exc:
            raise RuntimeError(
                "CryptImage.deserialize received a malformed object serialization."
            ) from exc
        crypt_image = CryptImage(image)
        crypt_image.key_hash = key_hash
        return crypt_image
