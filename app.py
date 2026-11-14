"""
Vehicle Budget Recommender - modern Streamlit app.

Enter a budget and see what you can buy - from a cycle all the way to a
helicopter - including combinations such as "2 cycles + 1 electric bike".
A floating chatbot (bottom-right) answers questions about the vehicles.
"""
import os

import pandas as pd
import plotly.express as px
import streamlit as st

import chatbot
import images
import recommender as rec

BASE = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Vehicle Budget Recommender",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------ theme
st.markdown(
    """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

  html, body, .stApp, .stApp * { font-family: 'Poppins', 'Segoe UI', sans-serif !important; }

  .stApp {
      background:
        radial-gradient(1100px 700px at 85% -10%, rgba(99,102,241,.28), transparent 60%),
        radial-gradient(900px 600px at -10% 110%, rgba(168,85,247,.22), transparent 60%),
        radial-gradient(600px 400px at 50% 120%, rgba(236,72,153,.12), transparent 60%),
        linear-gradient(160deg, #0b1020 0%, #101532 45%, #0a0f1e 100%) !important;
      color: #e6edf7;
  }
  .stSidebar { background: rgba(8,11,26,.92) !important; border-right: 1px solid rgba(255,255,255,.08); }
  .stSidebar * { color: #dbe3f4 !important; }

  /* glass cards */
  .glass {
      background: linear-gradient(145deg, rgba(255,255,255,.09), rgba(255,255,255,.03));
      border: 1px solid rgba(255,255,255,.12); border-radius: 18px;
      padding: 18px 20px; backdrop-filter: blur(12px);
      box-shadow: 0 10px 30px rgba(0,0,0,.25);
  }
  .glass:hover { border-color: rgba(139,92,246,.55); }

  /* gradient headline */
  .hero-title {
      font-size: 3.2rem; font-weight: 800; line-height: 1.15; margin: 0;
      background: linear-gradient(90deg, #818cf8, #c084fc 45%, #f472b6);
      -webkit-background-clip: text; background-clip: text; color: transparent;
  }
  .hero-sub { color: #9fb0d8; font-size: 1.05rem; margin-top: 8px; }

  /* metric pills */
  .metric { text-align: center; padding: 14px 10px; }
  .metric .num { font-size: 1.7rem; font-weight: 800; color: #fff; }
  .metric .lbl { font-size: .8rem; color: #9fb0d8; letter-spacing: .4px; text-transform: uppercase; }

  /* vehicle cards */
  .veh-card {
      background: linear-gradient(150deg, rgba(255,255,255,.085), rgba(255,255,255,.025));
      border: 1px solid rgba(255,255,255,.11); border-radius: 16px;
      padding: 14px 15px; height: 100%; transition: all .25s ease;
  }
  .veh-card:hover { transform: translateY(-4px); border-color: rgba(139,92,246,.65);
      box-shadow: 0 12px 28px rgba(99,102,241,.25); }
  .veh-card .vname { font-weight: 600; color: #fff; font-size: .95rem; line-height: 1.3; }
  .veh-card .vprice { font-size: 1.05rem; font-weight: 800; color: #4ade80; margin: 7px 0 3px; }
  .veh-card .vmeta { color: #9fb0d8; font-size: .76rem; line-height: 1.5; }
  .vtag { display: inline-block; font-size: .68rem; padding: 2px 9px; border-radius: 20px;
      background: rgba(99,102,241,.2); border: 1px solid rgba(129,140,248,.35); color: #cbd5ff;
      margin-top: 8px; }

  /* vehicle photo */
  .vimg { position: relative; height: 130px; border-radius: 12px; overflow: hidden;
      margin-bottom: 10px; background: rgba(255,255,255,.05); }
  .vimg img { width: 100%; height: 100%; object-fit: cover; transition: transform .45s ease; }
  .veh-card:hover .vimg img { transform: scale(1.09); }
  .vimg .vicon { position: absolute; top: 8px; right: 8px; width: 34px; height: 34px;
      display: flex; align-items: center; justify-content: center; font-size: 1.05rem;
      background: rgba(10,12,30,.7); border-radius: 50%; backdrop-filter: blur(4px); }
  .vnoimg { display: flex; align-items: center; justify-content: center;
      background: linear-gradient(135deg, rgba(99,102,241,.28), rgba(168,85,247,.22)); }
  .vnoimg .vicon { position: static; font-size: 2.8rem; width: auto; height: auto;
      background: none; backdrop-filter: none; }

  /* category banner */
  .banner { display: flex; gap: 9px; overflow-x: auto; padding: 10px 2px 14px; }
  .banner-img { position: relative; flex: 0 0 auto; width: 168px; height: 100px;
      border-radius: 14px; overflow: hidden; border: 1px solid rgba(255,255,255,.16);
      box-shadow: 0 8px 20px rgba(0,0,0,.35); }
  .banner-img img { width: 100%; height: 100%; object-fit: cover; transition: transform .45s ease; }
  .banner-img:hover img { transform: scale(1.1); }
  .banner-img span { position: absolute; left: 9px; bottom: 7px; font-size: .74rem;
      font-weight: 700; color: #fff; text-shadow: 0 1px 5px rgba(0,0,0,.9); }

  /* combo card */
  .combo-item { display: flex; justify-content: space-between; gap: 10px;
      padding: 6px 0; border-bottom: 1px dashed rgba(255,255,255,.12); font-size: .9rem; }
  .combo-item:last-child { border-bottom: none; }

  /* inputs & widgets on dark */
  .stButton>button { border-radius: 12px; border: 1px solid rgba(139,92,246,.4);
      background: rgba(99,102,241,.12); color: #e0e7ff; font-weight: 600; width: 100%; }
  .stButton>button:hover { background: rgba(99,102,241,.35); border-color: #8b5cf6; }
  .stButton>button[kind="primary"] { background: linear-gradient(135deg,#6366f1,#a855f7); border: none; }
  div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="slider"] { color: #e6edf7; }
  .stTabs [data-baseweb="tab-list"] { gap: 6px; }
  .stTabs [data-baseweb="tab"] { border-radius: 12px 12px 0 0; padding: 8px 18px;
      background: rgba(255,255,255,.05); color: #9fb0d8; font-weight: 600; }
  .stTabs [aria-selected="true"] { background: linear-gradient(135deg, rgba(99,102,241,.4), rgba(168,85,247,.3));
      color: #fff !important; }
  ::-webkit-scrollbar { width: 8px; }
  ::-webkit-scrollbar-thumb { background: rgba(139,92,246,.4); border-radius: 4px; }
</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------ data & models
@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(BASE, "vehicles.csv"))


@st.cache_resource
def load_models():
    # loads model.joblib (trained on Kaggle); trains again from the CSV if the file is missing
    return rec.load_or_train(load_data(), os.path.join(BASE, "model.joblib"))


df = load_data()
bundle, model_source = load_models()


def veh_card(row, budget=None):
    """One glassy vehicle card with a real photo (category photo as fallback)."""
    brand = row.get("brand", "")
    brand_txt = f" · {brand}" if brand else ""
    img = images.image_for(row["name"], row["category"])
    if img:
        img_html = (
            f"<div class='vimg'><img src='{img}' alt='' loading='lazy'>"
            f"<span class='vicon'>{rec.emoji(row['category'])}</span></div>"
        )
    else:
        img_html = (
            f"<div class='vimg vnoimg'>"
            f"<span class='vicon'>{rec.emoji(row['category'])}</span></div>"
        )
    qty = ""
    if budget:
        n = int(budget // row["price_pkr"])
        if n > 1:
            qty = f"<div class='vmeta'>🛒 You can buy up to <b>{n}</b></div>"
    return (
        f"<div class='veh-card'>"
        f"{img_html}"
        f"<div class='vname'>{row['name']}</div>"
        f"<div class='vprice'>{rec.money(row['price_pkr'])}</div>"
        f"<div class='vmeta'>⛽ {row['fuel_type']} · 🪑 {row['seats']} seats · ⚡ {row['top_speed_kmh']} km/h</div>"
        f"{qty}<span class='vtag'>{row['category']}{brand_txt}</span>"
        f"</div>"
    )


def card_grid(frame, budget=None, per_row=4):
    rows = frame.to_dict("records")
    for i in range(0, len(rows), per_row):
        cols = st.columns(per_row)
        for col, row in zip(cols, rows[i : i + per_row]):
            col.markdown(veh_card(row, budget), unsafe_allow_html=True)


# ------------------------------------------------------------------ sidebar
PRESETS = [
    ("1 Lakh", 100_000), ("5 Lakh", 500_000), ("10 Lakh", 1_000_000),
    ("50 Lakh", 5_000_000), ("1 Crore", 10_000_000), ("10 Crore", 100_000_000),
    ("50 Crore", 500_000_000), ("100 Crore", 1_000_000_000),
]

with st.sidebar:
    st.markdown("## 💰 Your Budget")
    pc1, pc2, pc3, pc4 = st.columns(4)
    for i, (label, value) in enumerate(PRESETS):
        [pc1, pc2, pc3, pc4][i % 4].button(label, key=f"pre_{i}")
    clicked = [k for k in [f"pre_{i}" for i in range(len(PRESETS))] if st.session_state.get(k)]
    if clicked:
        st.session_state["budget_in"] = PRESETS[int(clicked[0].split("_")[1])][1]

    budget = st.number_input(
        "Budget (PKR)", min_value=5_000, max_value=100_000_000_000,
        value=150_000, step=10_000, key="budget_in",
    )
    st.markdown(
        f"<div class='glass' style='text-align:center'><div class='num' style='color:#4ade80;font-size:1.2rem'>{rec.money(budget)}</div></div>",
        unsafe_allow_html=True,
    )

    st.markdown("## ⚙️ Options")
    all_categories = sorted(df["category"].unique())
    chosen = st.multiselect("Only these categories (empty = all)", all_categories)
    max_items = st.slider("Max vehicles in one combination", 1, 4, 3)
    min_spend = st.slider("Use at least this much of the budget (%)", 50, 100, 85, step=5)

    stats = rec.dataset_stats(df)
    st.markdown("## 📊 Dataset")
    st.caption(
        f"🚙 {stats['vehicles']} vehicles · 🗂️ {stats['categories']} categories · "
        f"🏭 {stats['brands']} brands"
    )
    st.caption(
        "Prices are approximate market estimates (see `date` and `source` in the dataset) "
        "and change often. Verify before buying."
    )

pool = df[df["category"].isin(chosen)] if chosen else df
affordable = pool[pool["price_pkr"] <= budget].sort_values("price_pkr", ascending=False)

# ------------------------------------------------------------------ header
st.markdown(
    "<div style='margin: 6px 0 4px'>"
    "<h1 class='hero-title'>🚗 Vehicle Budget Recommender</h1>"
    "<div class='hero-sub'>Enter your budget and see what you can buy — from a cycle "
    "all the way to a helicopter. Ask <b>V-Bot</b> (bottom-right corner) anything!</div>"
    "</div>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ metric pills
m1, m2, m3, m4 = st.columns(4)
if len(affordable):
    m1.markdown(f"<div class='glass metric'><div class='num'>{len(affordable)}</div><div class='lbl'>Vehicles you can afford</div></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='glass metric'><div class='num'>{affordable['category'].nunique()}</div><div class='lbl'>Categories fit</div></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='glass metric'><div class='num' style='color:#4ade80'>{rec.money(affordable['price_pkr'].max())}</div><div class='lbl'>Best you can buy</div></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='glass metric'><div class='num' style='color:#c084fc'>{rec.money(pool['price_pkr'].min())}</div><div class='lbl'>Cheapest overall</div></div>", unsafe_allow_html=True)
else:
    m1.markdown("<div class='glass metric'><div class='num'>0</div><div class='lbl'>Vehicles you can afford</div></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='glass metric'><div class='num'>{rec.money(pool['price_pkr'].min())}</div><div class='lbl'>Cheapest in filter</div></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='glass metric'><div class='num' style='color:#f472b6'>{rec.money(max(pool['price_pkr'].min() - budget, 0))}</div><div class='lbl'>You are short by</div></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='glass metric'><div class='num'>{pool['category'].nunique()}</div><div class='lbl'>Categories in filter</div></div>", unsafe_allow_html=True)

st.write("")

# photo banner: one featured photo per category
BANNER_ORDER = ["Cycle", "Petrol Bike", "Car", "Van", "Rickshaw", "Heavy Bike",
                "Boat", "Tractor", "Helicopter", "Aircraft", "Jet", "Electric Bike", "Scooter"]
banner = "".join(
    f"<div class='banner-img'><img src='{images.CATEGORY_IMAGES[c]}' alt=''>"
    f"<span>{rec.emoji(c)} {c}</span></div>"
    for c in BANNER_ORDER
    if c in images.CATEGORY_IMAGES
)
st.markdown(f"<div class='banner'>{banner}</div>", unsafe_allow_html=True)

tab_buy, tab_combo, tab_similar, tab_price, tab_data = st.tabs(
    ["🛒  What can I buy?", "🧩  Combinations", "🔎  Similar vehicles (KNN)",
     "🧮  Price estimator (Random Forest)", "🗂️  Dataset"]
)

# ------------------------------------------------------------------ tab 1
with tab_buy:
    if affordable.empty:
        st.info("Nothing in the dataset fits this budget yet. Try a higher budget or clear the category filter.")
    else:
        counts = affordable["category"].value_counts()
        fig = px.bar(
            x=counts.values, y=counts.index, orientation="h",
            labels={"x": "Vehicles in budget", "y": "Category"},
            color=counts.values, color_continuous_scale="Viridis", text=counts.values,
        )
        fig.update_layout(
            height=420, template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins"), margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.subheader("Everything that fits your budget")
        for category, group in affordable.groupby("category", sort=False):
            st.markdown(
                f"<div style='font-weight:700;color:#c7d2fe;margin:12px 0 6px'>"
                f"{rec.emoji(category)} {category} <span style='color:#64748b'>({len(group)})</span></div>",
                unsafe_allow_html=True,
            )
            card_grid(group, budget=budget)

# ------------------------------------------------------------------ tab 2
with tab_combo:
    st.subheader("Ways to spend your budget")
    st.caption(
        f"Combinations of up to {max_items} vehicles that use at least {min_spend}% of your budget. "
        "The same vehicle can be repeated (e.g. 2 cycles)."
    )
    combos = rec.find_combos(pool, budget, max_items=max_items, min_spend_ratio=min_spend / 100)
    if not combos:
        st.info("No combination found. Try lowering the 'use at least' percentage or raising the budget.")
    for rank, combo in enumerate(combos, 1):
        items_html = "".join(
            f"<div class='combo-item'><span>{rec.emoji(it['category'])} <b>{it['qty']} × {it['name']}</b>"
            f"<br><span style='color:#9fb0d8;font-size:.75rem'>{it['category']}</span></span>"
            f"<span style='color:#4ade80;font-weight:600'>{rec.money(it['unit_price'])}</span></div>"
            for it in combo["items"]
        )
        st.markdown(
            f"<div class='glass' style='margin-bottom:12px'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center'>"
            f"<div style='font-weight:700;color:#fff'>🧩 Combo #{rank}</div>"
            f"<div><span style='color:#4ade80;font-weight:700'>Total {rec.money(combo['total'])}</span>"
            f"<span style='color:#9fb0d8;font-size:.8rem'> &nbsp;·&nbsp; left over {rec.money(combo['remaining'])}</span></div>"
            f"</div><div style='margin-top:8px'>{items_html}</div></div>",
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------ tab 3
with tab_similar:
    st.subheader("Find similar vehicles")
    st.caption(
        "K-Nearest Neighbours compares category, fuel type, price, top speed and seats "
        "and returns the closest matches."
    )
    pick = st.selectbox("Pick a vehicle", df.sort_values("price_pkr")["name"].tolist())
    only_budget = st.checkbox("Only show vehicles within my budget", value=True)
    similar = rec.similar_vehicles(df, bundle, pick, max_price=budget if only_budget else None, k=6)
    if similar.empty:
        st.info("No similar vehicle fits inside your budget.")
    else:
        card_grid(similar, budget=budget)

# ------------------------------------------------------------------ tab 4
with tab_price:
    st.subheader("Estimate the price of a vehicle")
    st.caption(
        "A Random Forest trained on the dataset guesses a price from the specs. "
        "With a few hundred vehicles this is still a rough estimate."
    )
    a, b, c = st.columns(3)
    category = a.selectbox("Category", all_categories)
    fuel = b.selectbox("Fuel type", sorted(df["fuel_type"].unique()))
    seats = c.number_input("Seats", min_value=1, max_value=60, value=2, step=1)
    speed = a.number_input("Top speed (km/h)", min_value=5, max_value=1500, value=100, step=5)
    if st.button("🧮 Estimate price", type="primary"):
        estimate = rec.predict_price(bundle, category, fuel, seats, speed)
        st.markdown(
            f"<div class='glass metric' style='margin-top:10px'>"
            f"<div class='num' style='color:#4ade80'>{rec.money(estimate)}</div>"
            f"<div class='lbl'>Estimated price ({category} · {fuel})</div></div>",
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------ tab 5
with tab_data:
    st.subheader("Dataset")
    show = df[["name", "category", "brand", "price_pkr", "fuel_type", "seats", "top_speed_kmh", "source", "date"]]
    st.dataframe(show, hide_index=True, use_container_width=True)
    st.download_button("Download vehicles.csv", df.to_csv(index=False), file_name="vehicles.csv")

# ------------------------------------------------------------------ footer + chatbot
st.markdown(
    "<div style='text-align:center;color:#64748b;font-size:.8rem;margin:26px 0 8px'>"
    "Built with Streamlit · Random Forest + KNN · trained on Kaggle · "
    "prices are approximate market estimates</div>",
    unsafe_allow_html=True,
)
chatbot.render_chatbot(df)
