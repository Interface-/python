from M2Crypto import RSA 



msg = 'cclpwnybz'

rsa_pub = RSA.load_pub_key('rsa.pem')

#rsa_pri = RSA.load_key('rsa_pri.pem')

print '*************************************************************'

print '��Կ���ܣ�˽Կ����'

ctxt = rsa_pub.public_encrypt(msg, RSA.pkcs1_padding)

ctxt64 = ctxt.encode('base64')

print ('����:%s'% ctxt64)
