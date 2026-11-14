"""
Floating chatbot widget for the Vehicle Budget Recommender.

How it works
------------
render_chatbot(df) embeds the vehicle dataset into a small self-contained
HTML/JavaScript app (a Streamlit component). The widget floats in the
bottom-right corner of the page:

- a pulsing round chat bubble, click it to open a glassy chat panel
- the chatbot is rule-based and answers in English, from the dataset itself
  (no API key, works offline, no cost). It understands phrases such as:
    * "what can I buy for 100000?"   -> best vehicles in that budget
    * "Honda CD 70"                  -> full info + similar vehicles
    * "cheapest car"                 -> cheapest vehicle of a category
    * "most expensive helicopter"    -> most expensive vehicle
    * "10 lakh combo"                -> a combination that uses the budget
    * "fastest bike"                 -> fastest vehicle
    * "how many vehicles?"           -> dataset stats
- chat history survives Streamlit re-runs (saved in localStorage)
"""
import json

import pandas as pd
import streamlit.components.v1 as components

import images
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
            "i": images.image_for(r["name"], r["category"]),
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
          border: 1px solid rgba(255,255,255,.1); border-radius: 10px; overflow: hidden; }
  .card::after { content: ""; display: block; clear: both; }
  .thumb { float: left; width: 40px; height: 30px; object-fit: cover; border-radius: 6px;
           margin: 2px 8px 0 0; border: 1px solid rgba(255,255,255,.2); }
  .card .row { display: flex; justify-content: space-between; gap: 8px; }
  .price { color: #4ade80; font-weight: 600; white-space: nowrap; }
  .hint { color: #94a3b8; font-size: 11px; }

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
      <button id="clr" title="Clear chat" style="margin-left:auto;background:rgba(255,255,255,.12);color:#fff;border:none;border-radius:8px;width:26px;height:26px;cursor:pointer;font-size:12px">🗑️</button>
      <button id="close">✕</button>
    </header>
    <div id="msgs"></div>
    <div id="chips"></div>
    <div id="row">
      <input id="inp" placeholder="Type your budget or a vehicle name...">
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
  const img = v.i ? '<img class="thumb" src="' + v.i + '" onerror="this.style.display=\'none\'">' : "";
  return '<div class="card">' + img + '<div class="row"><b>' + emoji(v.c) + " " + esc(v.n) +
         '</b><span class="price">' + money(v.p) + "</span></div>" +
         '<div class="hint">' + esc(v.c) + " · " + esc(v.f) + " · " + v.s +
         " seats · " + v.t + " km/h</div></div>";
}
function labelOf(cat) { return cat === "Cycle*" ? "cycle" : cat ? cat.toLowerCase() : "vehicle"; }

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

/* ---------- brain (English) ---------- */
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
  ["rickshaw|qingqi|loader", "Rickshaw"],
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
    if (new RegExp(keys).test(t)) return cat === "Cycle" ? "Cycle*" : cat;
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
    return "😅 No vehicle in the dataset fits that budget.<br>The cheapest option is:<br>" +
           card(cheapest) + "<span class='hint'>Try a budget of at least " + money(cheapest.p) + "!</span>";
  }
  let html = "💰 With a budget of <b>" + money(budget) + "</b> you can buy <b>" + pool.length +
             "</b> vehicles. Top picks:<br>";
  pool.slice(0, 6).forEach(v => { html += card(v); });
  const combo = [];
  let left = budget;
  for (const v of pool) {
    if (combo.length >= 3) break;
    if (v.p <= left) { combo.push(v); left -= v.p; }
  }
  if (combo.length > 1) {
    html += "<span class='hint'>💡 Smart combo: " + combo.map(v => emoji(v.c) + " " + esc(v.n)).join(" + ") + "</span>";
  }
  return html;
}
function catReply(cat) {
  const list = inCat(cat).sort((a, b) => a.p - b.p);
  let html = emoji(cat === "Cycle*" ? "Cycle" : cat) + " <b>" + labelOf(cat) +
             "</b> — " + list.length + " vehicles in the dataset.<br>" +
             "<span class='hint'>cheapest: " + esc(list[0].n) + " (" + money(list[0].p) +
             ") · most expensive: " + esc(list[list.length - 1].n) + " (" + money(list[list.length - 1].p) + ")</span><br>";
  list.slice(0, 4).forEach(v => { html += card(v); });
  return html;
}
function comboReply(budget) {
  const pool = V.filter(v => v.p <= budget).sort((a, b) => b.p - a.p);
  if (!pool.length) return "😅 No combo is possible with that budget.";
  const combo = []; let left = budget;
  for (const v of pool) {
    if (combo.length >= 3) break;
    if (v.p <= left) { combo.push(v); left -= v.p; }
  }
  let html = "🧩 A smart combo for <b>" + money(budget) + "</b>:<br>";
  combo.forEach(v => { html += card(v); });
  html += "<span class='hint'>Total " + money(budget - left) + " · left over " + money(left) + "</span>";
  return html;
}
function statsReply() {
  const cats = [...new Set(V.map(v => v.c))].length;
  const cheapest = [...V].sort((a, b) => a.p - b.p)[0];
  const dearest = [...V].sort((a, b) => b.p - a.p)[0];
  return "📊 <b>Dataset stats</b><br>" +
         "<div class='card'><div class='row'><span>🚙 Vehicles</span><b>" + V.length + "</b></div>" +
         "<div class='row'><span>🗂️ Categories</span><b>" + cats + "</b></div>" +
         "<div class='row'><span>💸 Cheapest</span><b>" + esc(cheapest.n) + "</b></div>" +
         "<div class='row'><span>👑 Most expensive</span><b>" + esc(dearest.n) + "</b></div></div>";
}
function respond(text) {
  const t = text.toLowerCase().trim();
  const tokens = t.split(/[^a-z0-9]+/).filter(Boolean);
  const GREETINGS = new Set(["hi", "hello", "hey", "salam", "salaam", "assalam", "asslam",
                             "asalam", "aoa", "as", "yo", "greetings"]);
  if (tokens.some(w => GREETINGS.has(w)))
    return "👋 <b>Hello! I'm V-Bot</b> — your vehicle assistant. I only talk vehicles!<br>" +
           "<span class='hint'>Try: <i>what can I buy for 100000</i>, <i>Honda CD 70</i>, " +
           "<i>cheapest car</i>, <i>most expensive helicopter</i></span>";
  if (/thank|shukriya|bye|khuda hafiz/.test(t))
    return "😊 You're welcome! Come back any time to talk about vehicles.";
  if (/help|what can you do|how do you work|examples/.test(t))
    return "🧠 I can answer questions about vehicles:<br>" +
           "<div class='card'>💬 <i>what can I buy for 150000?</i> — vehicles in your budget</div>" +
           "<div class='card'>🔍 <i>Honda CD 70</i> — full info + similar vehicles</div>" +
           "<div class='card'>💸 <i>cheapest car</i> / <i>most expensive helicopter</i></div>" +
           "<div class='card'>🧩 <i>10 lakh combo</i> — a combination for your budget</div>" +
           "<div class='card'>⚡ <i>fastest bike</i> · 📊 <i>how many vehicles</i></div>";

  const num = parseBudget(t);
  const cat = detectCat(t);

  if (/how many|dataset|stats|total vehicles|summary/.test(t)) return statsReply();

  if (/cheapest|lowest price|budget option|entry level/.test(t)) {
    const list = cat ? inCat(cat) : V;
    const v = [...list].sort((a, b) => a.p - b.p)[0];
    return "💸 The cheapest " + labelOf(cat) + ":<br>" + card(v);
  }
  if (/most expensive|priciest|costliest|top end|premium|luxury/.test(t)) {
    const list = cat ? inCat(cat) : V;
    const v = [...list].sort((a, b) => b.p - a.p)[0];
    return "👑 The most expensive " + labelOf(cat) + ":<br>" + card(v);
  }
  if (/fastest|top speed|quickest/.test(t)) {
    const list = cat ? inCat(cat) : V;
    const v = [...list].sort((a, b) => b.t - a.t)[0];
    return "⚡ The fastest " + labelOf(cat) + ":<br>" + card(v);
  }
  if (/combo|combin|mix/.test(t)) {
    if (num === null || num <= 1000)
      return "🧩 Tell me your budget and I'll build a combo — e.g. <i>'10 lakh combo'</i>.";
    return comboReply(num);
  }
  if (num !== null && num > 1000) return budgetReply(num);
  if (/what can i (buy|get)|suggest|recommend/.test(t))
    return "💰 Tell me your budget and I'll show you the options!<br>" +
           "<span class='hint'>e.g. <i>'what can I buy for 100000'</i></span>";

  const v = findVehicle(t);
  if (v) {
    const sim = V.filter(x => x.c === v.c && x.n !== v.n && x.p >= v.p * 0.5 && x.p <= v.p * 1.6)
                 .sort((a, b) => Math.abs(a.p - v.p) - Math.abs(b.p - v.p)).slice(0, 2);
    let html = emoji(v.c) + " <b>" + esc(v.n) + "</b><br>" +
               "<div class='card'><div class='row'><span>🏷️ " + esc(v.b) + " · " + esc(v.c) +
               "</span><span class='price'>" + money(v.p) + "</span></div>" +
               "<div class='hint'>⛽ " + esc(v.f) + " · 🪑 " + v.s + " seats · ⚡ top " + v.t + " km/h</div></div>";
    if (sim.length) html += "<span class='hint'>🔎 Similar vehicles:</span><br>" + sim.map(card).join("");
    return html;
  }
  if (cat) return catReply(cat);

  return "🤔 I didn't quite get that — I only know about <b>vehicles</b>! Try:<br>" +
         "<div class='card'>💰 <i>what can I buy for 100000</i></div>" +
         "<div class='card'>🔍 <i>Honda CD 70</i></div>" +
         "<div class='card'>🚁 <i>most expensive helicopter</i></div>";
}

/* ---------- UI wiring ---------- */
function send() {
  const text = $("inp").value.trim();
  if (!text) return;
  $("inp").value = "";
  push("user", esc(text));
  const typing = document.createElement("div");
  typing.className = "typing";
  typing.textContent = "V-Bot is typing...";
  $("msgs").appendChild(typing);
  $("msgs").scrollTop = $("msgs").scrollHeight;
  setTimeout(() => { typing.remove(); push("bot", respond(text)); }, 350);
}
$("send").onclick = send;
$("inp").addEventListener("keydown", e => { if (e.key === "Enter") send(); });
$("bubble").onclick = () => setMode(true);
$("close").onclick = () => setMode(false);
$("clr").onclick = () => {
  history = [];
  save();
  $("msgs").innerHTML = "";
  push("bot", "👋 <b>Chat cleared!</b> Ask me anything about vehicles — " +
              "budgets, prices, comparisons or specs.<br><span class='hint'>Try a chip below 👇</span>");
};

const CHIPS = ["What can I buy for 100000?", "Honda CD 70", "Cheapest car",
               "Most expensive helicopter", "10 lakh combo"];
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
  push("bot", "👋 <b>Hello! I'm V-Bot</b> — your vehicle assistant.<br>" +
              "Ask me about budgets, prices, comparisons or any vehicle in the dataset!<br>" +
              "<span class='hint'>You can also click a chip below 👇</span>");
}
</script>
</body>
</html>"""
