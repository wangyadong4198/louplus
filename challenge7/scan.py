#!/usr/bin/env python3
import socket
import getopt
import sys

def get_args(args):
    host = ''
    port = ''
    try:
        host = args[args.index('--host') + 1]
        port = args[args.index('--port') + 1]
        if len(host.split('.')) != 4:
            print("Parameter Error.")
            return 'ERROR_HOST',0
        if '-' in port:
            port = port.split('-')
        else:
            port = [port,port]
    except:
        print("Parameter Error.")
    return host,[int(port[0]),int(port[1])]

def scan(host,ports):
    open_list = []
    s = socket.socket()
    s.settimeout(0.1)
    for i in range(ports[0],ports[1]+1):
        if s.connect_ex((host,i)) == 0:
            open_list.append(i)
            print('{} open'.format(i))
        else:
            print('{} closed'.format(i))
    s.close()
    return open_list

if __name__ == '__main__':
    host,port = get_args(sys.argv[1:])
    if host == 'ERROR_HOST':
        pass
    else:
        scan(host,port)
