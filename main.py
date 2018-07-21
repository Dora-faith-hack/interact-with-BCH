from recall import *
from upload import *

file_path = 'test_file'

if __name__ == '__main__':
    # TODO: socket to upload and give (filepath, data_type)
    upload_file(file_path, data_type=0)
    # TODO: save the TX id with the file to database


    # TODO: socket to recall and give
    # TODO: (decode_key, filepath, tx_id, source_address, data_type)
    recall_file(decode_key, file_path, tx_id, source_address, data_type)
