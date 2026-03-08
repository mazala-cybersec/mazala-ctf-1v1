from flask import Flask, request, render_template_string, Response
from lxml import etree
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "mazala{xxe_r34d_4ny_f1le}")

with open("/etc/flag", "w") as f:
    f.write(FLAG)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FreightFlow — Logistics Portal</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:Arial,sans-serif;background:#f0f4f8;color:#222;min-height:100vh}
  nav{background:#0d47a1;padding:0 32px;display:flex;align-items:center;justify-content:space-between;height:56px}
  nav .logo{color:#fff;font-size:1.15rem;font-weight:700;letter-spacing:1px}
  nav .logo span{color:#90caf9}
  nav ul{list-style:none;display:flex;gap:22px}
  nav ul a{color:rgba(255,255,255,.75);text-decoration:none;font-size:.86rem}
  nav ul a:hover{color:#fff}
  .hero{background:linear-gradient(135deg,#0d47a1,#1565c0);color:#fff;padding:38px 32px}
  .hero h1{font-size:1.7rem;margin-bottom:6px}
  .hero p{color:rgba(255,255,255,.6);font-size:.9rem}
  .container{max-width:960px;margin:32px auto;padding:0 24px;display:grid;grid-template-columns:2fr 1fr;gap:24px}
  .main-col{}
  .side-col{}
  .panel{background:#fff;border-radius:8px;box-shadow:0 1px 6px rgba(0,0,0,.07);overflow:hidden;margin-bottom:20px}
  .panel-hdr{background:#e3f2fd;padding:14px 20px;border-bottom:1px solid #bbdefb;display:flex;align-items:center;gap:10px}
  .panel-hdr h2{font-size:.95rem;font-weight:700;color:#0d47a1}
  .panel-hdr .icon{font-size:1.1rem}
  .panel-body{padding:20px}
  .form-group{margin-bottom:14px}
  .form-group label{display:block;font-size:.78rem;font-weight:600;color:#777;text-transform:uppercase;letter-spacing:.8px;margin-bottom:5px}
  .form-group input,.form-group select{width:100%;border:1px solid #dde;border-radius:5px;padding:9px 12px;font-size:.88rem;outline:none}
  .form-group input:focus,.form-group select:focus{border-color:#0d47a1}
  .form-group textarea{width:100%;border:1px solid #dde;border-radius:5px;padding:9px 12px;font-size:.82rem;font-family:'Courier New',monospace;outline:none;min-height:180px;resize:vertical;background:#fafafa;color:#333;line-height:1.55}
  .form-group textarea:focus{border-color:#0d47a1}
  .btn-blue{background:#0d47a1;color:#fff;border:none;padding:10px 26px;border-radius:5px;font-size:.88rem;font-weight:600;cursor:pointer}
  .btn-blue:hover{background:#0a3d91}
  .result-ok{background:#e8f5e9;border:1px solid #a5d6a7;border-radius:6px;padding:14px 16px;font-size:.86rem;color:#2e7d32;margin-top:14px;word-break:break-all;line-height:1.7}
  .result-err{background:#fce4ec;border:1px solid #f48fb1;border-radius:6px;padding:14px 16px;font-size:.84rem;color:#c62828;font-family:monospace;margin-top:14px;word-break:break-all;line-height:1.7}
  .shipment-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f0f0f0;font-size:.86rem}
  .shipment-row:last-child{border-bottom:none}
  .badge{display:inline-block;padding:2px 9px;border-radius:10px;font-size:.72rem;font-weight:600}
  .badge.transit{background:#e3f2fd;color:#0d47a1}
  .badge.delivered{background:#e8f5e9;color:#2e7d32}
  .badge.pending{background:#fff3e0;color:#e65100}
  .stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:4px}
  .stat-card{background:#e3f2fd;border-radius:6px;padding:12px;text-align:center}
  .stat-card .n{font-size:1.3rem;font-weight:700;color:#0d47a1}
  .stat-card .l{font-size:.72rem;color:#888}
  footer{background:#0d47a1;color:rgba(255,255,255,.45);text-align:center;padding:18px;font-size:.75rem;margin-top:40px;grid-column:1/-1}
</style>
</head>
<body>
<nav>
  <div class="logo">📦 Freight<span>Flow</span></div>
  <ul>
    <li><a href="/">Dashboard</a></li>
    <li><a href="#">Shipments</a></li>
    <li><a href="#">Invoices</a></li>
    <li><a href="#">Reports</a></li>
    <li><a href="#">Settings</a></li>
  </ul>
</nav>
<div class="hero">
  <h1>Logistics Management Portal</h1>
  <p>Track shipments, upload invoices and manage your freight operations</p>
</div>
<div class="container">
  <div class="main-col">
    <div class="panel">
      <div class="panel-hdr"><span class="icon">📄</span><h2>XML Invoice Upload</h2></div>
      <div class="panel-body">
        <p style="font-size:.85rem;color:#666;margin-bottom:14px">Upload your invoice in our standard XML format. Supported schema: FreightFlow Invoice v2.1</p>
        <form method="POST" action="/api/invoice/upload">
          <div class="form-group">
            <label>Shipment Reference</label>
            <input name="ref" value="{{ ref_val|e }}" placeholder="e.g. FF-2026-00441" autocomplete="off">
          </div>
          <div class="form-group">
            <label>XML Invoice Data</label>
            <textarea name="xml_data" spellcheck="false">{% if xml_val %}{{ xml_val }}{% else %}&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;invoice&gt;
  &lt;shipper&gt;Acme Corp&lt;/shipper&gt;
  &lt;recipient&gt;Global Freight Ltd&lt;/recipient&gt;
  &lt;item&gt;Industrial Parts&lt;/item&gt;
  &lt;weight unit="kg"&gt;340&lt;/weight&gt;
  &lt;total currency="USD"&gt;4200.00&lt;/total&gt;
&lt;/invoice&gt;{% endif %}</textarea>
          </div>
          <button type="submit" class="btn-blue">Upload Invoice →</button>
        </form>
        {% if result %}
        <div class="{{ result_class }}">{{ result }}</div>
        {% endif %}
      </div>
    </div>
  </div>
  <div class="side-col">
    <div class="panel">
      <div class="panel-hdr"><span class="icon">📊</span><h2>Overview</h2></div>
      <div class="panel-body">
        <div class="stat-grid">
          <div class="stat-card"><div class="n">148</div><div class="l">Active Shipments</div></div>
          <div class="stat-card"><div class="n">32</div><div class="l">Pending Invoices</div></div>
          <div class="stat-card"><div class="n">$1.2M</div><div class="l">MTD Revenue</div></div>
          <div class="stat-card"><div class="n">99.1%</div><div class="l">On-Time Rate</div></div>
        </div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-hdr"><span class="icon">🚚</span><h2>Recent Shipments</h2></div>
      <div class="panel-body">
        <div class="shipment-row"><div><strong style="font-size:.84rem">FF-2026-00441</strong><div style="font-size:.74rem;color:#aaa">Singapore → Rotterdam</div></div><span class="badge transit">In Transit</span></div>
        <div class="shipment-row"><div><strong style="font-size:.84rem">FF-2026-00438</strong><div style="font-size:.74rem;color:#aaa">Dubai → Hamburg</div></div><span class="badge delivered">Delivered</span></div>
        <div class="shipment-row"><div><strong style="font-size:.84rem">FF-2026-00435</strong><div style="font-size:.74rem;color:#aaa">Shanghai → LA</div></div><span class="badge pending">Pending</span></div>
        <div class="shipment-row"><div><strong style="font-size:.84rem">FF-2026-00431</strong><div style="font-size:.74rem;color:#aaa">Busan → Felixstowe</div></div><span class="badge delivered">Delivered</span></div>
      </div>
    </div>
  </div>
</div>
<footer style="background:#0d47a1;color:rgba(255,255,255,.45);text-align:center;padding:18px;font-size:.75rem;margin-top:0">
  © 2026 FreightFlow Logistics Systems. All rights reserved. &nbsp;|&nbsp; ops@freightflow.local
</footer>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(PAGE, ref_val="", xml_val="", result=None, result_class="")


@app.route("/api/invoice/upload", methods=["POST"])
def upload_invoice():
    ref = request.form.get("ref", "").strip()
    raw = (request.form.get("xml_data", "") or "").strip().encode()

    if not raw:
        return render_template_string(PAGE, ref_val=ref, xml_val="", result="Error: no XML data provided.", result_class="result-err")

    try:
        # VULNERABLE: resolve_entities=True
        parser = etree.XMLParser(resolve_entities=True, no_network=False)
        tree   = etree.fromstring(raw, parser)

        shipper   = tree.findtext("shipper")   or "(unknown)"
        recipient = tree.findtext("recipient") or "(unknown)"
        item      = tree.findtext("item")      or "(unknown)"
        total     = tree.findtext("total")     or "(unknown)"

        result       = f"✔ Invoice accepted for shipment {ref or 'N/A'} — Shipper: {shipper} | Recipient: {recipient} | Cargo: {item} | Amount: {total}"
        result_class = "result-ok"

    except etree.XMLSyntaxError as e:
        result       = f"XML parse error: {e}"
        result_class = "result-err"
    except Exception as e:
        result       = f"Processing error: {e}"
        result_class = "result-err"

    return render_template_string(
        PAGE,
        ref_val=ref,
        xml_val=raw.decode(errors="replace"),
        result=result,
        result_class=result_class
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
