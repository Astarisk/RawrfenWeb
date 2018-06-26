import struct


class Message:

    def __init__(self, buf=bytearray()):
        self.ptr = 0
        self.buf = bytearray(buf)

    def read_int8(self):
        pass

    def read_uint8(self):
        val = self.buf[self.ptr]
        self.ptr += 1
        return val

    def read_int16(self):
        # 'h' represents a short format
        val = struct.unpack('h', self.buf[self.ptr:self.ptr + 2])
        self.ptr += 2
        return val

    def read_uint16(self):
        # 'H' represents an unsigned short format
        val = struct.unpack('H', self.buf[self.ptr:self.ptr + 2])
        self.ptr += 2
        return val

    def read_int32(self):
        # 'i' represents an int format
        val = struct.unpack('i', self.buf[self.ptr:self.ptr + 4])
        self.ptr += 4
        return val

    def read_uint32(self):
        # 'I' represents an unsigned int format
        val = struct.unpack('I', self.buf[self.ptr:self.ptr + 4])
        self.ptr += 4
        return val

    def read_int64(self):
        # 'q' represents a long long format
        val = struct.unpack('q', self.buf[self.ptr:self.ptr + 8])
        self.ptr += 8
        return val

    def read_string(self):
        s = ''
        while True:
            c = self.read_uint8()
            if c == 0:
                break
            s += chr(c)
        # Strings are returned as utf-8 in the hafen client
        return s.encode("utf-8")

    def read_float32(self):
        # 'f' represents a float format
        val = struct.unpack('f', self.buf[self.ptr:self.ptr + 4])
        self.ptr += 4
        return val

    def eom(self):
        if self.ptr >= len(self.buf):
            return True
        return False

    # Loftar uses a rbuf and wbuf byte arrays for read and write seperation, being python I'll just combine it into the
    # same one

    def add_bytes(self, val):
        self.buf.extend(val)

    def add_uint8(self, val):
        self.buf.extend(struct.pack(val))

    def add_int16(self, val):
        # 'h' represents a short format
        self.buf.extend(struct.pack('h', val))

    def add_uint16(self, val):
        # 'H' represents an unsigned short format
        self.buf.extend(struct.pack('H', val))

    def add_int32(self, val):
        # 'i' represents an int format
        self.buf.extend(struct.pack('i', val))

    def add_uint32(self, val):
        # 'I' represents an unsigned int format
        self.buf.extend(struct.pack('I', val))

    def add_int64(self, val):
        # 'q' represents a long long format
        self.buf.extend(struct.pack('q', val))

    def add_string(self, val, enc="utf-8"):
        # Encode the string into the proper format
        self.buf.extend(val.encode(enc))
        # Loftar uses 0 to signify end of string
        self.buf.append(0)
