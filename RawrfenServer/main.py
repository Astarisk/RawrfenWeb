from authclient import AuthClient
from config import Config
from session import Session
from ui import UI
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import threading
import json
import utils

clients = []
clients_lock = threading.Lock()


class Main(WebSocket):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: I'm not a fan of this way to implement this. Should make a "Client" wraooer around sess and ui to
        # keep the code clean.
        self.ui = None

    def handleMessage(self):
        # Dispatch the message based on type
        # First turn the data into a json for easier handling.
        print("Received a message from the webclient...")
        print(self.data)
        msg = json.loads(self.data)

        if msg["type"] == "login":
            print("authing...")
            print(msg["user"])
            ac = AuthClient(Config.hafenAuthHost, Config.hafenAuthPort, "authsrv.crt")
            success = ac.weblogin(msg['user'], msg['pw'])
            cookie = ac.get_cookie()

            if success:
                self.sendMessage(json.dumps({
                    'type': 'login',
                    'success': True
                }))

            sess = Session(Config.hafenHost, Config.hafenPort, msg['user'], cookie, self, None)
            self.ui = UI(sess)

        if msg["type"] == "play":
            self.ui.sess.queuemsg(utils.login(msg["name"], self.ui.charlist))

        if msg["type"] == "chat_msg":
            self.ui.sess.queuemsg(utils.send_chat_msg(int(msg["chat_id"]), msg["chat_msg"]))

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')
        # Dirty way to close the session for now
        self.ui.sess.state = "fin"


    #def main():
    #    print("authing...")
    #    ac = AuthClient(Config.hafenAuthHost, Config.hafenAuthPort, "authsrv.crt")
    #   ac.login(Config.username, Config.pw)
    #    cookie = ac.get_cookie()

    #   print("Connecting...")
    #    sess = Session(Config.hafenHost, Config.hafenPort, Config.username, cookie, None)
    #    ui = UI(sess)
    #    #sess.sess_login()
    #    import time
    #    # TODO: Need to do better threading than this, But it will do for now...
    #    exit_flag = threading.Event()
    #    while not exit_flag.wait():
    #        print("11")
    #        pass


server = SimpleWebSocketServer('', 8000, Main)
server.serveforever()

#if __name__ == '__main__':
#    Main.main()
