# UnionCardinality
This repo contains a demo program for a paper submission for 2020 AMIA Informatics Summit, entitled "Toward a More Accurate Accrual for Clinical Trials: Joint Cohort Discovery Using Bloom Filters and Homomorphic Encryption". 

To run this demo, download the python script PhaseTwoSimulation.py and two synthetic data files institution1.txt and institution2.txt. These two synthetic data files each contains 1800 and 1500 pseudo identifiers, but they have 300 pseudo identifiers in common. The true value for the union cardinality here is 3000 (1800 + 1500 - 300).

The objective of the python script is to simulate the secure two party protocol described in the above paper submission. At the end of the computation, the estimated value for the union cardinality is output. 

# Dependencies  
pip install numpy  
pip install hashlib  
pip install pycryptodome  

# Parameter Tweaks
Bloom filter size (m): default to 2^16. Bigger Bloom filter makes the estimation more accurate. One can compare the estimation accuracy between 2^16 and 2^20 Bloom filter. To change to 2^20, change the hex_digits to 5. As we indicated in the paper, when k = 30, m = 2^16 gives an average abosulte error ~10, whereas k = 30, m = 2^16 gives an average abosulte error less than 2.

k: the function of hash functions.

random_salt: this gives different salt to the SHA512. To vary the simulations, try different values of "randomvalue", "random value", "random  value", "random   value". Using fixed k and m, these simulation produce estimation results at a certain accuracy level.


# References  
https://pypi.org/project/numpy/  
https://pypi.org/project/hashlib/  
https://pypi.org/project/pycryptodome/  
