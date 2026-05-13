import random
import math
import secrets


# Modular exponentiation function used in the Miller-Rabin primality test, encryption, decryption.
def power(base, exponent, modulus):
    # Initialise power
    result = 1
    # Modulo the base
    base = base % modulus
    while exponent > 0:
        # If exponent is odd multiply base with a result
        if (exponent % 2) == 1:
            result = (result * base) % modulus

        # Divide exponent by 2
        exponent = exponent >> 1
        # Square the base
        base = (base * base) % modulus

    return result


def mrtest(d, n, r):
    # Pick a random base number from 2 to n - 2 to test our prime
    a = random.randint(2, n - 2)

    # Calculate a^((n - 1)/2) % n
    result = power(a, d, n)
    if result == 1 or result == n - 1:
        return True
    for _ in range(r - 1):
        result = (result * result) % n
        if result == n - 1:
            return True
        if result == 1:
            return False
    return False

    return False

def is_prime(integer):
    if integer <= 1 or integer ==4:
        return False
    if integer <= 3:
        return True

    odd_number = integer - 1
    r = 0
    while odd_number % 2 == 0:
        odd_number //= 2
        r += 1
        print(f"\nTesting n = {integer}")
        print(f"n - 1 = 2^{r} * {odd_number}")

# Repeated test for accuracy
    for i in range(5):
        if mrtest(odd_number, integer, r) == False:
            print(f"{integer} is composite!\n")
            return False

    print(f"{integer} maybe prime!\n")
    return True

def generate_prime():

    while True:
        p = random.randint(101, 9999)
        if is_prime(p):
            return p

def mod_inverse(e, phi):
    if math.gcd(e, phi) > 1:
        return print("Inverse doesn't exist")

    for d in range(1, phi):
        if ((e % phi) * (d % phi)) % phi == 1:
            return d

    return print("Inverse doesn't exist")

def keys():

    # Get 2 primes
    p = generate_prime()
    q = generate_prime()

    while p == q:
        q = generate_prime()

    # Calculate n
    n = p * q

    # Calculate phi
    phi = (p - 1) * (q - 1)

    # Pick public exponent e
    e = 0
    while math.gcd(e, phi) != 1:
        e = random.randrange(3, phi - 1)

    # Determine d if d * e ≡ 1 % phi (multiplicative inverse of e mod phi)
    d = mod_inverse(e, phi)

    if (d * e) % phi != 1:
        raise ValueError("Modular inverse failed, key invalid.")

    else:
        print(f"Primes p = {p}, q = {q}")
        print(f"n = {n}")
        print(f"phi(n) = {phi}")
        print(f"Public key (n, e) = ({n}, {e})")
        print(f"Private key (d) = ({d})")


    return e, d, n

def encrypt(plain_text, e, n):
    return power(plain_text, e, n)


def decrypt(cipher_text, d, n):
    return power(cipher_text, d, n)


def stream_key(n):
    bit_length = n.bit_length() - 1
    return secrets.randbits(bit_length)


def main():

    e, d, n = keys()

    print (f"Public key (n, e) = ({n}, {e})")
    print (f"Private key (d) = ({d})")


    K = stream_key(n)
    print(f'Stream Cipher Key K: {K}')

    encrypted = encrypt(K, e, n)

    decrypted = decrypt(encrypted, d, n)

    print(f'Encrypted: {encrypted}')
    print(f'Decrypted: {decrypted}')

if __name__ == "__main__":
    main()








