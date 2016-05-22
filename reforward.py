#-*- coding: UTF-8 -*- 
import sys
import threading
import paramiko
from optparse import OptionParser
import getpass






def handler(chan,host,port):
    sock=socket.socket()
    try:
        sock.connect((host,port))
    except Exception as e:
        verbose('Forwarding request to %s:%d failed: %r' % (host,port,e))
        return
    print('Connected! Tunnel open %r -> %r -> %r'% (chan.origin_addr,chan.getpeername(),(host,port)))

    while True:
        r,w,x=select.select([sock,chan],[],[])
        if sock in r:
            data=sock.recv(1024)
            if len(data)==0:
                break
            chan.send(data)
        if chan in r:
            data=chan.recv(1024)
            if len(data)==0:
                break
            sock.send(data)
    chan.close()
    sock.close()
    print
    ('Tunnel closed from %r' % (chan.origin_addr,))
        











def reverse_forward_tunnel(server_port,remote_host,remote_port,transprot):
    transport.request_port_forward('',server_port)
    while True:
        chan=transport.accept(1000)
        if chan is None:
            continue
        thr=threading.Thread(target=handler,args=(chan,remote_host,remote_port))

        thr.setDaemon(True)
        thr.start()








def main():
    #options,server,remote=parse_options()
    password="toor"
    #if options.readpass:
     #   password=getpass.getpass('Enter SSH password: ')
    
    server0="192.168.157.130"
    optionsport=int(8080)
    server1=int(22)
    username="root"
    remote0="192.168.1.104"
    remote1=int(80)
    client=paramiko.SSHClient()
    #client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('Connecting to ssh host %s:%d ...' % (server0,server1))
    try:
        #client.connect(server0,server1,'root',key_filename="C:\\Users\\nibir\\Desktop",look_for_keys='id_rsa',password='toor')
         client.connect(server0,username='root',password='toor')
    except Exception as e:
        print('*** Failed to connect to %s:%d: %r' % (server0,server1,e))
        sys.exit(1)

    print('Now forwarding remote port %d to %s:%d ...' % (optionsport,remote0,remote1))

    try:
        reverse_forward_tunnel(optionsport,remote0,remote1,client)
    except KeyboardInterrupt:
        print ('C-c: port forwarding stopped.')
        sys.exit(0)
main()
