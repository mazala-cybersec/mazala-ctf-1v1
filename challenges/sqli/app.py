from flask import Flask, request, render_template_string
import sqlite3, os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "mazala{sq1i_g0t_u}")

def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL, stock INTEGER)")
    conn.execute("CREATE TABLE flags (id INTEGER PRIMARY KEY, flag_value TEXT)")
    conn.executemany("INSERT INTO products VALUES (?,?,?,?,?)", [
        (1, "Wireless Mouse",      "Electronics",   29.99, 142),
        (2, "Mechanical Keyboard", "Electronics",   89.99,  58),
        (3, "USB-C Hub",           "Electronics",   34.99, 203),
        (4, "Desk Lamp",           "Office",        19.99,  77),
        (5, "Notebook Pack",       "Stationery",     9.99, 310),
        (6, "Cable Organizer",     "Office",        12.99, 415),
        (7, "Monitor Stand",       "Furniture",     49.99,  34),
        (8, "Webcam HD",           "Electronics",   64.99,  91),
    ])
    conn.execute("INSERT INTO flags VALUES (1, ?)", (FLAG,))
    conn.commit()
    return conn

DB = init_db()

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TechNest — Office & Electronics</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:Arial,sans-serif;background:#f4f6f8;color:#222;min-height:100vh}
  nav{background:#1a1a2e;padding:0 32px;display:flex;align-items:center;justify-content:space-between;height:56px}
  nav .logo{color:#fff;font-size:1.2rem;font-weight:700;letter-spacing:1px}
  nav .logo span{color:#4fc3f7}
  nav ul{list-style:none;display:flex;gap:24px}
  nav ul a{color:rgba(255,255,255,.7);text-decoration:none;font-size:.88rem}
  nav ul a:hover{color:#fff}
  .hero{background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;padding:40px 32px;text-align:center}
  .hero h1{font-size:1.8rem;margin-bottom:8px}
  .hero p{color:rgba(255,255,255,.6);font-size:.92rem;margin-bottom:24px}
  .search-bar{display:flex;max-width:520px;margin:0 auto}
  .search-bar input{flex:1;padding:12px 16px;border:none;font-size:.92rem;border-radius:4px 0 0 4px;outline:none}
  .search-bar button{background:#4fc3f7;color:#1a1a2e;border:none;padding:12px 24px;font-weight:700;font-size:.92rem;cursor:pointer;border-radius:0 4px 4px 0}
  .search-bar button:hover{background:#29b6f6}
  .container{max-width:1000px;margin:32px auto;padding:0 24px}
  .section-title{font-size:1rem;font-weight:700;color:#555;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #e0e0e0}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:18px;margin-bottom:32px}
  .card{background:#fff;border-radius:8px;padding:18px;box-shadow:0 1px 4px rgba(0,0,0,.08)}
  .card .cat{font-size:.72rem;color:#4fc3f7;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}
  .card .name{font-size:.95rem;font-weight:600;margin-bottom:6px}
  .card .price{font-size:1.05rem;color:#1a1a2e;font-weight:700}
  .card .stock{font-size:.76rem;color:#888;margin-top:4px}
  .card .btn{display:block;margin-top:12px;background:#1a1a2e;color:#fff;text-align:center;padding:7px;border-radius:4px;font-size:.82rem;cursor:pointer;border:none;width:100%}
  .results-box{background:#fff;border-radius:8px;padding:20px 24px;box-shadow:0 1px 4px rgba(0,0,0,.08);margin-bottom:24px}
  .results-box h3{font-size:.95rem;font-weight:700;margin-bottom:12px;color:#333}
  .result-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f0f0f0;font-size:.88rem}
  .result-row:last-child{border-bottom:none}
  .result-row .rname{font-weight:600}
  .result-row .rprice{color:#1a1a2e;font-weight:700}
  .no-result{color:#999;font-size:.88rem;font-style:italic}
  .error-box{background:#fff3f3;border:1px solid #ffcccc;border-radius:6px;padding:14px 18px;font-size:.84rem;color:#c0392b;font-family:monospace;word-break:break-all;margin-bottom:20px}
  footer{background:#1a1a2e;color:rgba(255,255,255,.4);text-align:center;padding:20px;font-size:.78rem;margin-top:40px}
</style>
</head>
<body>
<nav>
  <div class="logo">Tech<span>Nest</span></div>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="#">Products</a></li>
    <li><a href="#">Deals</a></li>
    <li><a href="#">Contact</a></li>
  </ul>
</nav>
<div class="hero">
  <h1>Office &amp; Electronics — Free shipping over $50</h1>
  <p>Search thousands of products for your workspace</p>
  <form method="GET" action="/search">
    <div class="search-bar">
      <input name="q" value="{{ query|e }}" placeholder="Search products..." autocomplete="off" spellcheck="false">
      <button type="submit">Search</button>
    </div>
  </form>
</div>
<div class="container">
  {% if error %}
  <div class="error-box">{{ error }}</div>
  {% endif %}
  {% if rows is not none %}
  <div class="results-box">
    <h3>Results for "{{ query|e }}"</h3>
    {% if rows %}
      {% for row in rows %}
      <div class="result-row">
        <div>
          <div class="rname">{{ row[0] }}</div>
          <div style="font-size:.76rem;color:#aaa">{{ row[1] if row|length > 1 else '' }}</div>
        </div>
        <div class="rprice">{{ row[2] if row|length > 2 else '' }}</div>
      </div>
      {% endfor %}
    {% else %}
      <div class="no-result">No products found matching "{{ query|e }}".</div>
    {% endif %}
  </div>
  {% endif %}
  <div class="section-title">Featured Products</div>
  <div class="grid">
    <div class="card"><div class="cat">Electronics</div><div class="name">Wireless Mouse</div><div class="price">$29.99</div><div class="stock">142 in stock</div><button class="btn">Add to Cart</button></div>
    <div class="card"><div class="cat">Electronics</div><div class="name">Mechanical Keyboard</div><div class="price">$89.99</div><div class="stock">58 in stock</div><button class="btn">Add to Cart</button></div>
    <div class="card"><div class="cat">Electronics</div><div class="name">USB-C Hub</div><div class="price">$34.99</div><div class="stock">203 in stock</div><button class="btn">Add to Cart</button></div>
    <div class="card"><div class="cat">Office</div><div class="name">Desk Lamp</div><div class="price">$19.99</div><div class="stock">77 in stock</div><button class="btn">Add to Cart</button></div>
    <div class="card"><div class="cat">Electronics</div><div class="name">Webcam HD</div><div class="price">$64.99</div><div class="stock">91 in stock</div><button class="btn">Add to Cart</button></div>
    <div class="card"><div class="cat">Furniture</div><div class="name">Monitor Stand</div><div class="price">$49.99</div><div class="stock">34 in stock</div><button class="btn">Add to Cart</button></div>
  </div>
</div>
<footer>© 2026 TechNest Ltd. All rights reserved. &nbsp;|&nbsp; support@technest.local</footer>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(PAGE, query="", rows=None, error=None)


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    rows, error = None, None
    if q:
        try:
            cur = DB.execute(
                f"SELECT name, category, '$' || CAST(price AS TEXT) FROM products WHERE name LIKE '%{q}%'"
            )
            rows = cur.fetchall()
        except Exception as e:
            error = str(e)
    return render_template_string(PAGE, query=q, rows=rows, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
