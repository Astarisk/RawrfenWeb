import threading

class Session:

    def __init__(self):
        # Threads

        # "Session reader"
        self.rworkerThread = threading.Thread(target=self.rworker)
        self.rworkerThread.daemon = True
        self.rworkerThread.start()

        # "Session writer"
        self.sworkerThread = threading.Thread(target=self.sworker)
        self.sworkerThread.daemon = True
        self.sworkerThread.start()

        #"Server time ticker"
        self.tickerThread = threading.Thread(target=self.ticker)
        self.tickerThread.daemon = True
        self.tickerThread.start()

    def rworker(self):
        pass

    def sworker(self):
        pass

    def ticker(self):
        pass
