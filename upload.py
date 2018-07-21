from OP_RETURN import *
from config import *
from iexist import IEXIST


def hash_file(file_path):
    with open(file_path, 'rb') as input_file:
        file_content = input_file.read()

    hash_sha256 = hashlib.sha256()
    hash_sha256.update(file_content)
    sha256_value = hash_sha256.hexdigest()
    print("file sha256: ", sha256_value)
    return sha256_value


def push_op_return_to_bch(data_type, sha256_value):
    iexist_protocol = IEXIST()
    op_return_value = iexist_protocol.get_op_return_value(status=1,
                                                          type=data_type,
                                                          data_hash=sha256_value)
    print("OP_RETURN: ", op_return_value)

    res = OP_RETURN_send(sender_address, 0.001, op_return_value)
    print(res)

    tx_id = res.get("txid")
    print("TX id: ", tx_id)


def upload_file(file_path, data_type):
    sha256_value = hash_file(file_path)
    push_op_return_to_bch(data_type, sha256_value)
