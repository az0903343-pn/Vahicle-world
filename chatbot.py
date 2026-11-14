"""
Floating chatbot widget for the Vehicle Budget Recommender.

How it works
------------
render_chatbot(df) embeds the vehicle dataset into a small self-contained
HTML/JavaScript app (a Streamlit component). The widget floats in the
bottom-right corner of the page:

- a pulsing round chat bubble, click it to open a glassy chat panel
- the chatbot is rule-based and answers from the dataset itself
  (no API key, works offline, no cost):
    * "100000 me kya aata hai?"  -> best vehicles in that budget
    * "Honda CD 70"              -> full info + similar vehicles
    * "sabse sasti car"          -> cheapest vehicle of a category
    * "mehngi helicopter"        -> most expensive vehicle
    * "10 lakh combo"            -> a combination that uses the budget
    * "sabse tez bike"           -> fastest vehicle
- chat history survives Streamlit re-runs (saved in localStorage)
"""
import json

import pandas as pd
import streamlit.components.v1 as components

from recommender import CATEGORY_EMOJI


def render_chatbot(df: pd.DataFrame):
    """Renders the floating chatbot widget. Call it once, at the end of app.py."""
    vehicles = [
        {
            "n": r["name"],
            "c": r["category"],
            "b": r["brand"],
            "p": float(r["price_pkr"]),
            "f": r["fuel_type"],
            "s": int(r["seats"]),
            "t": int(r["top_speed_kmh"]),
        }
        for _, r in df.iterrows()
    ]
    data = json.dumps(vehicles, ensure_ascii=False).replace("<", "\\u003c")
    emoji_map = json.dumps(CATEGORY_EMOJI, ensure_ascii=False)

    html = _HTML.replace("__DATA__", data).replace("__EMOJI__", emoji_map)
    # height 72 = collapsed bubble; the widget grows itself when opened
    components.html(html, height=72, width=380, scrolling=False)


_HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body { background: transparent !important; margin: 0; padding: 0;
               font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; }
  #root { position: fixed; inset: 0; }

  /* ---------- bubble ---------- */
  #bubble { position: absolute; right: 14px; bottom: 14px; width: 56px; height: 56px;
            border-radius: 50%; border: none; cursor: pointer; font-size: 26px;
            background: linear-gradient(135deg,#6366f1,#a855f7 55%,#ec4899);
            box-shadow: 0 8px 24px rgba(139,92,246,.55); display: flex;
            align-items: center; justify-content: center; z-index: 10; }
  #bubble::after { content: ""; position: absolute; inset: -6px; border-radius: 50%;
            border: 2px solid rgba(168,85,247,.55); animation: pulse 2s infinite; }
  @keyframes pulse { 0% {transform: scale(.9); opacity: 1;}
                     70% {transform: scale(1.25); opacity: 0;} 100% {opacity: 0;} }

  /* ---------- panel ---------- */
  #panel { position: absolute; inset: 0; display: none; flex-direction: column;
           background: linear-gradient(160deg, rgba(15,18,38,.97), rgba(24,20,48,.97));
           border: 1px solid rgba(255,255,255,.14); border-radius: 18px;
           box-shadow: 0 18px 50px rgba(0,0,0,.55); overflow: hidden; }
  header { display: flex; align-items: center; gap: 10px; padding: 12px 14px;
           background: linear-gradient(135deg, rgba(99,102,241,.35), rgba(236,72,153,.25));
           border-bottom: 1px solid rgba(255,255,255,.1); }
  header .logo { font-size: 22px; }
  header .title { color: #fff; font-weight: 700; font-size: 14px; }
  header .sub { color: #c7d2fe; font-size: 11px; }
  #close { margin-left: auto; background: rgba(255,255,255,.12); color: #fff;
           border: none; border-radius: 8px; width: 26px; height: 26px;
           cursor: pointer; font-size: 13px; }

  #msgs { flex: 1; overflow-y: auto; padding: 12px; display: flex;
          flex-direction: column; gap: 8px; }
  #msgs::-webkit-scrollbar { width: 5px; }
  #msgs::-webkit-scrollbar-thumb { background: rgba(255,255,255,.2); border-radius: 3px; }

  .msg { max-width: 88%; padding: 8px 11px; border-radius: 14px; font-size: 12.5px;
         line-height: 1.45; color: #e8ecff; animation: pop .18s ease; }
  @keyframes pop { from {opacity: 0; transform: translateY(6px);} to {opacity: 1;} }
  .bot { align-self: flex-start; background: rgba(255,255,255,.09);
         border: 1px solid rgba(255,255,255,.1); border-bottom-left-radius: 4px; }
  .user { align-self: flex-end; background: linear-gradient(135deg,#6366f1,#8b5cf6);
          border-bottom-right-radius: 4px; }
  .msg b { color: #fff; }
  .card { margin: 3px 0; padding: 6px 9px; background: rgba(255,255,255,.06);
          border: 1px solid rgba(255,255,255,.1); border-radius: 10px; }
  .card .row { display: flex; justify-content: space-between; gap: 8px; }
  .price { color: #4ade80; font-weight: 600; white-space: nowrap; }
  .hint { color: #94a3b8; font-size: 11px; }
  .typing { align-self: flex-start; color: #94a3b8; font-size: 12px; padding: 4px 10px; }

  #chips { display: flex; flex-wrap: wrap; gap: 5px; padding: 6px 10px;
           border-top: 1px solid rgba(255,255,255,.08); }
  .chip { font-size: 11px; color: #cbd5ff; background: rgba(99,102,241,.18);
          border: 1px solid rgba(129,140,248,.4); border-radius: 20px;
          padding: 4px 10px; cursor: pointer; }
  .chip:hover { background: rgba(99,102,241,.4); }

  #row { display: flex; gap: 7px; padding: 9px 10px;
         border-top: 1px solid rgba(255,255,255,.08); background: rgba(0,0,0,.25); }
  #inp { flex: 1; background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.15);
         border-radius: 20px; padding: 8px 13px; color: #fff; font-size: 12.5px;
         outline: none; }
  #inp::placeholder { color: #64748b; }
  #send { width: 36px; border: none; border-radius: 50%; cursor: pointer;
          background: linear-gradient(135deg,#6366f1,#a855f7); color: #fff; font-size: 15px; }
</style>
</head>
<body>
<div id="root">
  <button id="bubble" title="Chat with V-Bot">🤖</button>
  <div id="panel">
    <header>
      <div class="logo">🤖</div>
      <div><div class="title">V-Bot — Vehicle Assistant</div>
           <div class="sub">budget · prices · comparisons</div></div>
      <button id="close">✕</button>
    </header>
    <div id="msgs"></div>
    <div id="chips"></div>
    <div id="row">
      <input id="inp" placeholder="Budget ya vehicle ka naam likhein...">
      <button id="send">➤</button>
    </div>
  </div>
</div>

<script>
const V = __DATA__;
const EMOJI = __EMOJI__;
const $ = (id) => document.getElementById(id);

/* ---------- fit the iframe & resize on open/close ---------- */
function setMode(open) {
  const f = window.frameElement;
  if (f) {
    f.style.position = "fixed"; f.style.bottom = "16px"; f.style.right = "16px";
    f.style.zIndex = "999999"; f.style.border = "none";
    f.style.width = open ? "380px" : "76px";
    f.style.height = open ? "560px" : "76px";
    f.style.background = "transparent";
  }
  $("bubble").style.display = open ? "none" : "flex";
  $("panel").style.display = open ? "flex" : "none";
  if (open) $("inp").focus();
}

/* ---------- helpers ---------- */
function emoji(cat) { return EMOJI[cat] || "🚗"; }
function words(n) {
  if (n >= 1e9) return (n / 1e9).toFixed(2) + " arab";
  if (n >= 1e7) return (n / 1e7).toFixed(2) + " crore";
  if (n >= 1e5) return (n / 1e5).toFixed(2) + " lakh";
  return null;
}
function money(n) {
  const w = words(n);
  return "Rs " + n.toLocaleString("en-US") + (w ? " (" + w + ")" : "");
}
function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function card(v) {
  return '<div class="card"><div class="row"><b>' + emoji(v.c) + " " + esc(v.n) +
         '</b><span class="price">' + money(v.p) + "</span></div>" +
         '<div class="hint">' + esc(v.c) + " · " + esc(v.f) + " · " + v.s +
         " seats · " + v.t + " km/h</div></div>";
}
function cats() { return [...new Set(V.map(v => v.c))]; }

/* ---------- chat history (survives app re-runs) ---------- */
let history = [];
try { history = JSON.parse(localStorage.getItem("vbot_chat") || "[]"); } catch (e) {}
function save() {
  try { localStorage.setItem("vbot_chat", JSON.stringify(history.slice(-30))); } catch (e) {}
}
function push(who, html, persist) {
  const el = document.createElement("div");
  el.className = "msg " + who;
  el.innerHTML = html;
  $("msgs").appendChild(el);
  $("msgs").scrollTop = $("msgs").scrollHeight;
  if (persist !== false) { history.push({ who: who, html: html }); save(); }
}

/* ---------- brain ---------- */
function parseBudget(t) {
  const m = t.match(/(\d[\d.,]*)\s*(arab|billion|crore|carore|million|lakh|lac|k)?/);
  if (!m) return null;
  let n = parseFloat(m[1].replace(/[,\s]/g, ""));
  if (isNaN(n)) return null;
  const u = m[2] || "";
  if (u === "arab" || u === "billion") n *= 1e9;
  else if (u === "crore" || u === "carore") n *= 1e7;
  else if (u === "million") n *= 1e6;
  else if (u === "lakh" || u === "lac") n *= 1e5;
  else if (u === "k") n *= 1e3;
  return n;
}
const CATRULES = [
  ["heavy bike|sports bike|hayabusa|ktm|duke|harley|cbr|z900", "Heavy Bike"],
  ["electric|e-bike|ebike|jolta|yadea|evee|vlektra", "Electric Bike"],
  ["cycle|bicycle|bmx|pedal", "Cycle"],
  ["scooter|scooty|vespa|juno|activa", "Scooter"],
  ["petrol bike|motorbike|motorcycle|70cc|125cc|cd 70|cg 125|ybr", "Petrol Bike"],
  ["rickshaw|qingqi|.loader", "Rickshaw"],
  ["van|hiace|bolan|karvaan", "Van"],
  ["car|mehran|alto|cultus|corolla|civic|fortuner|land cruiser|sportage|tucson", "Car"],
  ["bus|truck|coach|shehzore|trailer", "Bus/Truck"],
  ["tractor|millat|john deere|new holland", "Tractor"],
  ["boat|yacht|jet ski|trawler|jet-ski", "Boat"],
  ["helicopter|copter|robinson|bell 407|airbus h", "Helicopter"],
  ["aircraft|aeroplane|airplane|plane|skyhawk|piper", "Aircraft"],
  ["jet|gulfstream|citation|bombardier|bbj|phenom", "Jet"],
];
function detectCat(t) {
  for (const [keys, cat] of CATRULES) {
    if (new RegExp(keys).test(t)) {
      if (cat === "Cycle") return V.filter(v => v.c.includes("Cycle")).length ? "Cycle*" : cat;
      return cat;
    }
  }
  return null;
}
function inCat(cat) {
  return cat === "Cycle*" ? V.filter(v => v.c.includes("Cycle")) : V.filter(v => v.c === cat);
}
function findVehicle(t) {
  const tt = t.split(/[^a-z0-9]+/).filter(Boolean);
  let best = null, bestScore = 0;
  for (const v of V) {
    const n = v.n.toLowerCase();
    let score = 0;
    if (t.length >= 4 && n.includes(t)) score += 3;
    const toks = n.split(/[^a-z0-9]+/).filter(w => w.length > 1);
    for (const w of toks) if (tt.includes(w)) score += 1;
    if (score > bestScore) { bestScore = score; best = v; }
  }
  return bestScore >= 3 ? best : null;
}
function budgetReply(budget) {
  const pool = V.filter(v => v.p <= budget).sort((a, b) => b.p - a.p);
  if (!pool.length) {
    const cheapest = [...V].sort((a, b) => a.p - b.p)[0];
    return "😅 Is budget me dataset ka koi vehicle nahi aata.<br> sabse sasti cheez hai:<br>" +
           card(cheapest) + "<span class='hint'>budget " + money(cheapest.p) + " tak barha kar dekhein!</span>";
  }
  let html = "💰 <b>" + money(budget) + "</b> me aap ye khareed sakte hain (" + pool.length + " options):<br>";
  pool.slice(0, 6).forEach(v => { html += card(v); });
  const combo = [];
  let left = budget;
  for (const v of pool) {
    if (combo.length >= 3) break;
    if (v.p <= left) { combo.push(v); left -= v.p; }
  }
  if (combo.length > 1) {
    html += "<span class='hint'>💡 Smart combo: " + combo.map(v => emoji(v.c) + " " + esc(v.n)).join(" + ") +
            "</span>";
  }
  return html;
}
function catReply(cat) {
  const list = inCat(cat).sort((a, b) => a.p - b.p);
  let html = emoji(cat === "Cycle*" ? "Cycle" : cat) + " <b>" + (cat === "Cycle*" ? "Cycle" : cat) +
             "</b> — dataset me " + list.length + " vehicles hain.<br>" +
             "<span class='hint'>sabse sasti: " + esc(list[0].n) + " (" + money(list[0].p) +
             ") · sabse mehngi: " + esc(list[list.length - 1].n) + " (" + money(list[list.length - 1].p) + ")</span><br>";
  list.slice(0, 4).forEach(v => { html += card(v); });
  return html;
}
function comboReply(budget) {
  const pool = V.filter(v => v.p <= budget).sort((a, b) => b.p - a.p);
  if (!pool.length) return "😅 Is budget me combo possible nahi.";
  const combo = []; let left = budget;
  for (const v of pool) {
    if (combo.length >= 3) break;
    if (v.p <= left) { combo.push(v); left -= v.p; }
  }
  let html = "🧩 <b>" + money(budget) + "</b> ka combo:<br>";
  combo.forEach(v => { html += card(v); });
  html += "<span class='hint'>Total " + money(budget - left) + " · bacha " + money(left) + "</span>";
  return html;
}
function respond(text) {
  const t = text.toLowerCase().trim();

  if (/^(hi|hello|hey|salam|assalam|aoa|asalam)/.test(t))
    return "👋 <b>Salam!</b> Main V-Bot hoon. Aap mujh se vehicles ke baare me kuch bhi pooch sakte hain —<br>" +
           "<span class='hint'>jaise: <i>100000 me kya aata hai</i>, <i>Honda CD 70</i>, <i>sabse sasti car</i>, <i>mehngi helicopter</i></span>";
  if (/help|madad|kya kar sakte|kaise/.test(t))
    return "🧠 Main ye sab bata sakta hoon:<br>" +
           "<div class='card'>💬 <i>150000 me kya aata hai?</i> — budget ke andar best options</div>" +
           "<div class='card'>🔍 <i>Honda CD 70</i> — kisi bhi vehicle ki full info</div>" +
           "<div class='card'>💸 <i>sabse sasti car</i> / <i>mehngi helicopter</i></div>" +
           "<div class='card'>🧩 <i>10 lakh combo</i> — budget ka smart combination</div>" +
           "<div class='card'>⚡ <i>sabse tez bike</i> — fastest vehicle</div>";

  const num = parseBudget(t);
  const cat = detectCat(t);

  if (/sabse sasta|sabse sasti|cheapest|sasta|sasti/.test(t)) {
    const list = cat ? inCat(cat) : V;
    const v = [...list].sort((a, b) => a.p - b.p)[0];
    return (cat ? emoji(cat) + " " : "") + "💸 Sabse sasti " + (cat === "Cycle*" ? "cycle" : cat ? cat : "vehicle") + ":<br>" + card(v);
  }
  if (/sabse mehnga|sabse mehngi|mehnga|mehngi|expensive|top end/.test(t)) {
    const list = cat ? inCat(cat) : V;
    const v = [...list].sort((a, b) => b.p - a.p)[0];
    return (cat ? emoji(cat) + " " : "") + "👑 Sabse mehngi " + (cat === "Cycle*" ? "cycle" : cat ? cat : "vehicle") + ":<br>" + card(v);
  }
  if (/sabse tez|fastest|speed/.test(t)) {
    const list = cat ? inCat(cat) : V;
    const v = [...list].sort((a, b) => b.t - a.t)[0];
    return "⚡ Sabse tez " + (cat === "Cycle*" ? "cycle" : cat ? cat : "vehicle") + ":<br>" + card(v);
  }
  if (/combo|combin|mix/.test(t)) return comboReply(num || 1000000);
  if (num !== null && num > 1000) return budgetReply(num);

  const v = findVehicle(t);
  if (v) {
    const sim = V.filter(x => x.c === v.c && x.n !== v.n && x.p >= v.p * 0.5 && x.p <= v.p * 1.6)
                 .sort((a, b) => Math.abs(a.p - v.p) - Math.abs(b.p - v.p)).slice(0, 2);
    let html = emoji(v.c) + " <b>" + esc(v.n) + "</b><br>" +
               "<div class='card'><div class='row'><span>🏷️ " + esc(v.b) + " · " + esc(v.c) +
               "</span><span class='price'>" + money(v.p) + "</span></div>" +
               "<div class='hint'>⛽ " + esc(v.f) + " · 🪑 " + v.s + " seats · ⚡ top " + v.t + " km/h</div></div>";
    if (sim.length) html += "<span class='hint'>🔎 Isi jaisi:</span><br>" + sim.map(card).join("");
    return html;
  }
  if (cat) return catReply(cat);

  return "🤔 Ye thora samajh nahi aaya. Aap ye try karein:<br>" +
         "<div class='card'>💰 <i>100000 me kya aata hai</i></div>" +
         "<div class='card'>🔍 <i>Honda CD 70</i></div>" +
         "<div class='card'>🚁 <i>sabse mehngi helicopter</i></div>";
}

/* ---------- UI wiring ---------- */
function send() {
  const text = $("inp").value.trim();
  if (!text) return;
  $("inp").value = "";
  push("user", esc(text));
  const typing = document.createElement("div");
  typing.className = "typing";
  typing.textContent = "V-Bot likh raha hai...";
  $("msgs").appendChild(typing);
  $("msgs").scrollTop = $("msgs").scrollHeight;
  setTimeout(() => { typing.remove(); push("bot", respond(text)); }, 350);
}
$("send").onclick = send;
$("inp").addEventListener("keydown", e => { if (e.key === "Enter") send(); });
$("bubble").onclick = () => setMode(true);
$("close").onclick = () => setMode(false);

const CHIPS = ["100000 me kya aata hai", "Honda CD 70", "sabse sasti car", "mehngi helicopter", "10 lakh combo"];
CHIPS.forEach(c => {
  const el = document.createElement("span");
  el.className = "chip";
  el.textContent = c;
  el.onclick = () => { $("inp").value = c; send(); };
  $("chips").appendChild(el);
});

/* ---------- boot ---------- */
setMode(false);
if (history.length) {
  history.forEach(m => push(m.who, m.html, false));
} else {
  push("bot", "👋 <b>Salam! Main V-Bot hoon</b> — aap ka vehicle assistant.<br>" +
              "Poochein: <i>budget me kya aata hai</i>, kisi vehicle ki <i>price</i>, ya <i>comparison</i>!<br>" +
              "<span class='hint'>Neeche chips par bhi click kar sakte hain 👇</span>");
}
</script>
</body>
</html>"""
