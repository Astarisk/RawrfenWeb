import  socket
import ssl
from message import Message
import hashlib


class AuthException(Exception):
    pass


class AuthClient:

    def __init__(self, host, port, cert):
        try:
            self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ws = ssl.wrap_socket(self.sk, ca_certs=cert)
            self.ws.connect((host, port))
        except AuthException as e:
            raise AuthException(e)
        #finally:
        #    self.sk.close()

    def login(self, username, pw):
        pw = hashlib.sha256(bytearray(pw, "utf-8"))
        dig = pw.digest()

        rpl = self.cmd("pw", username, dig)
        stat = rpl.read_string()

        if stat == "ok":
            acc = rpl.read_string()
        elif stat == "no":
            err = rpl.read_string()
        else:
            raise AuthException("Unexpected reply `" + stat + "' from auth server")

    def get_cookie(self):
        rpl = self.cmd("cookie")
        stat = rpl.read_string()

        if stat == "ok":
            return rpl.read_bytes(32)
        else:
            raise AuthException("Unexpected reply `" + stat + "' from auth server")

    def sendmsg(self, msg):
        if len(msg.buf) > 65535:
            print("Message is too large")

        # This converts to Big Edian for the ssl server
        buf = bytearray(2)
        buf[0] = (len(msg.buf) & 0xff00) >> 8
        buf[1] = (len(msg.buf) & 0x00ff)

        buf.extend(msg.buf)
        success = self.ws.sendall(buf)
        print("success: " + str(success))

    def esendmsg(self, *args):
        buf = Message()

        for arg in args:
            if type(arg) == str:
                buf.add_string(arg)
            elif type(arg) == bytes:
                buf.add_bytes(arg)
        self.sendmsg(buf)

    def readall(self, l):
        res = bytearray()
        while True:
            read = l - len(res)

            if read < 1:
                break

            data = self.ws.recv(read)

            if not data:
                break

            res.extend(data)
        return res

    def recvmsg(self):
        msg_length = self.readall(2)
        msg = Message(msg_length)
        msg = self.readall(msg.read_eunit16())
        return Message(msg)

    def cmd(self, *args):
        self.esendmsg(*args)
        return self.recvmsg()
