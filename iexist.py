class IEXIST:

    head = "IEXIST"
    status_type = 0
    data_hash = ""

    def get_op_return_value(self, status, type, data_hash):

        self.status_type = type

        if status == 1:
            # Set the 8th bit to 1
            self.status_type |= (1 << 7)
        elif status == 0:
            # Set the 8th bit to 0
            self.status_type &= ~(1 << 7)
        else:
            print("[ERROR] Wrong status code number !")

        self.status_type &= 0x00ff
        self.status_type = chr(self.status_type)

        self.data_hash = data_hash

        op_return = self.head + self.status_type + self.data_hash
        return op_return
