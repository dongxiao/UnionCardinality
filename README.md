# UnionCardinality
This repo contains a demo program for the paper submission to 2020 AMIA Informatics Summit, entitled "Toward a More Accurate Accrual for Clinical Trials: Joint Cohort Discovery Using Bloom Filters and Homomorphic Encryption". 

To run this demo, download the Python script PhaseTwoSimulation.py and two synthetic data files institution1.txt and institution2.txt. There are 1800 and 1500 pseudo-identifiers in each synthetic data file. They constitute the subjects for the two private sets. These two private sets also have 300 pseudo-identifiers in common, which makes union cardinality 3000 (1800 + 1500 - 300).

The objective of this demo is to simulate the secure two party protocol described in the above paper submission. At the end of the computation, the estimated value for the union cardinality is printed. This program is for demo purpose only. To make the demo run fast, we use 256 bit ElGamal key in the discrete log implmentation.

# Dependencies  
$ pip install numpy  
$ pip install hashlib  
$ pip install pycryptodome  

# Parameter Tweaks
m: size of the Bloom filter and default to 2^16.  
Bigger Bloom filter makes the estimation more accurate. Try to compare the estimation accuracy between 2^16 and 2^20 Bloom filters. To change to 2^20, change the hex_digits setting to 5. As we indicated in Figure 1, when k = 30 and m = 2^16, this gives an average abosulte error around 10. When k = 30 and m = 2^20, we see an average absolute error less than 2.

k: the number of hash functions used in the Bloom filter, default to 30.  

random_salt: salt value to add to the SHA-512 hash.  
To vary the simulations, try different values such as "randomvalue", "random value", "random   value". Using fixed k and m, these simulations produce estimation results at a certain accuracy level.

# Run Simulation  
$ cd UnionCardinality  
$ python PhaseTwoSimulation.py  
The estimated union cardinality is printed in the end. Compare the estimated value with true value of 3000.

# References  
https://pypi.org/project/numpy/  
https://pypi.org/project/hashlib/  
https://pypi.org/project/pycryptodome/  
