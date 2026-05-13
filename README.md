

This repository includes:

- Implementations of symmetric and asymmetric encryption algorithms
- Examples of design layouts
- Hashing and message authentication codes
- Key derivation functions
- Digital signatures
- Other cryptographic utilities

Block Cipher X:

This block cipher has a block size of 64 bits and incorporates elements of substitution, permutation and key addition run through multiple rounds. 
It uses output feedback as its mode of operation, the initial vector (IV) injection has confusion inherently built in as well as avoiding bit error propagation in its ciphertext.
The algorithm uses a key size of 64 bits, it incorporates a key scheduling system that sends 16 bits into each round of encryption.

It works by first splitting the key in half and conducts a bitwise rotation once to the right and concatenates them back together. 
This becomes the new key in the next round. It will then go into a permuted choice module where every 4th bit is selected to be used for that round. 
There are 32 rounds of encryption in total with this algorithm as the key scheduling system allows for 32 unique keys before it wraps around to become the starting key, as such the decryption is made easy as it uses the same key to both encrypt and decrypt. 
It works with a random initial vector (IV) of 64 bits that is generated as the seed to add initial confusion, this is split into 4 blocks of 16 bits each. 

The first 16 bit block on the far left is put through an S-Box, This represents the substitution part of the algorithm.
Within the S-box the 16 bits are split in half and each 8 bit block is inputted into a lookup table, this design borrows the table from the AES algorithm as it is more resistant to cryptanalysis and difficult to inverse, introducing non-linearity and a good level of diffusion.
The output bits of the S-box are concatenated together and XOR’d with a 16 bit round key, This XOR result feeds into 2 places, first into the next round of encryption, shifting 1 row block right in the second round as well as becoming the new subkey to be XOR’d with the second block of 16 bits in the first round. The XOR results of this are similarly, shifted right by one and fed into the 3rd block of the second round as well as being used to XOR with the final 4th block of 16 bits, the final block wraps around and becomes the first block in the second round. 


Hash Algorithm K:

This algorithm breaks 128 bits of data into 4 blocks, which each ran through a hashing round 30 times, after the use of an initial seed the output of each round is fed into the next, with the final hash of the block being used as the seed for the next. 
The algorithm uses bitwise rotation as well as XOR operations with both previous XOR outputs as well as a vector in order to generate more diffusion.

It is able to take an input of any length by splitting the data into 128 bits, storing each block in a list and including padding of ‘1’ + ‘0’s for blocks not divisible by 128 it feeds the hash result of each block into the next. 
The hash output is also short and has a fixed length of 32 bits regardless of input. It is efficient as it only used basic XOR and bitwise operations. 

Message Authentication Code:

The MAC created is from block cipher X ran in cipher block chaining mode (CBC) to create a MAC. 
It takes a symmetric 64 bit key and a static IV to encrypt a message and returns the final block of ciphertext to be used as a MAC of the message.

