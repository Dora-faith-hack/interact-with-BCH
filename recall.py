import base64

from Crypto import Random
from Crypto.Cipher import AES

from OP_RETURN import *
from config import *
from iexist import IEXIST

import codecs

from pprint import pprint

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
    # check whether tx_id is equal (duplicated)

    # check status is valid?
    # get the transaction
    trans = OP_RETURN_bitcoin_cmd('getrawtransaction', False, tx_id, 1)
    pprint(trans)
    is_valid = check_status(trans)
    if not is_valid:
        print("[ERROR] The status is invalid !")
        return

    # check whether the address is the same?
    is_same = check_address(trans, source_address)
    if not is_same:
        print("[ERROR] The address is not the same !")
        return

    # decode the target file
    cipher = AESCipher(decode_key)
    with open(encrypt_file_path, 'rb') as encrypted_file:
        encryted_content = encrypted_file.read()
    original_content = cipher.decrypt(encryted_content)

    # hash file with SHA256
    hasher = hashlib.sha256()
    hasher.update(original_content)
    sha256_value = hasher.hexdigest()
    print("recall original file SHA256: ", sha256_value)

    # generate TX
    iexist_protocol = IEXIST()
    op_return_value = iexist_protocol.get_op_return_value(status=0,
                                                          type=data_type,
                                                          data_hash=sha256_value)

    print("OP_RETURN: ", op_return_value)

    # post transaction to BCH
    res = OP_RETURN_send(sender_address, 0.001, op_return_value)
    tx_id = res.get("txid")
    print("TX id: ", tx_id)


def check_status(trans):
    vout = trans.get("vout")
    for v in vout:
        if "OP_RETURN" in v.get("scriptPubKey").get("asm"):
            # Find the OP_RETURN
            op_return_hex = v.get("scriptPubKey").get("asm").split(' ')[1]
            op_return = codecs.decode(op_return_hex, 'hex')
            print(op_return)

    status = True
    for char in op_return[6:8]:
        if char < 128:
            status = False
            break

    return status


def check_address(trans, source_address):
    vout = trans.get('vout')
    addr = vout[0].get("scriptPubKey").get("addresses")[0]
    if addr == source_address:
        return True
    else:
        return False
