from M2Crypto import RSA 



msg = 'cclpwnybz'

rsa_pub = RSA.load_pub_key('rsa.pem')

#rsa_pri = RSA.load_key('rsa_pri.pem')

print '*************************************************************'

print '公钥加密，私钥解密'

ctxt = rsa_pub.public_encrypt(msg, RSA.pkcs1_padding)

ctxt64 = ctxt.encode('base64')

print ('密文:%s'% ctxt64)
