from PIL import Image
from Crypto.Cipher import AES
import hashlib

NONCE = b"arazim"


class CryptImage:
    """Represents an encrypted image."""

    def __init__(self, image: Image):
        self.image: Image = image
        self.key_hash = None

    @classmethod
    def create_from_path(cls, path: str):
        """Create a non-encrypted CryptImage from a given path."""
        image = Image.open(path)
        crypt_image = CryptImage(image)
        return crypt_image

    def encrypt(self, key: bytes):
        """Encrypt the image data using `key`."""
        image_data: bytes = self.image.tobytes()
        single_hash_key: bytes = hashlib.sha256(key).digest()
        cipher = AES.new(single_hash_key, AES.MODE_EAX, nonce=NONCE)
        encrypted_image_data = cipher.encrypt(image_data)
        print("Image len: ", len(image_data))
        print("EncImage len: ", len(encrypted_image_data))
        print("image", image_data[:100])
        print("encrypted", encrypted_image_data[:100])
        # encrypted_image = Image.frombytes("RGBA", self.image.size, encrypted_image_data)
        # self.image = encrypted_image
        self.image.frombytes(encrypted_image_data)
        double_hash_key = hashlib.sha256(single_hash_key).digest()
        self.key_hash = double_hash_key

    def decrypt(self, key: bytes) -> bool:
        """
        Decrypts the image if `key` is correct. Returns whether or not decryption was successful.
        """
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


def test():
    im = CryptImage.create_from_path("/home/roginski/Tranzania.png")
    im.image.save("/home/roginski/test1.png")
    im.encrypt(b"secret")
    print(im.decrypt(b"wrong"))
    print(im.decrypt(b"secret"))
    im.image.save("/home/roginski/test2.png")


if __name__ == "__main__":
    test()
