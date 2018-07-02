# Poorly named for now since this client doesn't even have a UI, but this is to try and keep consistent with the client

from message import Message, RMessage
from threading import Thread


class UI:

    def __init__(self, session):
        self.rwidgets = []
        self.sess = session

        self.remoteui_thread = Thread(target=self.remoteui)
        self.remoteui_thread.daemon = True
        self.remoteui_thread.start()
    # These methods are the core of botting, and the foundation of this class. For consistency I'll keep these going.

    # public void addwidget(int id, int parent, Object[] pargs)
    def addwdidget(self, id_, parent, pargs):
        print("Added: " + "\t id: " + str(id_) + "\tparent: " + str(parent) + "\tpargs: " + str(pargs))

    # public void newwidget(int id, String type, int parent, Object[] pargs, Object... cargs)
    def newwidget(self, id_, type_, parent, pargs, cargs):
        print("\n" + "id: " + str(id_) + "\ttype: " + str(type_) + "\tparent: " + str(parent) + "\tpargs: " + str(
            pargs) + "\tcargs: " + str(cargs))

    # public void uimsg(int id, String msg, Object... args)
    def uimsg(self, id_, name, args):
        print("\n" + "id: " + str(id_) + "\tmsg: " + str(name) + "\targs: " + str(args))

    # public void destroy(int id)
    def destroy(self, id_):
        print("Destroyed: " + str(id_))

    # This loops through and dispatches the sess.ui msgs to the right function
    # TODO: Add a wait in this loop so it isnt so spammy
    def remoteui(self):
        while True:
            msg = None
            while True:
                msg = self.sess.getuimsg()
                if msg is None:
                    break

                msg_type = msg.read_uint8()
                if msg_type == RMessage.RMSG_NEWWDG:
                    id_ = msg.read_uint16()
                    type_ = msg.read_string()
                    parent = msg.read_uint16()
                    pargs = msg.read_list()
                    cargs = msg.read_list()
                    self.newwidget(id_, type_, parent, pargs, cargs)
                elif msg_type == RMessage.RMSG_WDGMSG:
                    id_ = msg.read_uint16()
                    name = msg.read_string()
                    args = msg.read_list()
                    self.uimsg(id_, name, args)
                elif msg_type == RMessage.RMSG_DSTWDG:
                    id_ = msg.read_uint16()
                    self.destroy(id_)
                elif msg_type == RMessage.RMSG_ADDWDG:
                    id_ = msg.read_uint16()
                    parent = msg.read_uint16()
                    pargs = msg.read_list()
                    self.addwdidget(id_, parent, pargs)
