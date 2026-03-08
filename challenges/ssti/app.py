from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "mazala{sst1_pwn3d}")

with open("/etc/flag", "w") as f:
    f.write(FLAG)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CardCraft — Personalised Greeting Cards</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:'Georgia',serif;background:#fdf8f3;color:#333;min-height:100vh}
  nav{background:#5d4037;padding:0 32px;display:flex;align-items:center;justify-content:space-between;height:54px}
  nav .logo{color:#ffe0b2;font-size:1.15rem;font-weight:700;letter-spacing:2px}
  nav ul{list-style:none;display:flex;gap:22px}
  nav ul a{color:rgba(255,224,178,.75);text-decoration:none;font-size:.86rem}
  nav ul a:hover{color:#ffe0b2}
  .hero{background:linear-gradient(135deg,#5d4037,#8d6e63);color:#fff;padding:50px 32px;text-align:center}
  .hero h1{font-size:2rem;margin-bottom:10px;font-weight:400;letter-spacing:1px}
  .hero p{color:rgba(255,255,255,.65);font-size:.95rem;margin-bottom:0}
  .container{max-width:820px;margin:40px auto;padding:0 24px}
  .card-builder{background:#fff;border-radius:12px;box-shadow:0 2px 16px rgba(93,64,55,.1);overflow:hidden;margin-bottom:32px}
  .card-builder .cb-header{background:#efebe9;padding:18px 24px;border-bottom:1px solid #d7ccc8}
  .card-builder .cb-header h2{font-size:1.05rem;font-weight:600;color:#5d4037;font-family:Arial,sans-serif}
  .card-builder .cb-body{padding:28px 24px}
  .form-group{margin-bottom:18px}
  .form-group label{display:block;font-size:.82rem;font-family:Arial,sans-serif;font-weight:600;color:#8d6e63;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}
  .form-group input,.form-group select,.form-group textarea{width:100%;border:1px solid #d7ccc8;border-radius:6px;padding:10px 14px;font-size:.9rem;font-family:Arial,sans-serif;outline:none;background:#fdf8f3;color:#333}
  .form-group input:focus,.form-group select:focus{border-color:#8d6e63}
  .form-group textarea{min-height:90px;resize:vertical}
  .form-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
  .preview-btn{background:#5d4037;color:#ffe0b2;border:none;padding:12px 32px;border-radius:6px;font-family:Arial,sans-serif;font-size:.92rem;font-weight:600;cursor:pointer;letter-spacing:1px}
  .preview-btn:hover{background:#4e342e}
  .card-preview{margin-top:24px;border:2px dashed #d7ccc8;border-radius:10px;padding:28px;background:#fffef9;text-align:center;display:none}
  .card-preview.visible{display:block}
  .card-preview .greeting{font-size:1.4rem;color:#5d4037;margin-bottom:10px}
  .card-preview .message{color:#666;font-size:.95rem;line-height:1.7}
  .samples{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:32px}
  .sample{background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(93,64,55,.08);text-align:center;padding:20px 16px}
  .sample .emoji{font-size:2.2rem;margin-bottom:8px}
  .sample .stitle{font-size:.9rem;font-weight:600;font-family:Arial,sans-serif;color:#5d4037;margin-bottom:4px}
  .sample .sdesc{font-size:.78rem;color:#999;font-family:Arial,sans-serif}
  footer{background:#5d4037;color:rgba(255,224,178,.5);text-align:center;padding:20px;font-size:.76rem;font-family:Arial,sans-serif;margin-top:40px}
</style>
</head>
<body>
<nav>
  <div class="logo">✉ CardCraft</div>
  <ul>
    <li><a href="/">Create</a></li>
    <li><a href="#">Gallery</a></li>
    <li><a href="#">Pricing</a></li>
    <li><a href="#">Login</a></li>
  </ul>
</nav>
<div class="hero">
  <h1>Create a Personalised Greeting Card</h1>
  <p>Beautiful cards for every occasion, delivered instantly</p>
</div>
<div class="container">
  <div class="card-builder">
    <div class="cb-header"><h2>Card Builder</h2></div>
    <div class="cb-body">
      <form method="GET" action="/preview">
        <div class="form-row">
          <div class="form-group">
            <label>Recipient Name</label>
            <input name="to" value="{{ to_val|e }}" placeholder="e.g. Sarah" autocomplete="off" spellcheck="false">
          </div>
          <div class="form-group">
            <label>Occasion</label>
            <select name="occasion">
              <option>Birthday</option>
              <option>Anniversary</option>
              <option>Congratulations</option>
              <option>Thank You</option>
              <option>Get Well Soon</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>Personal Message</label>
          <textarea name="msg" placeholder="Write something heartfelt..." spellcheck="false">{{ msg_val|e }}</textarea>
        </div>
        <button type="submit" class="preview-btn">Preview Card →</button>
      </form>
      {% if preview_html %}
      <div class="card-preview visible">
        <div class="greeting">{{ preview_html }}</div>
        <div class="message">{{ msg_safe }}</div>
      </div>
      {% endif %}
    </div>
  </div>
  <div class="samples">
    <div class="sample"><div class="emoji">🎂</div><div class="stitle">Birthday</div><div class="sdesc">Make their day special</div></div>
    <div class="sample"><div class="emoji">💐</div><div class="stitle">Anniversary</div><div class="sdesc">Celebrate your love</div></div>
    <div class="sample"><div class="emoji">🎉</div><div class="stitle">Congratulations</div><div class="sdesc">Share the excitement</div></div>
  </div>
</div>
<footer>© 2026 CardCraft. All rights reserved. &nbsp;|&nbsp; hello@cardcraft.local</footer>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(PAGE, to_val="", msg_val="", preview_html=None, msg_safe=None)


@app.route("/preview")
def preview():
    to  = request.args.get("to", "Friend")
    msg = request.args.get("msg", "")
    occ = request.args.get("occasion", "Birthday")

    # VULNERABLE: to is injected directly into a template string
    inner = f"Happy {occ}, {to}! 🎉"
    try:
        rendered = render_template_string(inner)
    except Exception as e:
        rendered = f"(error: {e})"

    return render_template_string(
        PAGE,
        to_val=to,
        msg_val=msg,
        preview_html=rendered,
        msg_safe=msg
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
