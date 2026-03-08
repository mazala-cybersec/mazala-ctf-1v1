const express = require("express");
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const FLAG = process.env.FLAG || "mazala{jwt_4lg_n0n3}";
const PORT  = process.env.PORT  || 5000;

// ── Minimal JWT (intentionally broken alg:none) ──────────────────────────
function b64url(s) {
  return Buffer.from(s).toString("base64")
    .replace(/=/g,"").replace(/\+/g,"-").replace(/\//g,"_");
}
function b64urlDecode(s) {
  s = s.replace(/-/g,"+").replace(/_/g,"/");
  while (s.length % 4) s += "=";
  return Buffer.from(s,"base64").toString("utf8");
}
function signToken(payload, alg="HS256") {
  const h = b64url(JSON.stringify({alg, typ:"JWT"}));
  const p = b64url(JSON.stringify(payload));
  const sig = alg === "none" ? "" : b64url("sig-"+Math.random());
  return `${h}.${p}.${sig}`;
}
function verifyToken(token) {
  try {
    const [h64, p64] = token.split(".");
    const header  = JSON.parse(b64urlDecode(h64));
    const payload = JSON.parse(b64urlDecode(p64));
    if (header.alg === "none") return payload;   // ← no sig check
    if (header.alg === "HS256") return payload;  // ← fake check
    return null;
  } catch { return null; }
}
// ────────────────────────────────────────────────────────────────────────

const ORDERS = [
  { id:"ORD-1042", item:"Margherita Pizza",    status:"Delivered",   total:"$14.99" },
  { id:"ORD-1031", item:"Chicken Burger",       status:"Delivered",   total:"$11.50" },
  { id:"ORD-1028", item:"Caesar Salad",         status:"Cancelled",   total:"$9.99"  },
];

const INDEX = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SwiftBite — Food Delivery</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:Arial,sans-serif;background:#fff9f2;color:#333;min-height:100vh}
  nav{background:#e53935;padding:0 32px;display:flex;align-items:center;justify-content:space-between;height:56px}
  nav .logo{color:#fff;font-size:1.2rem;font-weight:700;letter-spacing:1px}
  nav ul{list-style:none;display:flex;gap:20px}
  nav ul a{color:rgba(255,255,255,.8);text-decoration:none;font-size:.86rem}
  nav ul a:hover{color:#fff}
  .hero{background:linear-gradient(135deg,#e53935,#b71c1c);color:#fff;padding:44px 32px;text-align:center}
  .hero h1{font-size:1.9rem;margin-bottom:8px}
  .hero p{color:rgba(255,255,255,.65);font-size:.92rem}
  .container{max-width:860px;margin:36px auto;padding:0 24px}
  .panel{background:#fff;border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,.07);overflow:hidden;margin-bottom:24px}
  .panel-hdr{background:#ffebee;padding:16px 22px;border-bottom:1px solid #ffcdd2;display:flex;align-items:center;justify-content:space-between}
  .panel-hdr h2{font-size:.98rem;font-weight:700;color:#c62828}
  .panel-body{padding:22px}
  .form-group{margin-bottom:14px}
  .form-group label{display:block;font-size:.8rem;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:.8px;margin-bottom:5px}
  .form-group input{width:100%;border:1px solid #e0e0e0;border-radius:5px;padding:9px 13px;font-size:.9rem;outline:none}
  .form-group input:focus{border-color:#e53935}
  .btn-red{background:#e53935;color:#fff;border:none;padding:11px 28px;border-radius:5px;font-size:.9rem;font-weight:600;cursor:pointer}
  .btn-red:hover{background:#c62828}
  .btn-outline{background:transparent;color:#e53935;border:2px solid #e53935;padding:9px 22px;border-radius:5px;font-size:.88rem;font-weight:600;cursor:pointer;margin-left:10px}
  .order-row{display:flex;justify-content:space-between;align-items:center;padding:13px 0;border-bottom:1px solid #f5f5f5;font-size:.88rem}
  .order-row:last-child{border-bottom:none}
  .badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.74rem;font-weight:600}
  .badge.delivered{background:#e8f5e9;color:#2e7d32}
  .badge.cancelled{background:#fce4ec;color:#c62828}
  .badge.pending{background:#fff3e0;color:#e65100}
  .alert{padding:12px 16px;border-radius:6px;font-size:.86rem;margin-bottom:16px}
  .alert.err{background:#fce4ec;border:1px solid #ef9a9a;color:#c62828}
  .alert.ok{background:#e8f5e9;border:1px solid #a5d6a7;color:#2e7d32}
  .token-box{background:#f9f9f9;border:1px solid #e0e0e0;border-radius:5px;padding:10px 14px;font-family:monospace;font-size:.75rem;word-break:break-all;color:#555;margin-top:10px}
  .tabs{display:flex;border-bottom:2px solid #ffcdd2;margin-bottom:20px}
  .tab{padding:10px 20px;font-size:.88rem;font-weight:600;color:#999;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-2px}
  .tab.active{color:#e53935;border-color:#e53935}
  footer{background:#e53935;color:rgba(255,255,255,.5);text-align:center;padding:18px;font-size:.76rem;margin-top:40px}
</style>
</head>
<body>
<nav>
  <div class="logo">🍕 SwiftBite</div>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="#">Menu</a></li>
    <li><a href="#">Track Order</a></li>
    <li><a href="#">Account</a></li>
  </ul>
</nav>
<div class="hero">
  <h1>Fast Food, Faster Delivery</h1>
  <p>Order from the best local restaurants. Delivered in 30 minutes.</p>
</div>
<div class="container">

  <div class="panel">
    <div class="panel-hdr"><h2>My Account</h2></div>
    <div class="panel-body">
      <div class="tabs">
        <div class="tab active">Login</div>
        <div class="tab">Register</div>
      </div>
      <form method="POST" action="/login">
        <div class="form-group"><label>Email</label><input name="email" type="email" placeholder="you@example.com" value="demo@swiftbite.local"></div>
        <div class="form-group"><label>Password</label><input name="password" type="password" placeholder="••••••••" value="demo1234"></div>
        <button class="btn-red" type="submit">Login</button>
        <button class="btn-outline" type="button">Guest Checkout</button>
      </form>
    </div>
  </div>

  <div class="panel">
    <div class="panel-hdr"><h2>Recent Orders</h2><span style="font-size:.78rem;color:#999">Last 30 days</span></div>
    <div class="panel-body">
      ${ORDERS.map(o => `
      <div class="order-row">
        <div><strong>${o.item}</strong><div style="font-size:.76rem;color:#aaa;margin-top:2px">${o.id}</div></div>
        <div style="text-align:right"><div class="badge ${o.status.toLowerCase()}">${o.status}</div><div style="font-size:.82rem;margin-top:4px">${o.total}</div></div>
      </div>`).join("")}
    </div>
  </div>

</div>
<footer>© 2026 SwiftBite Technologies. All rights reserved.</footer>
</body>
</html>`;

const DASHBOARD = (token, alert) => `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SwiftBite — Dashboard</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:Arial,sans-serif;background:#fff9f2;color:#333}
  nav{background:#e53935;padding:0 32px;display:flex;align-items:center;justify-content:space-between;height:56px}
  nav .logo{color:#fff;font-size:1.2rem;font-weight:700}
  nav ul{list-style:none;display:flex;gap:20px}
  nav ul a{color:rgba(255,255,255,.8);text-decoration:none;font-size:.86rem}
  .container{max-width:860px;margin:36px auto;padding:0 24px}
  .panel{background:#fff;border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,.07);overflow:hidden;margin-bottom:24px}
  .panel-hdr{background:#ffebee;padding:16px 22px;border-bottom:1px solid #ffcdd2}
  .panel-hdr h2{font-size:.98rem;font-weight:700;color:#c62828}
  .panel-body{padding:22px}
  .alert{padding:12px 16px;border-radius:6px;font-size:.86rem;margin-bottom:16px}
  .alert.err{background:#fce4ec;border:1px solid #ef9a9a;color:#c62828}
  .alert.ok{background:#e8f5e9;border:1px solid #a5d6a7;color:#2e7d32}
  .token-box{background:#f9f9f9;border:1px solid #e0e0e0;border-radius:5px;padding:10px 14px;font-family:monospace;font-size:.75rem;word-break:break-all;color:#555;margin-top:10px}
  .btn-red{background:#e53935;color:#fff;border:none;padding:10px 24px;border-radius:5px;font-size:.88rem;font-weight:600;cursor:pointer;margin-top:12px}
  .form-group{margin-bottom:14px}
  .form-group label{display:block;font-size:.8rem;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:.8px;margin-bottom:5px}
  .form-group input{width:100%;border:1px solid #e0e0e0;border-radius:5px;padding:9px 13px;font-size:.88rem;font-family:monospace;outline:none}
  footer{background:#e53935;color:rgba(255,255,255,.5);text-align:center;padding:18px;font-size:.76rem;margin-top:40px}
</style>
</head>
<body>
<nav>
  <div class="logo">🍕 SwiftBite</div>
  <ul><li><a href="/">Home</a></li><li><a href="/dashboard">Dashboard</a></li></ul>
</nav>
<div class="container">
  ${alert ? `<div class="alert ${alert.type}">${alert.msg}</div>` : ""}
  <div class="panel">
    <div class="panel-hdr"><h2>Session Token</h2></div>
    <div class="panel-body">
      <p style="font-size:.88rem;color:#666;margin-bottom:8px">Your current session token (passed as Bearer header to API endpoints):</p>
      <div class="token-box">${token || "(no token)"}</div>
      <p style="font-size:.78rem;color:#aaa;margin-top:8px">Use this token to access <code style="background:#f0f0f0;padding:1px 5px">/api/orders</code> and <code style="background:#f0f0f0;padding:1px 5px">/api/admin/stats</code></p>
    </div>
  </div>
  <div class="panel">
    <div class="panel-hdr"><h2>Test API Access</h2></div>
    <div class="panel-body">
      <form method="POST" action="/api/admin/stats-form">
        <div class="form-group">
          <label>Bearer Token</label>
          <input name="token" value="${token || ""}" spellcheck="false" autocomplete="off">
        </div>
        <button class="btn-red" type="submit">Access Admin Stats →</button>
      </form>
    </div>
  </div>
</div>
<footer>© 2026 SwiftBite Technologies. All rights reserved.</footer>
</body>
</html>`;

const ADMIN_PAGE = (flag) => `<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>SwiftBite — Admin</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}body{font-family:Arial,sans-serif;background:#fff9f2;color:#333}
  nav{background:#e53935;padding:0 32px;display:flex;align-items:center;height:56px}
  nav .logo{color:#fff;font-size:1.2rem;font-weight:700}
  .container{max-width:860px;margin:36px auto;padding:0 24px}
  .panel{background:#fff;border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,.07);overflow:hidden;margin-bottom:24px}
  .panel-hdr{background:#ffebee;padding:16px 22px;border-bottom:1px solid #ffcdd2}
  .panel-hdr h2{font-size:.98rem;font-weight:700;color:#c62828}
  .panel-body{padding:22px;font-size:.9rem;line-height:1.8}
  .stat{display:inline-block;background:#ffebee;border-radius:8px;padding:14px 22px;margin:6px;text-align:center}
  .stat .n{font-size:1.6rem;font-weight:700;color:#e53935}
  .stat .l{font-size:.76rem;color:#999}
  .flag-box{background:#1a1a2e;color:#00ff41;font-family:monospace;padding:16px;border-radius:6px;word-break:break-all;margin-top:16px;font-size:.9rem}
  footer{background:#e53935;color:rgba(255,255,255,.5);text-align:center;padding:18px;font-size:.76rem;margin-top:40px}
</style></head>
<body>
<nav><div class="logo">🍕 SwiftBite Admin</div></nav>
<div class="container">
  <div class="panel">
    <div class="panel-hdr"><h2>Platform Statistics</h2></div>
    <div class="panel-body">
      <div class="stat"><div class="n">4,821</div><div class="l">Total Orders</div></div>
      <div class="stat"><div class="n">1,204</div><div class="l">Active Users</div></div>
      <div class="stat"><div class="n">$38,419</div><div class="l">Revenue (MTD)</div></div>
      <div class="stat"><div class="n">98.4%</div><div class="l">Delivery Rate</div></div>
      <div style="margin-top:20px;font-size:.82rem;color:#c62828;font-weight:600">System Token:</div>
      <div class="flag-box">${flag}</div>
    </div>
  </div>
</div>
<footer>© 2026 SwiftBite Technologies.</footer>
</body></html>`;

// ── Routes ───────────────────────────────────────────────────────────────
app.get("/", (req, res) => res.send(INDEX));

app.post("/login", (req, res) => {
  const token = signToken({ sub: "user_882", role: "customer", email: req.body.email || "demo@swiftbite.local", iat: Math.floor(Date.now()/1000) });
  res.redirect(`/dashboard?token=${encodeURIComponent(token)}`);
});

app.get("/dashboard", (req, res) => {
  const token = req.query.token || "";
  res.send(DASHBOARD(token, null));
});

function requireAdmin(token) {
  if (!token) return null;
  const payload = verifyToken(token);
  if (!payload) return null;
  return payload.role === "admin" ? payload : null;
}

app.get("/api/admin/stats", (req, res) => {
  const token = (req.headers.authorization || "").replace(/^Bearer\s+/i,"");
  if (!requireAdmin(token)) return res.status(403).json({ error: "Forbidden" });
  res.json({ flag: FLAG });
});

app.post("/api/admin/stats-form", (req, res) => {
  const token = (req.body.token || "").trim();
  const payload = verifyToken(token);
  if (!payload) return res.send(DASHBOARD(token, { type:"err", msg:"Invalid token structure." }));
  if (payload.role !== "admin") return res.send(DASHBOARD(token, { type:"err", msg:`Access denied — role '${payload.role}' is not permitted here.` }));
  res.send(ADMIN_PAGE(FLAG));
});

app.listen(PORT, "0.0.0.0", () => console.log(`[+] SwiftBite running on :${PORT}`));
