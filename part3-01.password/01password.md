
# 01 Break the Hash

<p>In this exercise you are given a hash and a list of candidate passwords, and
your task is to write a password guesser that finds the password in the candidates that was used to generate the hash.</p><p>The hash follows a common format used for storing hashed password</p><div class="gatsby-highlight" data-language="text"><pre class="language-text"><code class="language-text">procotol$salt$hash</code></pre></div><p>Here, the protocol will always be set to 42, so you can ignore it.
For hashing we will use SHA-384. In this exercise, the hash is constructed by hashing a message containing the salt followed by the actual password.
In practice, the combination of salt and the password is significantly more convoluted.</p><p>The salt and the password hash are both base64 encoded in the hash string, and need to be decoded.</p><p><em>Hints:</em></p><ol>
<li>You will find hashlib and base64 libraries useful.</li>
<li>The hash and the candidates are all text strings but the above libraries operate with byte arrays. Use <code class="language-text">encode('utf-8')</code> to get a byte array from a text string.</li>
</ol>

---

