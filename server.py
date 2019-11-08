# coding: utf-8

import socket
import sys
import threading


class Connection(threading.Thread):
    def __init__(self, port, ip, port_set, port_mutex):
        threading.Thread.__init__(self)
        self.port = port
        self.ip = ip
        self.port_set = port_set
        self.lock = port_mutex

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        data, addr = sock.recvfrom(1024)
        print(data)
        sock.close()


def test_port(min, max):
    port_set = set()
    for i in range(min, max):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('127.0.0.1', i))
            port_set.add(i)
        except socket.error:
            print('port bind failed', i)
        finally:
            sock.close()
    return port_set


def main(argv):
    set_lock = threading.Lock()
    port_set = test_port(1000, 9999)
    print(argv)
    UDP_IP_ADDRESS = "127.0.0.1"
    UDP_PORT_NO = 8091

    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

    while True:
        data, addr = serverSock.recvfrom(1024)
        print("Message: ", data.decode('utf-8'))
        if data.decode('utf-8') == 'SYN':
            set_lock.acquire()
            cl_port = port_set.pop()
            set_lock.release()
            conn = Connection(cl_port, addr, port_set, set_lock)
            conn.start()
            tosend = "SYN-ACK"+str(cl_port)
            serverSock.sendto(tosend.encode('utf-8'), (addr, UDP_PORT_NO))
        data, addr1 = serverSock.recvfrom(1024)
        if data.decode('utf-8') == 'ACK' and addr == addr1:
            print('client connected')

    serverSock.close()


if __name__ == "__main__":
    main(sys.argv[1:])
