
# 05 Feistel Cipher

Feistel ciphers are used as a building blocks in constructing many known block ciphers.</p><p>In feistel cipher you are given a block cipher **F** that can encrypt a message of length *m*.
You are also given *n* keys **(K<sub>1</sub>,...,K<sub>n</sub>)**.   


Feistel cipher is a block cipher encrypting messages of *2m*.
At the beginning, original message is split in two halves, *L<sub>0</sub>* and R<sub>0</sub>, each of size *m*.
Then *n* iterations are done with updates   

L<sub>i</sub> = R<sub>i-1</sub>   
R<sub>i</sub> = L<sub>i-1</sub> xor F(R<sub>i-1</sub>, K<sub>i</sub>).   

Here *L<sub>i</sub>* and *R<sub>i</sub>* are the two halves of the ciphertext after ith round.   
The final cipher is *L<sub>n</sub>* followed by *R<sub>n</sub>*.
<p>The decryption works in similar fashion but in reverse order.
Note that we can rewrite the update equations as</p>

R<sub>i-1</sub> = L<sub>i</sub>   
L<sub>i</sub>   = R<sub>i</sub> xor F(R<sub>i-1</sub>, K<sub>i</sub>) = R<sub>i</sub> xor F(L<sub>i</sub>, K<sub>i</sub>).   

In other words, we can start from *L<sub>n</sub>* and *R<sub>n</sub>* and reverse all the way back to *L<sub>0</sub>* and *R<sub>0</sub>*.   


<img src="./feistel.svg">     


Implement Feistel cipher: complete encrypt and decrypt in <code class="language-text">src/feistel.py</code>.
The function *F* is a class parameter <code class="language-text">self.roundf</code>, and the keys is an array in class parameters <code class="language-text">self.keys</code>.   

You can assume that the block size *m* of *F* is 4.

---

