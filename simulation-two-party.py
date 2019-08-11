# Demo code for a secure two party union cardinality secure computation protocol
# Created for the AMIA 2020 Informatics Summit Paper submission
# Author: Xiao Dong
# Disclaimer: This code is created for a paper demo purpose only, don not copy and use in any production system.

import Crypto
import time
import numpy as np
import time
from Crypto import Random
from Crypto.PublicKey import ElGamal
from Crypto.Random import random

# Construct finite set for the original private sets. 
# We use bloom filters here
# Let's say two private sets mapped to two bloom filters
# m is the bloom filter size
m = 2**6

# Here we generate two bloom filters
bf1 = np.random.randint(2, size=m)
bf2 = np.random.randint(2, size=m)
actual_common0bits = len([i for i, e in enumerate(np.add(bf1, bf2)) if e == 0])
print(actual_common0bits)

key = ElGamal.generate(128, Random.new().read) # Generate ElGamal keys for large prime key.p
# !!!THIS 128 bit IS TOO SHORT FOR SECURITY!!! 
# This is for demo purpose only, as it runs faster
# DO NOT USE IT in practice
# key.p is the mopdulus, key.g is the generater for the cyclic group, key.y public key, key.x private key
# g is the generator for the cyclic group p, whose prime order is >> |bf|
rand_k = random.randint(2,key.p-2)

# SIMULATION BEGINS NOW
# Step Three, party 1 performs the encryption on its bloom filter bits
# And filling use these two cyphertext arrays, r and t 


r_1 = [0]*m
t_1 = [0]*m

t = time.process_time()
for i in range(m):
	rand_k = random.randint(2,key.p-2) # This technically should always be a prime number for security
									   # But for now let's just use a random number
	# iteratively encrypt its filter bits, if the bit == 1 encrypt 1, if bit == 0 encrypt key.p
	msg = key.g if bf1[i] == 0 else 1
	r_1[i] = pow(key.g, rand_k, key.p)
	t_1[i] = (pow(key.y, rand_k, key.p)*msg)%key.p
elapsed_time = time.process_time() - t 
print("Party 1 takes (secs) to encrypt - ")
print(elapsed_time )

# At Party 2 now. 2 performs the encryption of its bloom filter bf2 bits, but only do so for its zero bits
# in the mean time applying the additive homomorphic property of ElGamal, by multiplying the entries together
# The final answer (the number of zero for bf1 union bf2) is now hidden in the exponent 
t = time.process_time()
rand_k = random.randint(2,key.p-2)
r_2 = pow(key.g, rand_k, key.p)
t_2 = pow(key.y, rand_k, key.p)

for i in range(m):
	if bf2[i] == 0: 
		r_2 = (r_2 * r_1[i]) % key.p
		t_2 = (t_2 * t_1[i]) % key.p

elapsed_time = time.process_time() - t 
print("Party 2 takes (secs) to encrypt - ")
print(elapsed_time)

# At Party 1 again, 1 decrypts
t = time.process_time()
dec_r = pow(r_2, key.p-1-key.x, key.p) # This r^-dA 
print("The answer of how many common zero bits is hidden in this exponent!")

# Lookup phase
for i in range(m):
	if (pow(key.g, i, key.p) == (dec_r*t_2)%key.p) : 
		print ("We find out how many common zero bits now!!!")
		print(i)
	
elapsed_time = time.process_time() - t 
print("Party 1 takes (secs) to dencrypt - ")
print(elapsed_time)


