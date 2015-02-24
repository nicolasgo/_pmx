'''module for handling encryption
   Created by Nicolas Gosselin
'''

import hashlib

saved = {}
rsaved = {}  # a reverse dictionary can be used to lookup original msisdn from hashed ids

def xx(x):
    if not saved.has_key(x):
        try:
            m = hashlib.md5()
            m.update(x)
            mh = '%.12s'%(m.hexdigest()[10:30])
            saved[x]=mh
            rsaved[mh]=x

        except:
            print type(x),x

    return saved[x]


