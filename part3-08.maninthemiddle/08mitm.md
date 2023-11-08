
# 08 Man In The Middle

<p>Certificates are needed to prevent man in the middle attacks. In this exercise we will create a
man-in-the-middle server that capitalizes every letter of the HTML page. You should
capitalize the output only if the server responses with HTML.</p><p>The template contains a simple web server that connects simply shows the page address and nothing else.
Modify the server so that it pretends to be the server given in
<code class="language-text">self.remote_address</code> but capitalizes every letter in the response.</p><p>You should at least match response code, content, and content type.</p><p>You can test the server manually with</p><div class="gatsby-highlight" data-language="sh"><pre class="language-sh"><code class="language-sh">python3 mitm.py 8000 target_domain</code></pre></div><p>and by going to <code class="language-text">http://localhost:8000</code>. Do not forget to add <code class="language-text">http://</code> or <code class="language-text">https://</code> in the <code class="language-text">target_domain</code>.</p><p>You can use an external target or you can start your own local target by launching a target server with</p><div class="gatsby-highlight" data-language="sh"><pre class="language-sh"><code class="language-sh">python3 -m http.server 9000</code></pre></div><p>in the <code class="language-text">server</code> folder.
This will start the target server at port 9000 and</p><div class="gatsby-highlight" data-language="sh"><pre class="language-sh"><code class="language-sh">python3 mitm.py 8000 http://localhost:9000</code></pre></div><p>in the <code class="language-text">src</code> folder
will start a man-in-the-middle server at 8000.</p><p>Note that you can use https website as a target as well. The visible difference
here is that the browser will not show that the displayed website is secure.</p><p><em>Hints:</em></p><ol>
<li>Make sure to use both <code class="language-text">self.remote_address</code>  and <code class="language-text">self.path</code>.</li>
<li>Requests library is your friend.</li>
<li>You don't need to parse HTML. You can simply capitalize every letter in response (use <code class="language-text">upper()</code>).
This will certainly break certain pages, especially with javascript code.
Fancier approach would be to parse HTML with beautifulsoup but it is not needed for this exercise.</li>
</ol>

---

