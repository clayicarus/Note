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

print("enter filename: ", end = '')
filename = input().replace(' ', '')

if(os.path.exists(filename)):
    f = open(filename, "r")
    text = f.read()
    f.close()
    print("enter password: ", end = '')
    pswd = input()
    aes = AES.new(fillPadding(pswd), AES.MODE_ECB)
    en_text = aes.encrypt(fillPadding(text))
    poz = filename.rfind('/')
    if(poz != -1):
        temp = list(filename)
        temp.insert(poz + 1, "encrypted_")
        s = ''
        for i in temp:
            s += i
        filename = s
    else:
        filename = "encrypted_" + filename
    f = open(filename, "wb")
    f.write(en_text)
    f.close()
else:
    print("{} open failed".format(filename))
