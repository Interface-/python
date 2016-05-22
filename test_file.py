num=0
while True:
    num+=1
    file_name="pcap%d.pcap" % num
    try:
        fp=open("final.pcap",'ab')
        fp1=open(file_name,'rb')
       
        try:
            print "copt file..."
            str=fp1.readlines()
            fp.writelines(str)
            #fp.close()
            fp1.close()
            fp.close()
            print "copy file:%s ok" % file_name
        except:
            print "read file error"
    
    except:
        break
        print "OPEN file error"

        
