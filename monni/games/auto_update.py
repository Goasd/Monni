import threading
import time

class AutoUpdate:

    def __init__(self, servers, load):
        self.servers = servers
        self.load = load
        self.process = None

    def start(self):
        thread = threading.Thread(target=self.update_servers, args=())
        thread.daemon = True
        thread.start()

    def stop(self):
        if self.process is not None:
            self.process.terminate()

    def update_servers(self):
        while True:
            time.sleep(120)
            for server in self.servers:
                self.load.update_server_data(server)