#Seed Value
seed = 0

#Pseudo-Random Number Generator (PRNG) Function
def prng(x):
    A = 293
    B = 105
    m = 2**32
    return (A * x + B) % m

#Steam Cipher Function
def steam_cipher(text, seed):
    result = ""
    x = seed
    for char in text:
        x = prng(x)
        cipher_char = chr(ord(char) ^ (x % 256))
        result += cipher_char
    return result

#Encryption Function
def encrypt():
    plaintext = input("Enter message to encrypt: ")
    print("Encryption in progress...")
    ciphertext = steam_cipher(plaintext, seed)
    print("Encrypted message: " + ciphertext)
    return

#Decryption Function
def decrypt():
    ciphertext = input("Enter message to decrypt: ")
    print("Decryption in progress...")
    plaintext = steam_cipher(ciphertext, seed)
    print("Decrypted message: " + plaintext)
    return

#Main
while True:
    print("Steam Cipher Main Menu")
    print("1. Encryption")
    print("2. Decryption")
    print("3. Exit")
    task = input("Enter task (1-3): ")
    if task == "1":
        encrypt()
    elif task == "2":
        decrypt()
    elif task == "3":
        print("Exiting program...")
        break
    else:
        print("Invalid input, try again.")