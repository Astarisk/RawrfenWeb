from threading import Lock
from coord import Coord
from message import Message


class Ocache:

    OD_REM = 0
    OD_MOVE = 1
    OD_RES = 2
    OD_LINBEG = 3
    OD_LINSTEP = 4
    OD_SPEECH = 5
    OD_COMPOSE = 6
    OD_ZOFF = 7
    OD_LUMIN = 8
    OD_AVATAR = 9
    OD_FOLLOW = 10
    OD_HOMING = 11
    OD_OVERLAY = 12
    # OD_AUTH = 13 -- Removed
    OD_HEALTH = 14
    OD_BUDDY = 15
    OD_CMPPOSE = 16
    OD_CMPMOD = 17
    OD_CMPEQU = 18
    OD_ICON = 19
    OD_RESATTR = 20
    OD_END = 255
    posres = Coord(0.0107421875, 0.0107421875)

    def __init__(self):
        self.gobs = {}
        self.gobs_lock = Lock()

    def getgob(self, id, frame):
        pass

    def remove(self, id, frame):
        pass

    def move(self, gob, msg):
        c = msg.read_coord()
        ia = msg.read_uint16()

        # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def cres(self, gob, msg):
        resid = msg.read_uint16()
        sdt = None

        if resid & 0x8000 != 0:
            resid &= ~0x8000
            sdt = Message(msg.read_bytes(msg.read_uint8()))

        # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def linberg(self, gob, msg):
        s = msg.read_coord().mul(Ocache.posres)
        v = msg.read_coord().mul(Ocache.posres)

        # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def linstep(self, gob, msg):
        t = None
        e = None
        w = msg.read_int32()

        if w == -1:
            t = e = -1
        elif (w & 0x80000000) == 0:
            pass
            #t = w * 0x1p-10
            #e = -1
        else:
            #t = (w & ~0x80000000) * 0x1p-10
            w = msg.read_int32()
            #e = (w < 0)?-1:(w * 0x1p-10)

        # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def homing(self, gob, msg):
        oid = msg.read_uint32()

        if oid == 0xffffffff:
            pass
        else:
            tgtc = msg.read_coord().mul(Ocache.posres)
            v = msg.read_int32() # * 0x1p-10 * 11
        # TODO: Finish this... For now just getting the messages out of the way

    def speak(self, gob, msg):
        zo = float(msg.read_int16() / 100)
        txt = msg.read_string()

        # TODO: Finish this... For now just getting the messages out of the way

    def composite(self, gob, msg):
        id = msg.read_uint16()

       # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def cmppose(self, gob, msg):
        poses = []
        tposes = []
        pfl = msg.read_uint8()
        seq = msg.read_uint8()


        if (pfl & 2) != 0:
            while True:
                resid = msg.read_uint16()
                if resid == 65535:
                    break
                sdt = None
                if (resid & 0x8000) != 0:
                    resid &= ~0x8000
                    sdt = Message(msg.read_bytes(msg.read_uint8()))

                # Add pose to list here...

        ttime = 0
        if (pfl & 4) != 0:
            while True:
                resid = msg.read_uint16()

                if resid == 65535:
                    break

                sdt = None
                if (resid & 0x8000) != 0:
                    resid &= ~0x8000
                    sdt = Message(msg.read_bytes(msg.read_uint8()))
                # Add pose to list here...

            ttime = float((msg.read_uint8() / 10.0))

        # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def cmpmod(self, gob, msg):
        mod = []
        mseq = 0

        while True:
            modid = msg.read_uint16()

            if modid == 65535:
                break

            while True:
                resid = msg.read_uint16()

                if resid == 65535:
                    break

                sdt = None
                if (resid & 0x8000) != 0:
                    resid &= ~0x8000
                    sdt = Message(msg.read_bytes(msg.read_uint8()))

    def cmpequ(self, gob, msg):
        equ = None
        eseq = 0

        while True:
            h = msg.read_uint8()
            if h == 255:
                break
            ef = h & 0x80
            et = h & 0x7f
            at = msg.read_string()
            res = None
            resid = msg.read_uint16()
            sdt = None

            if (resid & 0x8000) != 0:
                resid &= ~0x8000
                sdt = Message(msg.read_bytes(msg.read_uint8()))

            # Grab the res here...

            if (ef & 128) != 0:
                x = msg.int16()
                y = msg.int16()
                z = msg.int16()
            else:
                pass

        # TODO: Finish this... For now just getting the messages out of the way

    def zoff(self, gob, msg):
        off = msg.read_int16()

        # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def lumin(self, gob, msg):
        off = msg.read_coord()
        sz = msg.read_uint16()
        str = msg.read_uint8()

        # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def avatar(self, gob, msg):
        layers = []
        while True:
            layer = msg.read_uint16()

            if layer == 65535:
                break
            #layers.append()
        # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def follow(self, gob, msg):
        oid = msg.read_uint32()
        xfres = None
        xfname = None

        if oid != 0xffffffff:
            id = msg.read_uint16()
            xfname = msg.read_string()

        # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def overlay(self, gob, msg):
        olid = msg.read_int32()
        prs = (olid & 1) != 0
        # olid >>>= 1
        resid = msg.read_uint16()
        res = None
        sdt = None
        if resid == 65535:
            res = None
        else:
            if (resid & 0x8000) != 0:
                resid &= ~0x8000
                sdt = Message(msg.read_bytes(msg.read_uint8()))
            # Grab the res here...

        # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def health(self, gob, msg):
        hp = msg.read_uint8()

        # TODO: Finish this... For now just getting the messages out of the way
        if gob:
            pass

    def buddy(self, gob, msg):
        name = msg.read_string()

        if (len(name) > 0):
            group = msg.read_uint8()
            btype = msg.read_uint8()

            # TODO: Finish this... For now just getting the messages out of the way
            if gob:
                pass
        else:
            # TODO: Finish this... For now just getting the messages out of the way
            if gob:
                pass

    def icon(self, gob, msg):
        resid = msg.read_uint16()
        res = None

        if resid == 65535:
            # TODO: Finish this... For now just getting the messages out of the way
            if gob:
                pass
        else:
            ifl = msg.read_uint8()
            # TODO: Finish this... For now just getting the messages out of the way
            if gob:
                pass

    def resattr(self, gob, msg):
        # This is all wrong...
        resid = msg.read_uint16()
        len_ = msg.read_uint8()
        dat = None

        if len_ > 0:
            data = msg.read_bytes(len_)
        else:
            dat = None

    def receive(self, gob, type_, msg):
        print("Ocache type: " + str(type_))

        if type_ == Ocache.OD_MOVE:
            self.move(gob, msg)
        elif type_ == Ocache.OD_RES:
            self.cres(gob, msg)
        elif type_ == Ocache.OD_LINBEG:
            self.linberg(gob, msg)
        elif type_ == Ocache.OD_LINSTEP:
            self.linstep(gob, msg)
        elif type_ == Ocache.OD_HOMING:
            self.homing(gob, msg)
        elif type_ == Ocache.OD_SPEECH:
            self.speak(gob, msg)
        elif type_ == Ocache.OD_COMPOSE:
            self.composite(gob, msg)
        elif type_ == Ocache.OD_CMPPOSE:
            self.cmppose(gob, msg)
        elif type_ == Ocache.OD_CMPMOD:
            self.cmpmod(gob, msg)
        elif type_ == Ocache.OD_CMPEQU:
            self.cmpequ(gob, msg)
        elif type_ == Ocache.OD_ZOFF:
            self.zoff(gob, msg)
        elif type_ == Ocache.OD_LUMIN:
            self.lumin(gob, msg)
        elif type_ == Ocache.OD_AVATAR:
            self.avatar(gob, msg)
        elif type_ == Ocache.OD_FOLLOW:
            self.follow(gob, msg)
        elif type_ == Ocache.OD_OVERLAY:
            self.overlay(gob, msg)
        elif type_ == Ocache.OD_HEALTH:
            self.health(gob, msg)
        elif type_ == Ocache.OD_BUDDY:
            self.buddy(gob, msg)
        elif type_ == Ocache.OD_ICON:
            self.icon(gob, msg)
        elif type_ == Ocache.OD_RESATTR:
            self.resattr(gob, msg)
        else:
            print("Unknown objdelta type: " + str(type_))


class Gob:
    # I will include the Gob inside Ocache for now. TODO: Refactor this out at a later date.

    def __init__(self, id):
        self.id = id

        # Not really needed for botting purposes
        self.frame = None
        self.virtual = None
