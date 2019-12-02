/*  The following program was prepared for the AMIA 2020 Informatics Summit paper "Toward a More Accurate 
    Accrual to Clinical Trials: Joint Cohort Discovery Using Bloom Filters and Homomorphic Encryption" by 
    Xiao Dong and David Randolph.

    The purpose of this program is to demonstrate how to use the following open source software to implement the
    three steps elgamal protocol described in the paper above. 
    https://github.com/lubux/ecelgamal

    This java program was implemented based on the test case proprograms from - 
    https://github.com/lubux/ecelgamal/blob/master/src/test/java/ECElGamalTest.java

    The following java utility may be needed to be imported to run this program    
    java.io.BufferedReader;java.io.FileReader;java.io.IOException;java.util.ArrayList;java.util.List;

    This program is for demo purpose only, do not modify and use it in the production system.

    Author: Xiao Dong*/

    @Test
    public void cohortTest() throws IOException{

	int m = (int) Math.pow(2, 23);
	
	int[] arrbf1_compliment =  new int[m];
	for (int i = 0; i < m; i++) {
		arrbf1_compliment[i] = 1;
	}

	BufferedReader br1 = new BufferedReader(new FileReader("bf1_ones.csv"));
	String line = "";

	while ((line = br1.readLine()) != null && !line.isEmpty()) {
		String[] indices_1 = line.split(",");
			for (int i=0; i<indices_1.length; i++) {
				arrbf1_compliment[Integer.valueOf(indices_1[i])] = 0;
			}
		}
	br1.close();

	int[] arrbf2 =  new int[m];
	for (int i = 0; i < m; i++) {
		arrbf2[i] = 0;
	}

	BufferedReader br2 = new BufferedReader(new FileReader("bf2_ones.csv"));
	line = "";

	while ((line = br2.readLine()) != null && !line.isEmpty()) {
		String[] indices_2 = line.split(",");
			for (int i=0; i<indices_2.length; i++) {
				arrbf2[Integer.valueOf(indices_2[i])] = 1;
			}
	}
	br2.close();

	ECElGamal.CRTParams params32 = ECElGamal.getDefault32BitParams();
	ECElGamal.ECElGamalKey key32 = ECElGamal.generateNewKey(params32);

	ECElGamal.ECElGamalCiphertext cipherArray[];
	cipherArray = new ECElGamal.ECElGamalCiphertext[m];

	ECElGamal.ECElGamalCiphertext cipher_sum;
	cipher_sum = ECElGamal.encrypt(BigInteger.valueOf(0), key32);

	long encrypt = System.nanoTime();
	for (int i=0; i<m; i++) {
		cipherArray[i] = ECElGamal.encrypt(BigInteger.valueOf(arrbf1_compliment[i]), key32);
	}
	encrypt = System.nanoTime() - encrypt;
	System.out.println(String.format("Enc: %.2f", convertMS(encrypt)));

	long addTime = System.nanoTime();
	for (int i=0; i<m; i++) {
		if (arrbf2[i] == 0) {
			cipher_sum = ECElGamal.add(cipher_sum, cipherArray[i]);
		}
	}
	addTime =  (System.nanoTime() - addTime);
	System.out.println(String.format("Add: %.2f", convertMS(addTime)));

	long decrypt = System.nanoTime();
	int decriptedVal = ECElGamal.decrypt32(cipher_sum, key32);
	decrypt = System.nanoTime() - decrypt;
	System.out.println(decriptedVal);
	System.out.println(String.format("Dec: %.2f", convertMS(decrypt)));
    }

