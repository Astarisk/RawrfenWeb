import socket
import threading
import time

from message import Message


class Session:
    # Client version
    PVER = 15

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

    def __init__(self, host, port, username, cookie, args=None):
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
        #self.tickerThread = threading.Thread(target=self.ticker)
        #self.tickerThread.daemon = True
        #self.tickerThread.start()

    def rworker(self):
        # This for now is really just a dirty implementation of the run method
        # rworker is really a java class.
        alive = True

        while alive:
            #try:
            print("RWORKER")
            # TODO: !p.getSocketAddress().equals(server)).. check for address
            print("waiting on a message...")
            msg = self.recv_msg()
            print("grabbing message type...")
            msg_type = msg.read_uint8()
            data = msg.buf[msg.ptr:len(msg.buf)]
            if msg_type == Session.MSG_SESS:
                self.msg_sess(Message(data))
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

            #except Exception as e:
                # TODO: Create a more defined excpetion
                #print("Make a real exception later...")
               #print(e)

    # Recieves the message from the socket
    def recv_msg(self):
        print("Recieving a message...")
        # socket.recvfrom(bufsize) returns data and address of socket
        # DatagramPacket p = new DatagramPacket(new byte[65536], 65536)
        data, addr = self.sk.recvfrom(65536)
        print("Message recieved...")
        print(">>> " + str(data))
        # TODO: Check the address and compare it to the servers, a little safety check
        # ('213.239.201.139', 1870) python saves this as a tuple
        print(addr)

        # Stores the data in a Packet Message
        # This is a PMessage class in Loftar's implementation, for now I'll just use a message class.

        # The first byte of this message is the message type. This gets assigned, and the rest of the buffer is passed
        # along without it.

        # TODO: I can either remake his PMessage to handle types or include it all in Message. For now this isn't a concern.
        msg = Message(data)
        print("Returing recieved message...")
        return msg

    def msg_sess(self, msg):
        print("Reading a msg_sess")
        if self.state == "conn":
            error = msg.read_uint8()
            print("error: " + str(error))
            if error == 0:
                print("State is connected...")
                self.state = ""
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
                #print("Stats is conn")
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
                    #print("Session is now connected to the server")
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

    def beat(self):
        print("Sending a beat...")
        msg = Message()
        msg.add_uint8(Session.MSG_BEAT)
        self.send_msg(msg)

    def send_msg(self, msg):
        print("Sending a message...")
        print(">>>" + str(msg.buf))
        #try:
            #print(self.sk)
        succ = self.sk.sendall(msg.buf)
            #succ = self.sk.send(msg.buf)
        print("Success: " + str(succ))
        #except Exception as e:
            #print(e)
        print("Message sent...")

    def ticker(self):
        pass

