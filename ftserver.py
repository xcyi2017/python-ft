#!/usr/bin/env python
# -*- coding:utf-8 -*-
#。——————————————————————————————————————————
#。
#。  ftserver.py
#。
#。 @Time    : 2018/7/26 00:09
#。 @Author  : ccapton
#。 @Software: PyCharm
#。 @Github  : https://github.com/ccapton
#。 @Email   : chenweibin1125@foxmail.com
#。__________________________________________
import sys,os
import socket
import threading
import argparse

from util import dir_divider,anti_dir_divider,checkfile,formated_time,formated_size,getFileMd5
import time

from language_words import languageSelecter
 
python_version = sys.version
if python_version.startswith('2.'):
    python_version = '2'
elif python_version.startswith('3.'):
    python_version = '3'

divider_arg  = ' _*_ '
right_arrows = '>'*10
left_arrows  = '<'*10

default_data_socket_port = 9997
default_command_socket_port = 9998

COMMAND_CLOSE = '[COMMAND CLOSE]'
COMMANE_MISSION_SIZE = '[COMMAND MISSION_SIZE]'
COMMANE_FILE_INFO = '[COMMAND FILE_INFO]'


class Messenger:
    def __init__(self,socket):
        self.socket = socket
        self.send_debug = False
        self.recev_debug = False

    def send_msg(self,msg):
        if self.socket:
            try:
               self.socket.send(bytes(msg ,encoding='utf8'))
            except Exception as e:
                if self.send_debug:print(dict('ce'))
        elif self.send_debug:print(dict('sin'))
        return self

    def recv_msg(self):
        if self.socket:
            try:
                msg = self.socket.recv(1024)
                return bytes(msg).decode('utf8')
            except Exception as e:
                if self.recev_debug:print(dict('ce'))
        elif self.recev_debug:  print(dict('sin'))
        return None


class CommandThread(threading.Thread):
    def __init__(self, host=None, port=default_command_socket_port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.working = True
        self.dataOn = True
        self.wait_client_flag = True
        self.mission_size = 0
        self.wrote_size = 0
        self.start_time = 0


    def setDataThread(self, server):
        self.dataThread = server

    def run(self):
        self.ssocket = socket.socket()
        self.ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.ssocket.bind((self.host, self.port))
            self.ssocket.listen(1)
            while self.wait_client_flag:
                socket2, addr = self.ssocket.accept()
                self.socket = socket2
                self.socket.send(
                    bytes(dict('ctcs') + self.host + ':' + str(self.port), encoding='utf8'))
                self.commandMessenger = Messenger(self.socket)
                command = self.commandMessenger.recv_msg()
                self.start_time = time.time()

                while command and len(command) and self.working> 0:
                    if command.startswith(COMMANE_MISSION_SIZE):
                        self.mission_size = int(command.split(divider_arg)[1])
                        print(dict('m_s')+': %s' % formated_size(self.mission_size))
                    elif command.startswith(COMMANE_FILE_INFO):
                        self.fileMission = FileMission(self.dataThread.socket, self, self.dataThread.save_path, command)
                        self.fileMission.start()
                        self.dataOn = True
                    elif command == COMMAND_CLOSE:
                        self.dataOn = False
                        time.sleep(0.3)
                        Warning(right_arrows+dict('rcd')+left_arrows)
                    command = self.commandMessenger.recv_msg()
        except OSError:
            warning(dict('cara'))
            self.wait_client_flag = False


    def file_ready(self,fileinfo):
        self.commandMessenger.send_msg(fileinfo + divider_arg +'ready')


    def file_transportover(self,fileinfo):
        self.commandMessenger.send_msg(fileinfo + divider_arg +'file_transport_ok')


    def file_existed(self,fileinfo):
        self.commandMessenger.send_msg(fileinfo + divider_arg + 'file_existed')


    def dir_created(self,fileinfo):
        self.commandMessenger.send_msg(fileinfo + divider_arg +'dir_create_ok')


    def rootdir_create(self,fileinfo):
        self.commandMessenger.send_msg(fileinfo + divider_arg +'rootdir_create_ok')


class Server(threading.Thread):
    def __init__(self,save_path,host = None,port = 9997):
        threading.Thread.__init__(self)
        self.save_path = save_path
        self.host = host
        self.port = int(port)
        self.wait_client_flag = True
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        print(dict('fsd') + self.save_path)


    def setCommandThread(self,commandThread):
        self.commandThread = commandThread

    def run(self):
        self.start_server_socket()
        self.wait_client()


    def start_server_socket(self):
        self.ssocket = socket.socket()
        self.ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.ssocket.bind((self.host, self.port))
            print(dict('shs'))
            print(dict('ra')+' (%s,%d)' % (self.host, self.port))
            print(dict('wfft')+'...')
        except OSError:
            self.wait_client_flag = False
            pass


    def wait_client(self):
        self.ssocket.listen(5)
        while self.wait_client_flag:
            socket, addr = self.ssocket.accept()
            print(dict('nc'), addr)
            try:
                socket.send(bytes(dict('ctds') + self.host + ':' + str(self.port), encoding="utf8"))
                self.socket = socket
                self.commandThread.setDataThread(self)
                self.commandThread.dataOn = True
            except ConnectionResetError as e:
                print(dict('aoc')+'\n')
                print(dict('wfft')+'...')


class FileMission(threading.Thread):
    def __init__(self,socket,commandThread,save_path,fileinfo):
        threading.Thread.__init__(self)
        self.commandThread = commandThread
        self.socket = socket
        self.save_path = save_path
        self.fileinfo = fileinfo
        self.working = True

    def run(self):
        self.handleMission()


    def handleMission(self):
        if self.fileinfo:
            self.filename = self.fileinfo.split(divider_arg)[1]
            self.filename = self.filename.replace(anti_dir_divider(), dir_divider())
            self.file_path = str(self.save_path + dir_divider() + self.filename)
            self.file_path = self.file_path.replace(anti_dir_divider(), dir_divider())
            self.filesize = int(self.fileinfo.split(divider_arg)[2])
        if self.filesize >= 0:
            self.file_md5 = self.fileinfo.split(divider_arg)[3]
            self.write_filedata()
        elif self.filesize == -1:
            if not os.path.exists(self.file_path):
                os.makedirs(self.file_path)
            index = int(self.fileinfo.split(divider_arg)[3])
            dir = self.fileinfo.split(divider_arg)[1]

            if index == 0:
                print(right_arrows+dict('ms')+left_arrows)
                print('-' * 30)
                self.commandThread.rootdir_create(self.fileinfo)
            else:
                self.commandThread.dir_created(self.fileinfo)
            print(dict('cd')+': ' + dir)


    def write_filedata(self):
        print(dict('st')+'%s %s' % (self.filename,formated_size(self.filesize)))

        if getFileMd5(self.file_path) == self.file_md5:
            print(dict('fe') + self.filename)
            self.commandThread.wrote_size += self.filesize
            self.commandThread.file_existed(self.fileinfo)
            downloaded_show = '%s/%s' % (formated_size(self.filesize), formated_size(self.filesize))
            total_downloaded_show = '%s/%s' % (formated_size(self.commandThread.wrote_size),
                                               formated_size(self.commandThread.mission_size))
            current_filename = os.path.basename(self.filename) + ' '
            print(current_filename + downloaded_show + ' | %.2f%%  >>>%s %s | %.2f%%' %
                             (float(self.filesize / self.filesize * 100),
                              dict('total'),
                              total_downloaded_show,
                              float(self.commandThread.wrote_size / self.commandThread.mission_size * 100)) + '\r')
            print('-' * 30)
            if self.commandThread.wrote_size == self.commandThread.mission_size and self.commandThread.wrote_size != 0:
                self.commandThread.wrote_size = 0
                self.commandThread.mission_size = 0
                print(right_arrows + dict('mc') + left_arrows)
                print(dict('cmct') + '%s' % formated_time(time.time() - self.commandThread.start_time))
                print(
                    dict('ra') + ' (%s,%d)' % (self.commandThread.dataThread.host, self.commandThread.dataThread.port))
                print(dict('wfft') + '...')
            return


        if self.filesize == 0:
            with open(self.file_path, 'wb') as f:
                pass
            self.commandThread.file_existed(self.fileinfo)
            return


        self.commandThread.file_ready(self.fileinfo)


        with open(self.file_path,'wb') as f:
            wrote_size = 0
            filedata = self.socket.recv(4096)
            while len(filedata) > 0 :
                tempsize = f.write(filedata)
                wrote_size += tempsize
                self.commandThread.wrote_size += tempsize
                f.flush()
                downloaded_show = '%s/%s' % (formated_size(wrote_size),formated_size(self.filesize))
                total_downloaded_show = '%s/%s' % (formated_size(self.commandThread.wrote_size),
                                                   formated_size(self.commandThread.mission_size))
                current_filename = os.path.basename(self.filename) +' '
                sys.stdout.write(current_filename + downloaded_show +' | %.2f%%  >>>%s %s | %.2f%%' %
                                 (float(wrote_size / self.filesize * 100),
                                  dict('total'),
                                  total_downloaded_show,
                                  float(self.commandThread.wrote_size / self.commandThread.mission_size * 100))+ '\r')
                if wrote_size == self.filesize:
                    print()
                    print(self.filename + ' ' + dict('dd'))

                    self.commandThread.file_transportover(self.fileinfo)

                    if not self.commandThread.dataOn:
                        self.socket.close()
                    break
                else:
                    try:

                        filedata = self.socket.recv(4096)
                    except ConnectionResetError:

                        warning(right_arrows+ dict('rcd')+left_arrows)


            if wrote_size < self.filesize:
                warning(right_arrows+dict('ci')+left_arrows)
                self.dataOn = False
                self.socket.close()
                self.commandThread.socket.close()
                self.commandThread.wrote_size = 0
                self.commandThread.mission_size = 0

            print('-'*30)

            if self.commandThread.wrote_size == self.commandThread.mission_size and self.commandThread.wrote_size != 0:
                self.commandThread.wrote_size = 0
                self.commandThread.mission_size = 0
                print(right_arrows+dict('mc')+left_arrows)
                print(dict('cmct')+'%s' % formated_time(time.time() - self.commandThread.start_time))
                print(dict('ra')+' (%s,%d)' % (self.commandThread.dataThread.host, self.commandThread.dataThread.port))
                print(dict('wfft')+'...')

def warning(text):
    print('[%s] '% dict('wa')+text)

def keyInPort():
    while True:
        temp_port = input(dict('ip'))
        if int(temp_port) > 0 and int(temp_port) != default_command_socket_port:
            return (int(temp_port),True)
        elif int(temp_port) <= 0:
            warning(dict('pmb'))
        elif int(temp_port) == default_command_socket_port:
            warning('Port %d is disabled,please key in other number' % default_command_socket_port)


def keyInSavePath():
    while True:
        filepath = input(dict('pidp'))
        if checkfile(filepath)[0] and checkfile(filepath)[1] == 0:
            return filepath, True
        elif not checkfile(filepath)[0]:
            warning(dict('pde'))
        elif checkfile(filepath)[0] and checkfile(filepath)[1] == 1:
            warning(dict('dpif'))


def keyInHost():
    while True:
        host = input(dict('pit'))
        if len(host) > 0:
            return host, True

def print_author_info(program_name):
    print('*'*60)
    line = 9
    while line > 0:
      if line == 8:
          print('。  %s' % program_name)
      elif line == 6:
          print('。  @ %s: Capton' % dict('Author'))
      elif line == 5:
          print('。  @ %s: http://ccapton.cn' % dict('Blog'))
      elif line == 4:
          print('。  @ %s: chenweibin1125@foxmail.com' % dict('Email'))
      elif line == 3:
          print('。  @ %s: https://github.com/ccapton' % dict('Github'))
      elif line == 2:
          print('。  @ %s: https://github.com/Ccapton/python-stuff/tree/master/filetransporter' % dict('Project'))
      else:
          print('。')
      line -= 1
    print('*'*60)

def dict(key):
    return languageSelecter.dict(key)

if __name__ == '__main__':
    
    if python_version == '2':
        reload(sys)   
        sys.setdefaultencoding("utf-8")

    print_author_info(dict('ftsp'))

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', required=False, help=(dict('tdpw')))
    parser.add_argument('-p', '--port', required=False, help=(dict('tptp')) ,type = int)
    parser.add_argument('-i', '--host', required=False, help=(dict('thtp')),type = str)

    args = parser.parse_args()

    port = default_data_socket_port
    port_ok = True
    host_ok = False
    save_path_ok = False

    save_path = args.dir
    if not save_path:
        save_path = 'downloads'
        if checkfile(save_path)[0] and checkfile(save_path)[1] == 0:
            if not os.path.exists(save_path):os.makedirs(save_path)
        save_path_ok = True
    else:
        if not checkfile(save_path)[0]:
            warning(dict('pde'))
            save_path,save_path_ok = keyInSavePath()
        else:
            save_path_ok = True

    if args.host:
        host = args.host
        host_ok = True
    else:
        host = '0.0.0.0'
        host_ok = True

    if args.port and args.port > 0 :
        port = args.port
        if port == default_command_socket_port:
            warning(dict('po')+' %d %s,%s' % (dict('id'),dict('pki'),default_command_socket_port))
            port , port_ok = keyInPort()
    elif args.port and args.port <=0:
        warning(dict('pmb'))
        port, port_ok = keyInPort()

    if port_ok and host_ok and save_path_ok:
        commandThread = CommandThread(host=host)
        server = Server(save_path=save_path,host = host, port=port)
        server.setCommandThread(commandThread)
        server.start()
        commandThread.setDataThread(server)
        commandThread.start()



