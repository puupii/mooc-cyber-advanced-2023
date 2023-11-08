
# 04 Frequency Attack

<p>Implement a simple frequency attack against a substitution cipher.
Complete <code class="language-text">decode</code> in <code class="language-text">decode.py</code>. The function is given a string <code class="language-text">ciphertext</code> and dictionary <code class="language-text">frequencies</code>,
where <code class="language-text">frequencies[c]</code> is a float indicating how frequent is the letter.
The output of the function should be a string (not byte array).</p><p>You can assume that <code class="language-text">ciphertext</code> and the output do not use capital letters.
Non-characters (spaces, enters) are not changed.</p><p>Furthermore, you can assume that the frequency rank in <code class="language-text">frequencies</code> matches
the frequency rank in the message.  That is, the most common letter in
<code class="language-text">frequencies</code> will be the most common letter in the message.</p><p>Hint: <code class="language-text">string.ascii_lowercase</code> and <code class="language-text">islower()</code> can be handy.</p>

---

