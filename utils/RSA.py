
# _*_ coding: utf-8 _*_
# @Time     : 2018/9/27 00:27
# @Author   : Ole211
# @Site     : 
# @File     : baike_crawl.py    
# @Software : PyCharm

from math import sqrt
import time

def return_ascii(s):
    if ord(s) < 100:
        return '000' + str(ord(s))
    elif ord(s) >= 100 and ord(s) < 200:
        return '00' + str(ord(s))
    elif ord(s) >= 10000 and ord(s) < 100000:
        return str(ord(s))
    
P = 223
Q = 157
N = P * Q
M = (P-1) * (Q-1)  
public_key = 11
private_key = []
for i in range(25000, 800000):
    if i*public_key % M == 1:
        private_key.append(i)

# 明文加公钥加密为密文
def encode(msg, public_key, N):
    s = list(map(return_ascii, msg))
    secret = '%'.join([str(int(i)**public_key % N) for i in s])
    return secret

# 密文加私钥解密为明文
def decode(secret, private_key, N):
    if "%" in secret:
        ss = [int(i)**private_key % N for i in secret.split('%')]
        if ss:
            msg = ''.join(chr(int(i)) for i in ss)
            return msg
    return None

if __name__ == '__main__':
    msg = 'poo..1475'
    secret = encode(msg, public_key, N)
    with open('d:/private_key.txt', 'w') as f:
        f.write(secret)
    print('保存密文成功')