# -*- coding: cp936 -*-
import os
from scapy.all import *

pkts=[]
count=0
pcapnum=0
filename=''

def test_dump_file(dump_file):
    print "Testing the dump file..."
   
    if os.path.exists(dump_file):
        print "dump fie %s found." %dump_file
        pkts=sniff(offline=dump_file)
        count = 0
        while (count<=2):
            print "----Dumping pkt:%s----" %dump_file
            print hexdump(pkts[count])
            count +=1
    else:
        print "dump fie %s not found." %dump_file

def write_cap(x):
    global pkts
    global count
    global pcapnum
    global filename
    pkts.append(x)
    count +=1
    if count ==3:
			
			pcapnum +=1
			pname="pcap%d.pcap"%pcapnum
			wrpcap(pname,pkts)
			filename ="./pcap%d.pcap"%pcapnum
			test_dump_file(filename)
			pkts=[]
			count=0
        
  


if __name__=='__main__':
    print "Start packet capturing and dumping ..."
    sniff(filter="dst net 127.0.0.1 and tcp",prn=write_cap)    #PBF过滤规则
   
        
