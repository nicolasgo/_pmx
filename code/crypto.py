'''
 module for encrypting elements
   
 Copyright (c) 2014, 2015, Pragmex Inc, All Right Reserved
 http://pragmex.com/
    
'''

import hashlib

saved = {}
rsaved = {}  # a reverse dictionary can be used to lookup original msisdn from hashed ids


def xx_msisdn(msisdn):
    if type(msisdn)==int:
        msisdn=str(msisdn)
    if not saved.has_key(msisdn):
        try:
            m = hashlib.md5()

            m.update(msisdn)
            mh = '%.12s'%(m.hexdigest()[10:30])
            
            saved[msisdn]=mh
            rsaved[mh]=msisdn

        except:
            print type(msisdn),msisdn

    return saved[msisdn]
    

def xx_ip(ip_address):
    y='1.2.3.4'
    try:
        parts=[]
        extra=0
        for elem in ip_address.split('.'):
#            print elem,int(elem)^(0xA8+extra),int(elem)^(0xA8+extra*7)
            parts.append(int(elem)^(0xA8+extra*7))
            extra +=1
        y=''
#        print ip_address,parts[::-1]
        for p in parts[::-1]:
            y+='%x.'%(p)
#            print y
        
        y=y[:-1] # remove the last '.'

    except:
        print type(ip_address),ip_address

    return y

