import secrets
import time

def iv_generator():
    return ''.join(str(secrets.randbits(1)) for _ in range(64))

def key_chain():
    keys64 = []
    subkeys16 = []
    
    # Generate the starting key
    master_key = ''.join(str(secrets.randbits(1)) for _ in range(64))
    keys64.append(master_key)
    
    def rotate(bits, n):
        return bits[-n:] + bits[:-n]
    
    # Generate the rest of the keys
    for i in range(1, 32):
        prev_key = keys64[-1]
        # Split in half
        left_half = rotate(prev_key[:32], 1)
        right_half = rotate(prev_key[32:], 1)
        # Append to keys64
        keys64.append(left_half + right_half)
    
    # Generate the sub keys by taking every 4th bit
    for key in keys64:
        subkey = ''.join(key[i] for i in range(0, 64, 4))
        subkeys16.append(subkey)
    
    return subkeys16, keys64

def s_box(block16):
    # Convert bit string to integers
    byte1 = int(block16[:8], 2)
    byte2 = int(block16[8:], 2)
    # Get the row and column from s_box
    row1, col1 = (byte1 >> 4) & 0x0F, byte1 & 0x0F
    row2, col2 = (byte2 >> 4) & 0x0F, byte2 & 0x0F
    # Substitute the bytes using lookup table
    sub_byte1 = lookup_table[row1][col1]
    sub_byte2 = lookup_table[row2][col2]
    # Convert back to bit string
    return format(sub_byte1, '08b') + format(sub_byte2, '08b')

lookup_table = [
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
]


def encryption_round(newblock64, subkeys16, round_num):
    # Split the block into 4x16 bit blocks
    block0 = newblock64[:16]
    block1 = newblock64[16:32]
    block2 = newblock64[32:48]
    block3 = newblock64[48:64]
    
    # Put the first block into the s_box
    s_block0 = s_box(block0)
    # XOR the s_box output with the sub_key
    round_key = subkeys16[round_num]
    xor_block0 = xor(s_block0, round_key)
    # Chain XOR
    xor_block1 = xor(xor_block0, block1)
    xor_block2 = xor(xor_block1, block2)
    xor_block3 = xor(xor_block2, block3)
    # Put the blocks back together with xor_block3 in front
    return xor_block3 + xor_block0 + xor_block1 + xor_block2

def string_to_binary(message):
    binary_blocks = []
    binary_string = ''.join(format(ord(char), '08b') for char in message)
    
    # Split into 64-bit blocks
    for i in range(0, len(binary_string), 64):
        block = binary_string[i:i+64]
        # Pad last block if necessary
        if len(block) < 64:
            block = block.ljust(64, '0')
        binary_blocks.append(block)
    
    return binary_blocks

def xor(a, b):
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))

def ofb_mode(bits64, subkeys16):
    for round_num in range(32):
        bits64 = encryption_round(bits64, subkeys16, round_num)
    return bits64

def main():
    print("[!!!!SENDING CLASSIFIED INFORMATION!!!]")
    time.sleep(2)
    print("[Secure Channel Established – Encryption Protocol: BCX-32]")
    time.sleep(2)
    print("[Authentication confirmed]")
    time.sleep(2)
    choice = input("Send Message? (y/n): ")
    
    if choice.lower() == 'y':
        message = input("\nEnter Message to Encrypt:\n ")
        
        iv = iv_generator()
        subkeys16, keys64 = key_chain()
        binary_blocks = string_to_binary(message)
        
        print("Master Key      :", keys64[0])
        print("First Subkey    :", subkeys16[0])
        print("IV                      :", iv)
        
        current_input = iv
        ciphertext_blocks = []
        
        for plaintext_block in binary_blocks:
            keystream = ofb_mode(current_input, subkeys16)
            ciphertext_block = xor(plaintext_block, keystream)
            ciphertext_blocks.append(ciphertext_block)
            current_input = keystream
        
        final_ciphertext = ''.join(ciphertext_blocks)
        print("\nFinal Ciphertext:", final_ciphertext)
    else:
        print("Transmission Cancelled")

if __name__ == "__main__":
    main()