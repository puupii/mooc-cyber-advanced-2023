
# 03 Repeating Pads

<p>Implement a xorpad cipher: complete <code class="language-text">encrypt</code> and <code class="language-text">decrypt</code> functions in <code class="language-text">src/xorpad.py</code>.
Both functions are byte arrays and should output an byte array as an output.</p><p>The pad can be significantly shorter than the message. In such a case you should repeat the pad as long as needed.</p><p>Note that repeating short pads is highly problematic, for example, one can
deduce the pad if a short part of message is known in advance (can you figure out how?). Thus, this should not be used in practice.</p>

---

