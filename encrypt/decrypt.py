# pip uninstall crypto
# pip uninstall pycryptodome
# pip install pycryptodome

import Crypto.Cipher.AES as AES
import os

def fillPadding(s):
    m = len(s) % 16
    if(m != 0):
        s += (16 - m) * '\x00'
    return s.encode()

def cleanZero(s):
    r = s.decode().replace('\x00', '')
    return r

print("enter encrypted filename: ", end = '\0')
filename = input().replace(' ', '')

if(os.path.exists(filename)):
    f = open(filename, "rb")
    en_text = f.read()
    f.close()
    print("enter password: ", end = '')
    pswd = input()
    aes = AES.new(fillPadding(pswd), AES.MODE_ECB)
    de_text = cleanZero(aes.decrypt(en_text))
    poz = filename.rfind('/')
    if(poz != -1):
        temp = list(filename)
        temp.insert(poz + 1, "decrypted_")
        s = ''
        for i in temp:
            s += i
        filename = s
    else:
        filename = "decrypted_" + filename
    f = open(filename, "w")
    f.write(de_text)
    f.close()
