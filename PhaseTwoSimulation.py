# The following python program is prepared as a demo for the AMIA 2020 Informatics Summit paper Submission
# entitled "Toward a More Accurate Accrual for Clinical Trials: Joint Cohort Discovery Using Bloom Filters 
# and Homomorphic Encryption". The ElGamal protocol is currently implemented in discrete log mode.
# 
# This program is for demo purpose only, do not modify and use it in the production system. We choose the 256 bit
# key only and in practice use at least 2048 bit 
# 
# Author: Xiao Dong

import numpy as np
import math
import hashlib
import Crypto
import time
from Crypto import Random
from Crypto.Random import random
from Crypto.PublicKey import ElGamal


# private_set:	Contains the supposedly private information that needs to be kept inside the institution boundaries,
#		here we use two synthetic data set institution1.txt and institution2.txt that contains
#		pseudo individual identifiers.
#
# hex_digits:	The hexdecimal digits are taken from the SHA512 and used as the Bloom filter hash functions. Each hexdecimal
#		digit corresponds to 4 bits. For example, hex_digits of 5 makes the hash function domain 2^20
#				
# m:		Size of the Bloom filter, this value is the same as the domain for the hash functions, such as 2^20 above
#
# k:		The number of hash functions. 
#
# random_salt:	This enables generating SHA512 outputs that are different from plain SHA512

def bloom_filter(private_set, hex_digits, m, k, random_salt):

	# record the one bits (true bits) for the Bloom filter
	one_bit_indices = [] 

	with open(private_set) as f:
		for line in f:
			line = line.strip() + random_salt
			hash_block_start = 0
			for x in range(k):
				hash_block_end = hash_block_start + hex_digits
				partial_hash_bits = hashlib.sha512(line.encode()).hexdigest()[hash_block_start:hash_block_end]
				hash_block_start = hash_block_start + 1
				one_bit_indices.append(int(partial_hash_bits, base=16))
	bf = np.zeros(m)
	bf[one_bit_indices] = 1
	return bf

# Simulates the network hub and institution approvals at the beginning of Phase II
print("*************************************************")
print("Joint cohort discovery requested by Institution I")
print("*************************************************")
print("Network hub approves")
print("Institution 2 approves")

# Simulates the network hub disseminate Bloom filter parameters to the two institutions 
print("\n***********************************************************")
print("Network hub disseminates common Bloom filter parameters")
print("***********************************************************")
hex_digits = 4 # hex_digits = 5 gives 2^20 bits in the Bloom filter, and higher estimation accuracy.
random_salt = "randomvalue" # to vary the simulations try different salt "randomvalue", "random value", "random   value". 
m = 2**(hex_digits*4) 
k = 30 
print("Bloom filter has " + str(m) + " bits")
print("Bloom filter uses " + str(k) + " hash functions\n")

t = time.process_time()
bf1 = bloom_filter('institution1.txt', hex_digits, m, k, random_salt)
print("Institution I Bloom filter generation time: {0:.4f} (seconds)".format(time.process_time() - t))

t = time.process_time()
bf2 = bloom_filter('institution2.txt', hex_digits, m, k, random_salt)
print("Institution II Bloom filter generation time: {0:.4f} (seconds)".format(time.process_time() - t))


# Generate Elgamal key. We chose to use the 256 bit key for demo purpose only. 
print("\n***************************************")
print("ElGamal Key Generation at Institution I")
print("***************************************")
t = time.process_time()
key = ElGamal.generate(256, Random.new().read)
print("ElGamal key generation time: {0:.4f} (seconds)".format(time.process_time() - t))


# At Step 1, Institution 1 performs the encryption on its Bloom filter bits, and generating ciphertext r_1 and t_1
print("\n************************************************")
print("Step 1: Bloom filter Encryption at Institution I")
print("************************************************")
r_1 = [0]*m
t_1 = [0]*m
t = time.process_time()
for i in range(m):
	rand_k = random.randint(2,int(key.p-1)) 
	bit = key.g if bf1[i] == 0 else 1
	r_1[i] = pow(key.g, rand_k, key.p)
	t_1[i] = (pow(key.y, rand_k, key.p)*bit)%key.p
print("Bloom filter encryption time: {0:.4f} (seconds)".format(time.process_time() - t))

print("\nLet us take a look at the first 10 Bloom filter bits before and after encryption")
print("\nBefore\tAfter")
for i in range(10):
	print(str(int(bf1[i]))+"\t"+str(r_1[i])+" "+str(t_1[i]))

# At Step 2, Institution 2 performs the additive homomorphic encryption, and generating ciphertext r_2 and t_2
print("\n************************************************")
print("Step 2: Homomorphic Encryption at Institution II")
print("************************************************")
t = time.process_time()
rand_k = random.randint(2,int(key.p-1))
r_2 = pow(key.g, rand_k, key.p)
t_2 = pow(key.y, rand_k, key.p)

for i in range(m):
	if bf2[i] == 0: 
		r_2 = (r_2 * r_1[i]) % key.p
		t_2 = (t_2 * t_1[i]) % key.p
print("Homomorphic encryption time: {0:.4f} (seconds)".format(time.process_time() - t))

# At Step 3, Institution 1 performs decryption and obtain the number of zero bits in bf1_union_bf2, after that 
# estimate the union cardinality using Equation (4) as explained in the paper.
print("\n***********************************")
print("Step 3: Decryption at Institution I")
print("***********************************")

bf1_zeros = int(m - sum(bf1)) 
bf1unionbf2_zeros = 0 

t = time.process_time()
dec_r = pow(r_2, key.p-1-key.x, key.p) # r^-dA 

# The possible range of bf1unionbf2_zeros is [0, bf1_zeros]
# The group order for the ElGamal key is much larger than m, this ensures the answer is both correct and unique
for i in range(bf1_zeros): 
	if (pow(key.g, i, key.p) == (dec_r*t_2)%key.p) : 
		bf1unionbf2_zero_bits = i
print("Decryption time: {0:.4f} (seconds)".format(time.process_time() - t))

print("We have discovered the number of zero bits in bf1 union bf2: "+str(bf1unionbf2_zero_bits))
estimated_size = (-math.log(bf1unionbf2_zero_bits/m) * m)/k # Equation (4) in the paper
print("Estimated Joint Cohort Size is: {0:.2f}".format(estimated_size))
print("Joint Cohort Discovery Phase II Completes Now.")
