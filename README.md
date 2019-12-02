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
To vary the simulations, try different values such as "randomvalue", "random&nbsp;value", "random&nbsp;&nbsp;&nbsp;value". Using fixed k and m, these simulations produce estimation results at a certain accuracy level.

# Run Simulation  
$ cd UnionCardinality  
$ python PhaseTwoSimulation.py  
The estimated union cardinality is printed in the end. Compare the estimated value with true value of 3000.

# Run 27K Example  
We also made the java program and the data set we used for the 27K example available here. The implementation uses the following elliptic curve based implementation for additive homomorphic Elgamal system.

https://github.com/lubux/ecelgamal

To set up this example, first follow the installation instruction provided in the github project above. After the installation completes, add the java program for 27K test case into ~/ecelgamal/ecelgamal/src/test/java/ECElGamalTest.java.

Place the two Bloomfilter files bf1_ones.csv and bf1_ones.csv into the ~/ecelgamal/ecelgamal/ These two Bloom filters are prepared using the optimized parameters as defined in the AMIA paper: m = 2^23, k = 45. Such parameter setting results in 648533 and 848822 number of one bits in the two Bloom filters. 

Run the following command to test
~/ecelgamal/ecelgamal$ mvn package

In our experiment conducted on a system with Intel i7-8750H 2.2GHz CPU and 16GB Memory, the first encryption step took 2966972.36 ms, the second homomorphic additive encryptopn step took 1588887.95 ms, the third and final decryption step took 6.24 ms. The number of zero bits in the projected union of the two private Bloom filter is 7257294, this leads to an estimation of 27005.27 as the union cardinality for the two private sets.

# References
https://pypi.org/project/numpy/  
https://pypi.org/project/hashlib/  
https://pypi.org/project/pycryptodome/  
