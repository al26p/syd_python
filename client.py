# coding: utf-8

import socket
import sys


def main(argv):
    print(argv)
    UDP_IP_ADDRESS = "127.0.0.1"
    if 'ip' in argv:
        UDP_IP_ADDRESS = str(argv.get('ip'))


    UDP_PORT_NO = 8091
    if 'port' in argv:
        UDP_PORT_NO = str(argv.get('port'))

    Message = "SYN"
    print(UDP_IP_ADDRESS)

    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    clientSock.sendto(Message.encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
    data, addr = clientSock.recvfrom(1024)
    print(data)


if __name__ == "__main__":
    arg_names = ['command', 'ip', 'port']
    args = dict(zip(arg_names, sys.argv))
    main(args)
