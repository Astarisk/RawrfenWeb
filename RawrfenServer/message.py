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
