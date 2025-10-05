import argparse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

def get_args():
    parser = argparse.ArgumentParser(description='RSA Encryption and Decryption')
    parser.add_argument('--mode', choices=['keygen', 'test'])
    parser.add_argument('--key_length', type=int, default=4096, help='Key length (in bits)')
    parser.add_argument('--output_dir', type=str, default='.', help='Output  directory')
    parser.add_argument('--key_dir', type=str, default='.', help='Where the key is stored')
    parser.add_argument('--message_dir', type=str, default='message.txt', help='Where the key is stored')
    args = parser.parse_args()
    return args

def key_gen(key_length, output_dir):
    # TODO starts
    # TODO ends
    f = open(os.path.join(output_dir, 'public.pem'), 'wb')
    f.write(key.publickey().exportKey('PEM'))
    f.close()
    f = open(os.path.join(output_dir, 'private.pem'), 'wb')
    f.write(key.exportKey('PEM'))
    f.close()

def load_key(key_dir):
    # TODO starts
    # TODO ends
    return key

def test(message_dir, key_dir):

    message = open(message_dir, 'rb').read()
    print('original text:')
    print(message)
    print('\n')
 
    key_pub = load_key(os.path.join(key_dir, 'public.pem'))
    cipher = PKCS1_OAEP.new(key_pub)
    ciphertext = cipher.encrypt(message)
    print('cipher text:')
    print(ciphertext)
    print('\n')

    key_prv = load_key(os.path.join(key_dir, 'private.pem'))
    cipher = PKCS1_OAEP.new(key_prv)
    message = cipher.decrypt(ciphertext)
    print('After decryption:')
    print(message)


def main():
    args = get_args()
    if args.mode == 'keygen':
        key_gen(args.key_length, args.output_dir)
    elif args.mode == 'test':
        test(args.message_dir, args.key_dir)

if __name__ == '__main__':
    main()

