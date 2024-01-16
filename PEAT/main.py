# from gps3 import gps3
# import RPi.GPIO
import random
# import digitalio
# import board
# import busio
# import adafruit_rfm9x
import rsa # pip install rsa

def encrypt(msg):
    # with open("/Users/anmolsaini/.ssh/peat.pub","r") as key_pub_file:
    #     key_pub = key_pub_file.read()
    #     encoded_msg = msg.encode('utf8')
    #     encrypted_msg = rsa.encrypt(encoded_msg, key_pub)
    #     print(encrypted_msg)

    fKey = open('/Users/anmolsaini/.ssh/peat.pub.pem','rb')
    #publicKey = rsa.PublicKey.load_pkcs1_openssl_pem(fKey.read())
    publicKey = rsa.PublicKey.load_pkcs1(fKey.read())
    encoded_msg = msg.encode('utf8')
    encrypted_msg = rsa.encrypt(encoded_msg, publicKey)
    print(encrypted_msg)
    return encrypted_msg

def decrypt(encrypted_msg):
    fKey = open('/Users/anmolsaini/.ssh/peat', 'rb')  # Assuming private key file is 'peat'
    privateKey = rsa.PrivateKey.load_pkcs1(fKey.read())
    decrypted_msg = rsa.decrypt(encrypted_msg, privateKey).decode('utf8')
    print(decrypted_msg)
    return decrypted_msg

#print("hello world")
enc_msg = encrypt("hello")
dec_msg = decrypt(enc_msg)