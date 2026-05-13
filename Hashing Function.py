# -----------======== Imports ========-----------#

# -----------======== Functions ========-----------#
def xor(a, b):
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))


def hash_round(block32, vector32):
    #Split block32 and vector32 into 4 blocks of 8 bits each
    block_A = block32[:8]
    block_B = block32[8:16]
    block_C = block32[16:24]
    block_D = block32[24:32]

    vector_1 = vector32[:8]
    vector_2 = vector32[8:16]
    vector_3 = vector32[16:24]
    vector_4 = vector32[24:32]

    # Rotate the bits
    def rotate_3(bits):
        return bits[3:] + bits[:3]

    # XOR the block with the previous block
    xor_block_A = xor(block_A, vector_1)
    xor_block_B = xor(block_B, rotate_3(xor_block_A))
    xor_block_C = xor(block_C, rotate_3(xor_block_B))
    xor_block_D = xor(block_D, rotate_3(xor_block_C))

    # XOR the first XOR with the inserted vector
    xor2_block_B = xor(xor_block_B, vector_2)
    xor2_block_C = xor(xor_block_C, vector_3)
    xor2_block_D = xor(xor_block_D, vector_4)

    next_round = xor2_block_D + xor_block_A + xor2_block_B + xor2_block_C

    return next_round


def padding(data):
    # Pad the data to be a multiple of 128 bits
    if len(data) % 128 != 0:
        data += '1'
    while len(data) % 128 != 0:
        data += '0'
    return data


def algorithm_y(binary128, vector32):
    #Split into 4 blocks
    block_A = binary128[:32]
    block_B = binary128[32:64]
    block_C = binary128[64:96]
    block_D = binary128[96:128]

    # Initial round
    hash_0 = hash_round(block_A, vector32)
    hash_A = hash_round(block_A, hash_0)
    for rounds in range(28):
        hash_A = hash_round(block_A, hash_A)

    hash_B = hash_round(block_B, hash_A)
    for rounds in range(29):
        hash_B = hash_round(block_B, hash_B)

    hash_C = hash_round(block_C, hash_B)
    for rounds in range(29):
        hash_C = hash_round(block_C, hash_C)

    hash_D = hash_round(block_D, hash_C)
    for rounds in range(29):
        hash_D = hash_round(block_D, hash_D)

    return hash_D


def main():
    print("Welcome to Hashing Algorithm Y\n")
    print("This is a simple hashing algorithm that uses XOR and bit rotation to hash data into a 8-hex value.\n")
    x = input("Enter data to be hashed:\n")

    # Convert the input to binary
    x_bytes = x.encode('utf-8')
    x_binary = ''.join(format(byte, '08b') for byte in x_bytes)

    if len(x_binary) % 128 != 0:
        x_binary = padding(x_binary)

    data128 = []
    for i in range(0, len(x_binary), 128):
        data128.append(x_binary[i:i + 128])

    seed_hex = 0xB63A56A8
    seed = format(seed_hex, '032b')


    #First data block using the seed
    binary128 = data128.pop()
    hash32 = algorithm_y(binary128, seed)

    #Subsequent data blocks using the previous hash
    while data128:
        binary128 = data128.pop()
        hash32 = algorithm_y(binary128, hash32)

    print(f'The hash of this data is: {int(hash32, 2):08x}')


main()







