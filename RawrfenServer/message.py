import struct
from coord import Coord


# TODO: Move this elsewhere I'd say, just having it here for now so I can make the add_list and get_list
class Color:
    # red, green, blue, alpha
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


class RMessage:

    RMSG_NEWWDG = 0
    RMSG_WDGMSG = 1
    RMSG_DSTWDG = 2
    RMSG_MAPIV = 3
    RMSG_GLOBLOB = 4

    RMSG_RESID = 6
    RMSG_PARTY = 7
    RMSG_SFX = 8
    RMSG_CATTR = 9
    RMSG_MUSIC = 10
    RMSG_TILES = 11

    RMSG_SESSKEY = 13
    RMSG_FRAGMENT = 14
    RMSG_ADDWDG = 15


class Message:

    T_END = 0
    T_INT = 1
    T_STR = 2
    T_COORD = 3
    T_UINT8 = 4
    T_UINT16 = 5
    T_COLOR = 6
    T_TTOL = 8
    T_INT8 = 9
    T_INT16 = 10
    T_NIL = 12
    T_UID = 13
    T_BYTES = 14
    T_FLOAT32 = 15
    T_FLOAT64 = 16
    T_FCOORD32 = 18
    T_FCOORD64 = 19

    def __init__(self, buf=bytearray()):
        self.ptr = 0
        self.buf = bytearray(buf)

        # Variables used in messages.
        # Set this if you want to identify the message as certain type of message.
        self.type = None

        # Set this if you are sending a message to pending
        self.seq = None

        # Amount of sends the message has had
        self.retx = 0

        # Last time the message was sent
        self.last = 0

    def read_bytes(self, len_):
        val = self.buf[self.ptr:self.ptr + len_]
        self.ptr += len_
        return val

    def read_remaining(self):
        val = self.buf[self.ptr:]
        self.ptr = len(self.buf)
        return val

    def read_int8(self):
        val = self.buf[self.ptr]
        self.ptr += 1
        return val

    def read_uint8(self):
        val = self.buf[self.ptr]
        self.ptr += 1
        return val

    def read_int16(self):
        # 'h' represents a short format
        val = struct.unpack('h', self.buf[self.ptr:self.ptr + 2])
        self.ptr += 2
        return val[0]

    def read_uint16(self):
        # 'H' represents an unsigned short format
        val = struct.unpack('H', self.buf[self.ptr:self.ptr + 2])
        self.ptr += 2
        return val[0]

    def read_eunit16(self):
        # 'H' represents an unsigned short format
        val = struct.unpack('>H', self.buf[self.ptr:self.ptr + 2])
        self.ptr += 2
        # This gets unpacked as a tuple...
        return val[0]

    def read_int32(self):
        # 'i' represents an int format
        val = struct.unpack('i', self.buf[self.ptr:self.ptr + 4])
        self.ptr += 4
        return val[0]

    def read_uint32(self):
        # 'I' represents an unsigned int format
        val = struct.unpack('I', self.buf[self.ptr:self.ptr + 4])
        self.ptr += 4
        return val[0]

    def read_int64(self):
        # 'q' represents a long long format
        val = struct.unpack('q', self.buf[self.ptr:self.ptr + 8])
        self.ptr += 8
        return val[0]

    def read_string(self):
        s = ''
        while True:
            c = self.read_uint8()
            if c == 0:
                break
            s += chr(c)
        return s

    def read_float32(self):
        # 'f' represents a float format
        val = struct.unpack('f', self.buf[self.ptr:self.ptr + 4])
        self.ptr += 4
        return val[0]

    def read_float64(self):
        # 'd' represents a double format
        val = struct.unpack('d', self.buf[self.ptr:self.ptr + 8])
        self.ptr += 8
        return val[0]

    def read_coord(self):
        return Coord(self.read_int32(), self.read_int32())

    def read_color(self):
        return Color(self.read_uint8(), self.read_uint8(), self.read_uint8(), self.read_uint8())

    def read_list(self):
        vals = []

        while True:
            if self.eom():
                break

            t = self.read_uint8()

            if t == Message.T_END:
                break
            elif t == Message.T_INT:
                vals.append(self.read_int32())
            elif t == Message.T_STR:
                vals.append(self.read_string())
            elif t == Message.T_COORD:
                vals.append(self.read_coord())
            elif t == Message.T_UINT8:
                vals.append(self.read_uint8())
            elif t == Message.T_UINT16:
                vals.append(self.read_uint16())
            elif t == Message.T_INT8:
                vals.append(self.read_int8())
            elif t == Message.T_INT16:
                vals.append(self.read_int16())
            elif t == Message.T_COLOR:
                vals.append(self.read_color())
            elif t == Message.T_TTOL:
                vals.append(self.read_list())
            elif t == Message.T_NIL:
                vals.append(0)
            elif t == Message.T_UID:
                vals.append(self.read_int64())
            elif t == Message.T_BYTES:
                length = self.read_uint8()

                if (length & 128) != 0:
                    length = self.read_int32()
                vals.append(self.read_bytes(length))
            elif t == Message.T_FLOAT32:
                vals.append(self.read_float32())
            elif t == Message.T_FLOAT64:
                vals.append(self.read_float64())
            elif t == Message.T_FCOORD32:
                #vals.append()
                print("FCoord32 is not implemented yet.")
            elif t == Message.T_FCOORD64:
                #vals.append()
                print("FCoord64 is not implemented yet.")
            else:
                raise Exception("Type not found when reading: " + str(t))
        return vals

    def eom(self):
        if self.ptr >= len(self.buf):
            return True
        return False

    # Loftar uses a rbuf and wbuf byte arrays for read and write seperation, being python I'll just combine it into the
    # same one

    def add_bytes(self, val):
        self.buf.extend(val)

    def add_uint8(self, val):
        self.buf.append(val)

    def add_int16(self, val):
        # 'h' represents a short format
        self.buf.extend(struct.pack('h', val))

    def add_uint16(self, val):
        # 'H' represents an unsigned short format
        self.buf.extend(struct.pack('H', val))

    def add_euint16(self, val):
        # 'H' represents an unsigned short format
        self.buf.extend(struct.pack('>H', val))

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

    def add_float32(self, val):
        # 'f' represents a float format
        self.buf.extend(struct.pack('f', val))

    def add_list(self, list_):
        for l in list_:
            if l is None:
                self.add_uint8(Message.T_NIL)
            elif type(l) == int:
                self.add_uint8(Message.T_INT)
                self.add_int32(l)
            # TODO: Check how this behaves with unicode? and just plain ascii? isinstance(s, unicode):
            # Python 3 says all strings are unicode, so who knows what happens...
            elif type(l) == str:
                self.add_uint8(Message.T_STR)
                self.add_string(l)
            elif type(l) == Coord:
                self.add_uint8(Message.T_COORD)
                # TODO: Could just make a addcoord method like loftar does...
                self.add_int32(l.x)
                self.add_int32(l.y)
            elif type(l) == bytearray:
                self.add_uint8(Message.T_BYTES)
                if len(l) < 128:
                    self.add_uint8(len(l))
                else:
                    self.add_uint8(0x80)
                    self.add_int32(len(l))
                self.add_bytes(l)
            elif type(l) == Color:
                self.add_uint8(Message.T_COLOR)
                self.add_uint8(l.r)
                self.add_uint8(l.g)
                self.add_uint8(l.b)
                self.add_uint8(l.a)
            elif type(l) == float:
                self.add_uint8(Message.T_FLOAT32)
                self.add_float32(l)
            else:
                raise Exception("Cannot encode a " + str(type(l)) + " as TTO.")
            # TODO: There is suppose to be a double condition here, but I feel like I need to differentiate between
            # a float and a double, and I dont know quite how to do that. In python a float is a double, so even the
            # above might not fully work. sys.getsizeof may work, Would need some testing.... A float in python is 64.


