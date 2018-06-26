import socket
import threading
import time

from message import Message


class Session:
    # Message types
    PVER = 15
    MSG_SESS = 0
    MSG_REL = 1
    MSG_ACK = 2
    MSG_BEAT = 3
    MSG_MAPREQ = 4
    MSG_MAPDATA = 5
    MSG_OBJDATA = 6
    MSG_OBJACK = 7
    MSG_CLOSE = 8
    SESSERR_AUTH = 1
    SESSERR_BUSY = 2
    SESSERR_CONN = 3
    SESSERR_PVER = 4
    SESSERR_EXPR = 5

    def __init__(self, server, port, username, cookie, args):
        # Connection information
        self.server = server
        self.port = port
        self.username = username
        self.cookie = cookie

        # TODO: Investigate what is in args
        self.args = args

        # Socket for the connection
        self.sk = None

        # State of the connection for the game
        self.state = "conn"

        # Threads

        # "Session reader"
        self.rworkerThread = threading.Thread(target=self.rworker)
        self.rworkerThread.daemon = True
        self.rworkerThread.start()

        # "Session writer"
        self.sworkerThread = threading.Thread(target=self.sworker)
        self.sworkerThread.daemon = True
        self.sworkerThread.start()

        # "Server time ticker"
        self.tickerThread = threading.Thread(target=self.ticker)
        self.tickerThread.daemon = True
        self.tickerThread.start()

    def rworker(self):
        # This for now is really just a dirty implementation of the run method
        # rworker is really a java class.
        alive = True

        while alive:
            try:
                msg = self.recv_msg()
                msg_type = msg.read_uint8()

                if msg_type == Session.MSG_SESS:
                    self.msg_sess(msg)
                if msg_type == Session.MSG_REL:
                    pass
                if msg_type == Session.MSG_ACK:
                    pass
                if msg_type == Session.MSG_MAPDATA:
                    pass
                if msg_type == Session.MSG_OBJDATA:
                    pass
                if msg_type == Session.MSG_CLOSE:
                    pass

            except Exception as e:
                # TODO: Create a more defined excpetion
                print("Make a real exception later...")

    # Recieves the message from the socket
    def recv_msg(self):
        # socket.recvfrom(bufsize) returns data and address of socket
        data, addr = self.sk.recvfrom(65536)

        # TODO: Check the address and compare it to the servers, a little safety check
        print(addr)

        # Stores the data in a Packet Message
        # This is a PMessage class in Loftar's implementation, for now I'll just use a message class.

        # The first byte of this message is the message type. This gets assigned, and the rest of the buffer is passed
        # along without it.

        # TODO: I can either remake his PMessage to handle types or include it all in Message. For now this isn't a concern.
        msg = Message(data)

        return msg

    def msg_sess(self, msg):
        if self.state == "conn":
            error = msg.read_uint8

            if error == 0:
                state = ""
            else:
                # TODO: Close the connection
                pass

    def sworker(self):
        last = 0
        retries = 0

        while True:
            # Time here is measured in seconds
            now = int(time.time())

            if self.state == "conn":
                if now - last > 2:
                    if retries > 5:
                        # TODO: Properly set this to closed.
                        self.state = ""
                        return

                    # TODO: Session Log in Goes here

                    last = now
                    retries = retries + 1
                    time.sleep(0.1)
                else:
                    # The session is connected to the server.
                    now = int(time.time())

                    # Can toggle this to false if another message has been sent to the server
                    beat = True

                    if beat:
                        # Once again python time is in seconds.
                        if now - last > 5:
                            self.beat()
                            last = now

    def sess_login(self):
        msg = Message()
        msg.add_uint16(2)
        # Client identification name for Loftar's stats
        msg.add_string("Hafen")
        # Client version
        msg.add_uint16(Session.PVER)
        msg.add_string(self.username)
        msg.add_uint16(len(self.cookie))
        msg.add_bytes(self.cookie)
       # msg.add_list(self.args)

    def beat(self):
        msg = Message()
        msg.add_uint8(Session.MSG_BEAT)
        self.send_msg(msg)

    def send_msg(self, msg):
        self.sk.sendto(msg.buf, (self.username, self.port))

    def ticker(self):
        pass
