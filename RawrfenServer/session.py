import socket
from threading import Lock, Thread, Condition
import time

from ocache import Ocache, Gob
from message import Message
from message import RMessage


class ObjAck:

    def __init__(self, id, frame, recv):
        self.id = id
        self.frame = frame
        self.recv = recv
        self.sent = 0


class Session:
    # Client version
    PVER = 17

    # Message types
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

    def __init__(self, host, port, username, cookie, websocket, args=None):
        # Connection information
        self.host = host
        self.port = port
        self.username = username
        self.cookie = cookie

        # TODO: Investigate what is in args
        self.args = args

        # Socket for the connection
        #try:
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sk.connect((self.host, self.port))
        #except Exception as e:
            #print("Socket connection failure")
            #print(e)

        # State of the connection for the game
        self.state = "conn"

        # Connection to the web interface
        self.websocket = websocket

        # Threads

        # "Session reader"
        self.rworkerThread = Thread(target=self.rworker)
        self.rworkerThread.daemon = True
        self.rworkerThread.start()

        # "Session writer"
        self.sworkerThread = Thread(target=self.sworker)
        self.sworkerThread.daemon = True
        self.sworkerThread.start()
        self.sworkerThread_condition = Condition()

        # "Server time ticker"
        #self.tickerThread = Thread(target=self.ticker)
        #self.tickerThread.daemon = True
        #self.tickerThread.start()


        # Class variables
        self.rseq = 0
        self.tseq = 0
        self.acktime = -1
        self.ackthresh = .03

        # ui / wdgmsgs
        self.uimsgs = []
        self.uimsg_lock = Lock()

        # Outgoing messages
        self.pending = []
        self.pending_lock = Lock()

        # Objacks messages
        self.objacks = {}
        self.objacks_lock = Lock()

        # Ocache
        self.oc = Ocache()

    def rworker(self):
        # This for now is really just a dirty implementation of the run method
        # rworker is really a java class.
        alive = True

        while alive:
            #try:
            # TODO: !p.getSocketAddress().equals(server)).. check for address
            msg = self.recv_msg()
            msg_type = msg.read_uint8()
            #print("msg_type->: " + str(msg_type))
            data = Message(msg.read_remaining())

            if msg_type == Session.MSG_SESS:
                self.msg_sess(data)
            if msg_type == Session.MSG_REL:
                self.msg_rel(data)
            if msg_type == Session.MSG_ACK:
                self.gotack(data)
            if msg_type == Session.MSG_MAPDATA:
                pass
            if msg_type == Session.MSG_OBJDATA:
                pass
                # TODO: The client loading slowdown exists within parsing OBJDATA messages
                #print("RECEIVING MSG_OBJDATA")
                #self.objdata(data)
            if msg_type == Session.MSG_CLOSE:
                self.state = "fin"

            if self.state == "fin":
                return

            #except Exception as e:
                # TODO: Create a more defined excpetion
                #print("Make a real exception later...")
               #print(e)

    def objdata(self, msg):
        while not msg.eom():
            fl = msg.read_uint8()
            id_ = msg.read_uint32()
            frame = msg.read_int32()

            with self.oc.gobs_lock:
                if fl != 0:
                    self.oc.remove(id, frame - 1)
                gob = self.oc.getgob(id, frame)

                if gob:
                    gob.frame = frame
                    gob.virtual = ((fl & 2) != 0)

                while True:
                    msg_type = msg.read_uint8()

                    if msg_type == Ocache.OD_REM:
                        self.oc.remove(id, frame)
                    elif msg_type == Ocache.OD_END:
                        break
                    else:
                        self.oc.receive(gob, msg_type, msg)

                with self.objacks_lock:
                    if id in self.objacks:
                        ack = self.objacks.get(id)
                        ack.frame = frame
                        ack.recv = int(time.time())
                    else:
                        self.objacks[id] = ObjAck(id_, frame, int(time.time()))

    def gotack(self, seq):
        seq = seq.read_uint16()
        print("Received an ack: " + str(seq))
        with self.pending_lock:
            for rmsg in self.pending:
                if rmsg.seq <= seq:
                    self.pending.remove(rmsg)

    # Recieves the message from the socket
    def recv_msg(self):
        # socket.recvfrom(bufsize) returns data and address of socket
        # DatagramPacket p = new DatagramPacket(new byte[65536], 65536)
        data, addr = self.sk.recvfrom(65536)
        #print("<<< " + str(data))
        # TODO: Check the address and compare it to the servers, a little safety check
        # ('213.239.201.139', 1870) python saves this as a tuple
        #print(addr)

        # Stores the data in a Packet Message
        # This is a PMessage class in Loftar's implementation, for now I'll just use a message class.

        # The first byte of this message is the message type. This gets assigned, and the rest of the buffer is passed
        # along without it.

        # TODO: I can either remake his PMessage to handle types or include it all in Message. For now this isn't a concern.
        msg = Message(data)
        return msg

    # Deals with Session Connection messages.
    def msg_sess(self, msg):
        print("Reading a msg_sess")
        if self.state == "conn":
            error = msg.read_uint8()
            if error == 0:
                print("State is connected...")
                self.state = ""
            else:
                # TODO: Close the connection in a much finer way
                self.state = "fin"

    def msg_rel(self, msg):
        #print("Found a msg_rel")
        seq = msg.read_uint16()

        while not msg.eom():
            msg_type = msg.read_uint8()
            if (msg_type & 0x80) != 0:
                msg_type &= 0x7f
                length = msg.read_uint16()
                #print(">> msg_rel->type: " + str(msg_type))
                pmsg = Message(msg.read_bytes(length))
            else:
                pmsg = Message(msg.read_remaining())

            # getrel(seq, PMessage) -> Looks like a circle buffer
            # // handlerel(PMessage msg) in the Java code -> deals with the messages
            if seq == self.rseq:
                # NEWDG, WDGMSG, DSSTWDG, ADD_WDG all get passed to UI to be processed..
                if msg_type == RMessage.RMSG_NEWWDG or msg_type == RMessage.RMSG_WDGMSG \
                        or msg_type == RMessage.RMSG_DSTWDG or msg_type == RMessage.RMSG_ADDWDG:
                    with self.uimsg_lock:
                        tmp = Message()
                        tmp.add_uint8(msg_type)
                        tmp.add_bytes(pmsg.buf)
                        self.uimsgs.append(tmp)
                elif msg_type == RMessage.RMSG_MAPIV:
                    pass
                elif msg_type == RMessage.RMSG_GLOBLOB:
                    pass
                elif msg_type == RMessage.RMSG_RESID:
                    resid = pmsg.read_uint16()
                    resname = pmsg.read_string()
                    resver = pmsg.read_uint16()

                    print("RESNAME: " + resname)
                elif msg_type == RMessage.RMSG_PARTY:
                    pass
                elif msg_type == RMessage.RMSG_SFX:
                    pass
                elif msg_type == RMessage.RMSG_CATTR:
                    pass
                elif msg_type == RMessage.RMSG_MUSIC:
                    pass
                elif msg_type == RMessage.RMSG_SESSKEY:
                    pass
                elif msg_type == RMessage.RMSG_FRAGMENT:
                    pass
                else:
                    raise Exception("<<< UNSUPPORTED RMESSAGE TYPE OF : " + str(msg_type))
                self.sendack(seq)
                self.rseq = (self.rseq + 1) % 65536
            seq += 1

    # ---------------------------------------------------
    # Below this is sworker and sworker related functions
    # TODO: I might just want to seperate this logic into another class if possible. No need to make session look ugly.
    # ---------------------------------------------------
    def sworker(self):
        last = 0
        retries = 0
        to = 0

        while True:
            # Time here is measured in seconds
            now = int(time.time())

            if self.state == "conn":
                if now - last > 2:
                    print("Trying to conn...")
                    if retries > 5:
                        print("Failed to connect 5 times...")
                        # TODO: Properly set this to closed.
                        self.state = ""
                        return

                    # TODO: Session Log in Goes here
                    print("Sess login")
                    self.sess_login()
                    print("Tried to connect...")
                    last = now
                    print("Now updated..")
                    retries = retries + 1
                    print("retry incremented...")
                    time.sleep(0.1)
                    print("Looping again...")
            else:

                # # Thread timeouts..
                # to = 5
                #
                # with self.pending_lock:
                #     if len(self.pending) > 0:
                #         to = 0.06
                #
                # with self.objacks_lock:
                #     if len(self.pending) > 0 and to > .12:
                #         to = 0.2
                #
                # if self.acktime > 0:
                #     to = self.acktime + self.ackthresh - now
                #
                #     if to > 0:
                #         time.sleep(to)

                # The session is connected to the server.
                now = int(time.time())

                # Can toggle this to false if another message has been sent to the server
                beat = True

                # Check and dispatch messages in pending...
                with self.pending_lock:
                    for rmsg in self.pending:

                        if rmsg.retx == 0:
                            txtime = 0
                        elif rmsg.retx == 1:
                            txtime = .08
                        elif rmsg.retx < 4:
                            txtime = .200
                        elif rmsg.retx < 10:
                            txtime = .620
                        else:
                            txtime = 2
                        if now - rmsg.last > txtime:
                            rmsg.last = now
                            rmsg.retx = rmsg.retx + 1
                            self.send_msg(rmsg)
                        beat = False

                with self.objacks_lock:
                    msg = None
                    dic = sorted(self.objacks)

                    for ack in dic:
                        objack = self.objacks[ack]

                        send = False
                        del_ = False

                        if now - objack.sent > .2:
                            send = True
                        if now - objack.recv < .12:
                            send = True
                            del_ = True
                        if send:
                            if msg is None:
                                msg = Message()
                                msg.add_uint8(Session.MSG_OBJACK)
                            elif len(msg.buf) > 1000 - 9:
                                self.send_msg(msg)
                                beat = False
                                msg = Message()
                                msg.add_uint8(Session.MSG_OBJACK)

                            msg.add_uint32(objack.id)
                            msg.add_int32(objack.frame)
                            objack.sent = now

                        if del_:
                            del self.objacks[ack]

                    if msg:
                        self.send_msg(msg)
                        beat = False

                if beat:
                    # Once again python time is in seconds.
                    if now - last > 5:
                        self.beat()
                        last = now
            if self.state == "fin":
                return

    def sess_login(self):
        print("Forming login message")
        msg = Message()
        msg.add_uint8(Session.MSG_SESS)
        msg.add_uint16(2)
        # Client identification name for Loftar's stats
        msg.add_string("Hafen")
        # Client version
        msg.add_uint16(Session.PVER)
        msg.add_string(self.username)
        msg.add_uint16(len(self.cookie))
        msg.add_bytes(self.cookie)
        print("Message being sent off")
        self.send_msg(msg)
       # msg.add_list(self.args)

    # Session specific messages
    def beat(self):
        print("Sending a beat...")
        msg = Message()
        msg.add_uint8(Session.MSG_BEAT)
        self.send_msg(msg)

    def sendack(self, seq):
        #print("Ack sent...")
        msg = Message()
        msg.add_uint8(Session.MSG_ACK)
        msg.add_uint16(seq)
        self.send_msg(msg)

    def send_msg(self, msg):
        # print(">>> " + str(msg.buf))
        success = self.sk.sendall(msg.buf)

    def ticker(self):
        pass

    # Adds a message to be sent out to pending
    def queuemsg(self, rmsg):
        msg = Message()
        msg.add_uint8(Session.MSG_REL)
        msg.add_uint16(self.tseq)
        msg.seq = self.tseq
        msg.add_bytes(rmsg.buf)
        self.tseq = (self.tseq + 1) % 65536

        with self.pending_lock:
            self.pending.append(msg)
            #s = ""
            #for b in msg.buf:
            #    s += str(b)
            #    s +=", "

            #print("que.. " + str(s))

    # Retrieves a message from uimsgs
    def getuimsg(self):
        msg = None
        with self.uimsg_lock:
            if len(self.uimsgs) == 0:
                return None
            msg = self.uimsgs.pop(0)
        return msg



