import base64

from Crypto import Random
from Crypto.Cipher import AES

from OP_RETURN import *
from config import *
from iexist import IEXIST

BS = 16  # AES-256
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))


def recall_file(decode_key, encrypt_file_path, tx_id, source_address,
                data_type):
    # TODO: check whether tx_id is equal (duplicated)

    # TODO: check status is valid?
    is_valid = check_status()

    # TODO: check whether the address is the same?

    # TODO: decode the target file
    cipher = AESCipher(decode_key)
    with open(encrypt_file_path, 'rb') as encrypted_file:
        encryted_content = encrypted_file.read()
    original_content = cipher.decrypt(encryted_content)

    # TODO: hash file with SHA256
    hasher = hashlib.sha256()
    hasher.update(original_content)
    sha256_value = hasher.hexdigest()
    print("recall original file SHA256: ", sha256_value)

    # TODO: generate TX
    iexist_protocol = IEXIST()
    op_return_value = iexist_protocol.get_op_return_value(status=0,
                                                          type=data_type,
                                                          data_hash=sha256_value)

    print("OP_RETURN: ", op_return_value)

    # TODO: post transaction to BCH
    res = OP_RETURN_send(sender_address, 0.001, op_return_value)
    tx_id = res.get("txid")
    print("TX id: ", tx_id)
