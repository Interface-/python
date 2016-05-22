# -*- coding: cp936 -*-
import random
import math
import string

def prime(min,max):
    list=[]
    for i in range(min,max):
        flag=0
        
        for j in range(2,i):
            #print "j:%d"%j
            if i%j==0:
                flag=1
                break
        if flag==0:
            list.append(i)
           # print "i:%d"%i
    print list
    prime_=random.choice(list)
    print prime_
    return prime_


def Key():
    global private_A
    global private_B
    global private_C
    global public_A
    
    global public_B
    
    private_A=prime(1,100);
    private_B=prime(1,100);
    print private_A,private_B
    public_A=private_A*private_B
    ol=(private_A-1)*(private_B-1)
    print "key_len:%d\nol:%d\n" % (public_A,ol)
    private_C=1
    #for private_C in range(1,ol):
    while(1):
        private_C=private_C+1
        if private_C%ol and ol%private_C:
            break
    # ex+ol y=1'''
    '''e=17
    ol=3120'''
    public_B=1
    flag=0
   # for public_B in range(1,3000):
    while(1):
        public_B=public_B+1
        if (private_C*public_B)%ol == 1:
            y=(1-private_C*public_B)/ol
            print "public_B:%d\ny:%d\n"%(public_B,y)
            flag=1
            break

    
    if flag == 0:
        print "error"
    else:
        print "私钥：%d,%d,%d\n"%(private_A,private_B,private_C)
        print "公钥：%d,%d\n"%(public_A,public_B)
        
    


def RSA():
    global RSA_M
    Key()
    message_char=raw_input("Please input message:\n")
    #message_char='a'
    message=ord(message_char)
    #print int(message_char)
    
   # message=int(message_char)
    print "a:%d"%message
    RSA_M=message
    for i in range(1,public_B):
        RSA_M=RSA_M*message
    RSA_M=RSA_M%public_A
    print "密文：%d"%RSA_M
    UNRSA()
    '''
    message=733
    print "a:%d"%message
    RSA_M=message
    for i in range(1,3):
        RSA_M=RSA_M*message
    RSA_M=RSA_M%3337
    print "密文：%d"%RSA_M'''

def UNRSA():
    print "正在解密...."
    message=RSA_M
    
    '''while(((public_B*d)%public_A)!=1):
        d=d+1'''
    print "private_C:%d\n"%private_C
    print "message:%d\n"%message
    print "public_A:%d\n"%public_A
    for o in range(1,private_C):
        message=message*RSA_M
    message=message%(public_A)
    print message
    '''message=chr(message)
    print "解密结果:%c\n"%message'''
        

if __name__ == '__main__':

    RSA()

