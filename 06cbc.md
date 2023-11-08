
# 06 Cipher Block Chaining (CBC)

Feistel cipher in the previous exercise can only handle blocks of *m = 8*. Next we are going to extend the cipher
to handle messages of any sizes.
We will use cipher block chaining (CBC).

<p>The first step is to make sure that the message length is a multiple of 8.
This is done with PKCS#7 padding. In such padding, message is padded with extra bytes
so that the message length is a multiple of 8. The value of the bytes are equal to the added bytes. If the message length
is already a multiple of 8, then 8 bytes are added with a value of 8. In other words, padding will be one of the
following lines.</p>

<div class="gatsby-highlight" data-language="rest"><pre class="language-rest"><code class="language-rest">
01
02 02
03 03 03
04 04 04 04 
...</code></pre></div>

<p>(note that the numbers are byte values not ascii integers)</p>
The next step is to encrypt the message.
Here the message is divided into blocks of length 8, *P<sub>1</sub>,P<sub>1</sub>...*.
We also set *C<sub>0</sub> = iv*, where *iv* is an initialization vector, an array of length 8, provided as a parameter.
The encryption proceeds iteratively with

*C<sub>i</sub> = encrypt(P<sub>i</sub> xor C<sub>i-1</sub>)*,

is *encrypt* our block cipher. The final cipher message is *C<sub>1</sub>C<sub>2</sub>C<sub>3</sub>...*. Note that we do not include *C<sub>0</sub>* here, the initilization vector is sent separately.   


<img src="./cbcencrypt.svg" alt="CBC encrypt">     

<p>To decrypt, note that</p>

*P<sub>i</sub> xor C<sub>i-1</sub> = decypt(C<sub>i</sub>)*

<p>which we can rewrite</p>


*P<sub>i</sub>  = decypt(C<sub>i</sub>) xor C<sub>i-1</sub>*.   


<img src="./cbcdecrypt.svg" alt="CBC decrypt">    

<p>Complete Cbc class by implementing <code class="language-text">encode</code> and <code class="language-text">decode</code>. Remember to add and remove the padding.
Note that you will also need the fully-implemented Feistel class from the previous exercise.</p><p>Hint: you will probably find the xor helper function helpful. Do not forget add the pad even if the message length is already a multiple of 8.</p>

---

