#import libraries
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util import Counter
from Crypto import Random
from binascii import hexlify

#this is only used for CTR mode
# Set up the counter with a nonce and initial value.
ctr_iv = int(hexlify(Random.new().read(AES.block_size)), 16)
#print('CTR IV (int): {0}'.format(ctr_iv))
ctr_encrypt_counter = Counter.new(128, initial_value=ctr_iv)
ctr_decrypt_counter = Counter.new(128, initial_value=ctr_iv)

#Apply padding
def pad(s, bs=32):
    return bytes(s + (16 - len(s) % 16) * chr(16 - len(s) % 16), 'utf-8')

def unpad(s):
        return s[0:-ord(s[-1:])]
    
    
def encryption(key, raw, iv, mode):
    data = pad(raw)
    if mode != AES.MODE_CTR and mode != AES.MODE_ECB:
        cipher = AES.new(key,mode,iv)
    if mode == AES.MODE_ECB:
        cipher = AES.new(key,mode)
    else:
        cipher = AES.new(key,AES.MODE_CTR,counter=ctr_encrypt_counter)
        
    return cipher.encrypt(data)

def decryption(key, ctext,iv,mode):
    if mode != AES.MODE_CTR and mode != AES.MODE_ECB:       
        cipher = AES.new(key,mode,iv)
    if mode == AES.MODE_ECB:
        cipher = AES.new(key,mode)
    else:
        cipher = AES.new(key,AES.MODE_CTR,counter=ctr_decrypt_counter)
        
    return unpad(cipher.decrypt(ctext))  
   
#generate 128bits-16 bytes key and iv
k = ("Network Security").encode('utf-8')
iv = ("1234"*4).encode('utf-8')

#plaintext is a character string of 5 blocks of 16 bytes 
plaintext = "Monash_FIT3031**"*5

print("Plaintext")
print(plaintext)

ciphertext= encryption(k,plaintext,iv,AES.MODE_CTR)

print("Ciphertext in hex mode")
print(ciphertext)

content= decryption(k,ciphertext,iv,AES.MODE_CTR).decode("utf-8")
print("Content after decryption")
print(content)