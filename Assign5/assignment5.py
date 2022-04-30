import random
from math import pow
 
a = random.randint(2, 10)
 
def power(num1, num2, num3):
    x, y = 1, num1
    while num2 > 0:
        if num2 % 2 != 0:
            x = (x * y) % num3
        y = (y * y) % num3
        num2 = int(num2 / 2)
    return x % num3
 
def generationKey(q):
    key = random.randint(pow(10, 20), q)
    while greatestCommonDivisor(q, key) != 1:
        key = random.randint(pow(10, 20), q)
 
    return key
 
def greatestCommonDivisor(num1, num2):
    if num1 < num2:
        return greatestCommonDivisor(num2, num1)
    elif num1 % num2 == 0:
        return num2
    else:
        return greatestCommonDivisor(num2, num1 % num2)
 
def encryptingMessage(msg, q, h, g):
    message_encryption = []
    k = generationKey(q)
    s = power(h, k, q)
    p = power(g, k, q)
    for i in range(0, len(msg)):
        message_encryption.append(msg[i])
    print("g^k used : ", p)
    print("g^ak used : ", s)
    for i in range(0, len(message_encryption)):
        message_encryption[i] = s * ord(message_encryption[i])
    return message_encryption, p
 
def decryptingMessage(message_encryption, p, key, q):
    dr_msg = []
    h = power(p, key, q)
    for i in range(0, len(message_encryption)):
        dr_msg.append(chr(int(message_encryption[i]/h)))
    return dr_msg
 
def main():
    msg = 'Samyak loves Networks'
    print("Original Message :", msg)
    q = random.randint(pow(10, 20), pow(10, 50))
    g = random.randint(2, q)
    key = generationKey(q)
    h = power(g, key, q)
    print("g used : ", g)
    print("g ^ a used : ", h)
    message_encryption, p = encryptingMessage(msg, q, h, g)
    dr_msg = decryptingMessage(message_encryption, p, key, q)
    dmsg = ''.join(dr_msg)
    print("Decrypted Message :", dmsg)
 
if __name__ == '__main__':
    main()
