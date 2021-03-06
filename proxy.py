#-*- coding: UTF-8 -*- 
import sys
import socket
import threading


def hexdump(src,length=16):
    result=[]
    digits=4 if isinstance(src,unicode) else 2


    for i in xrange(0,len(src),length):
        s=src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits,ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append( b"%04X %-*s %s" % (i,length*(digits+1),hexa,text))
    print b'\n'.join(result)



def receive_from(connection):
    buffer=""

     #设置超时时间  2s
    connection.settimeout(2)
    try:
            #持续读取数据直到没有数据或超时
        while True:
            data=connection.recv(4096)
            if not data:
                break
            buffer +=data

    except:
        pass

        return buffer

#对目标是remout_host的请求进行修改
def request_handler(buffer):
    #执行包修改
    return buffer


#对目标是local_host的请求进行修改
def response_handler(buffer):
    #执行包修改
    return buffer

    







def proxy_handler(client_socket,remote_host,remote_port,receive_first):

    #连接远程主机
    remote_socket=socket.socket(socket.AF_INET,)
    remote_socket.connect((remote_host,remote_port))
    #接受远程主机发来的数据
    if receive_first:
        remote_buffer=receive_from(remote_socket)
        hexdump(remote_buffer)

        #发送给响应处理函数
        remote_buffer=response_handler(remote_buffer)

        #如果有数据发送给本地客户端 发送
        if len(remote_bufffer):
            print "[<==] Sending %d bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)
    while True:
        local_buffer=receive_from(client_socket)

        if len(local_buffer):
            print "[==>] Received %d bytes from localhost." % len(local_buffer)
            hexdump(local_buffer)
            #进行消息处理
            local_buffer=request_handler(local_buffer)

            #向远程主机发送数据
            remote_socket.send(local_buffer)
            print "[==>] Send to remote"

        #接受响应数据
        remote_buffer=receive_from(remote_socket)
        if len(remote_buffer):

            print "[<==] Received %d bytes from remote." % len(remote_buffer)
            hexdump(remote_buffer)

            # 发送到处理函数
            remote_buffer=response_handler(remote_buffer)
            # 将响应发送给本地
            client_socket.send(remote_buffer)
            print "[<==] Sent to loaclhost."

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print "[*] No more data.Closeing connections."
            break






            
def server_loop(local_host,local_port,remote_host,remote_port,receive_first):

    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((local_host,local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host,local_port)

        print "[!!] Check for other listening sockets or correct permissions."

        sys.exit(0)

    print "[*] Listening on %s:%d" % (local_host,local_port)

    server.listen(5)

    while True:
        client_socket,addr = server.accept()

        #打印连接信息

        print "[==>] Received incoming connection from %s:%d" % (addr[0],addr[1])

        #开启新线程与远程主机通信
        proxy_thread=threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first))
        proxy_thread.start()


def main():
    if len(sys.argv[1:])!=5:
        print "Usage: ./proxy.py [local_host] [local_port] [remote_host] [remote_port] [receive_first]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)

    #设置本地监听参数
    local_host=sys.argv[1]
    local_port=int(sys.argv[2])

    #设置远程目标参数
    remote_host=sys.argv[3]
    remote_port=int(sys.argv[4])

    #设置receive_first
    receive_first=sys.argv[5]

    if "True" in receive_first:
        receive_first=True
    else:
        receive_first=False

    #设置监听socket
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)



main()

    



















    
