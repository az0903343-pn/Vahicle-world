"""
Vehicle budget recommender - helper code shared by the Kaggle notebook and the Streamlit app.

What it does
------------
1. find_combos()       : given a budget, finds combinations such as "2 cycles + 1 electric bike"
2. similar_vehicles()  : KNN (K-Nearest Neighbours) - finds vehicles similar to a chosen one
3. predict_price()     : Random Forest - estimates the price of a vehicle from its specs
4. train_models()      : trains the Random Forest + KNN and returns them in one dictionary
"""
import itertools
import os
from collections import Counter

import joblib
import numpy as np
import pandas as pd

# ==== HELPERS START ====
PRICE_FEATURES = ["category", "fuel_type", "top_speed_kmh", "seats"]
SIMILARITY_FEATURES = ["category", "fuel_type", "log_price", "top_speed_kmh", "seats"]

CATEGORY_EMOJI = {
    "Generic Cycle": "🚲",
    "Cycle": "🚲",
    "Electric Bike": "🛴",
    "Scooter": "🛵",
    "Petrol Bike": "🏍️",
    "Heavy Bike": "🏍️",
    "Rickshaw": "🛺",
    "Van": "🚐",
    "Car": "🚗",
    "Bus/Truck": "🚚",
    "Tractor": "🚜",
    "Boat": "🚤",
    "Helicopter": "🚁",
    "Aircraft": "✈️",
    "Jet": "🛩️",
}


def emoji(category):
    """Returns a matching emoji for a vehicle category."""
    return CATEGORY_EMOJI.get(category, "🚗")


def vehicle_info(df, name):
    """Returns the full row of a vehicle as a dict, or None if not found."""
    matches = df[df["name"].str.lower() == str(name).strip().lower()]
    if matches.empty:
        return None
    return matches.iloc[0].to_dict()


def search_vehicles(df, query, limit=6):
    """Fuzzy search: vehicles whose name contains the query (case-insensitive)."""
    q = str(query).strip().lower()
    if not q:
        return df.iloc[0:0]
    hits = df[df["name"].str.lower().str.contains(q, regex=False)]
    return hits.sort_values("price_pkr").head(limit)


def dataset_stats(df):
    """Small summary used by the app header and the chatbot."""
    return {
        "vehicles": int(len(df)),
        "categories": int(df["category"].nunique()),
        "brands": int(df["brand"].nunique()),
        "cheapest": float(df["price_pkr"].min()),
        "most_expensive": float(df["price_pkr"].max()),
    }


def add_features(df):
    """Adds log_price. Prices range from Rs 15,000 to Rs 19 billion, so we use log10."""
    data = df.copy().reset_index(drop=True)
    data["log_price"] = np.log10(data["price_pkr"])
    return data


def money(x):
    """Rs 150,000 (1.50 lakh) / Rs 3,000,000 (30.00 lakh) / Rs 90,000,000 (9.00 crore) ..."""
    x = float(x)
    if x >= 1e9:
        words = f"{x / 1e9:.2f} arab"
    elif x >= 1e7:
        words = f"{x / 1e7:.2f} crore"
    elif x >= 1e5:
        words = f"{x / 1e5:.2f} lakh"
    else:
        words = None
    text = f"Rs {x:,.0f}"
    return f"{text} ({words})" if words else text


def find_combos(df, budget, max_items=3, top_n=10, min_spend_ratio=0.85, pool_size=40):
    """
    Finds combinations of vehicles whose total price fits inside the budget.

    - The same vehicle can be repeated (e.g. 2 cycles).
    - A combination must use at least `min_spend_ratio` of the budget (default 85%),
      otherwise "1 cheap cycle" would always be a valid answer.
    - Combinations are ranked by: how much of the budget is used + how many
      different vehicle categories they contain (variety).
    - At most 2 combinations with the same category mix are shown.
    """
    pool = df[df["price_pkr"] <= budget].sort_values("price_pkr").reset_index(drop=True)
    if pool.empty:
        return []

    # keep the search fast for big budgets: spread the pool evenly across the price range
    if len(pool) > pool_size:
        keep = np.unique(np.linspace(0, len(pool) - 1, pool_size).round().astype(int))
        pool = pool.iloc[keep].reset_index(drop=True)

    names = pool["name"].tolist()
    prices = pool["price_pkr"].to_numpy()
    cats = pool["category"].tolist()

    found = []
    for size in range(1, max_items + 1):
        for combo in itertools.combinations_with_replacement(range(len(pool)), size):
            total = float(sum(prices[i] for i in combo))
            if total > budget or total < min_spend_ratio * budget:
                continue
            variety = len({cats[i] for i in combo})
            score = total / budget + 0.10 * variety
            found.append((score, combo, total))

    found.sort(key=lambda t: t[0], reverse=True)

    results, mix_count = [], Counter()
    for score, combo, total in found:
        mix = tuple(sorted(cats[i] for i in combo))
        if mix_count[mix] >= 2:
            continue
        mix_count[mix] += 1
        counts = Counter(combo)
        items = [
            {"name": names[i], "category": cats[i], "qty": q, "unit_price": float(prices[i])}
            for i, q in counts.items()
        ]
        summary = " + ".join(f"{it['qty']} x {it['name']}" for it in items)
        results.append(
            {"summary": summary, "items": items, "total": total, "remaining": float(budget - total)}
        )
        if len(results) >= top_n:
            break
    return results


def similar_vehicles(df, bundle, name, max_price=None, k=5):
    """KNN: the k vehicles most similar to `name` (category, fuel, price, speed, seats)."""
    data = add_features(df)
    X = bundle["feat"].transform(data[SIMILARITY_FEATURES])
    pos = int(np.where(data["name"] == name)[0][0])
    _, idx = bundle["knn"].kneighbors(X[[pos]], n_neighbors=len(data))
    rows = [i for i in idx[0] if i != pos]
    out = data.iloc[rows]
    if max_price is not None:
        out = out[out["price_pkr"] <= max_price]
    return out.head(k)[["name", "category", "price_pkr", "fuel_type", "seats", "top_speed_kmh"]]


def predict_price(bundle, category, fuel_type, seats, top_speed_kmh):
    """Random Forest price estimate in PKR."""
    row = pd.DataFrame(
        [{"category": category, "fuel_type": fuel_type, "top_speed_kmh": top_speed_kmh, "seats": seats}]
    )
    return float(10 ** bundle["price_model"].predict(row[PRICE_FEATURES])[0])
# ==== HELPERS END ====


def train_models(df):
    """Trains the Random Forest (price estimator) and the KNN (similar vehicles)."""
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.neighbors import NearestNeighbors
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    data = add_features(df)

    price_model = Pipeline(
        [
            (
                "pre",
                ColumnTransformer(
                    [
                        ("cat", OneHotEncoder(handle_unknown="ignore"), ["category", "fuel_type"]),
                        ("num", "passthrough", ["top_speed_kmh", "seats"]),
                    ]
                ),
            ),
            ("rf", RandomForestRegressor(n_estimators=300, random_state=42)),
        ]
    )
    price_model.fit(data[PRICE_FEATURES], data["log_price"])

    feat = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["category", "fuel_type"]),
            ("num", StandardScaler(), ["log_price", "top_speed_kmh", "seats"]),
        ]
    )
    X = feat.fit_transform(data[SIMILARITY_FEATURES])
    knn = NearestNeighbors(metric="euclidean").fit(X)

    return {"price_model": price_model, "feat": feat, "knn": knn, "n_rows": len(data)}


def load_or_train(df, model_path="model.joblib"):
    """
    Loads model.joblib (trained on Kaggle). If the file is missing, was made with a
    different scikit-learn version, or the dataset has changed, it trains again from the CSV.
    """
    if os.path.exists(model_path):
        try:
            bundle = joblib.load(model_path)
            if bundle.get("n_rows") == len(df):
                return bundle, "model.joblib (trained on Kaggle)"
        except Exception:
            pass
    return train_models(df), "trained again from vehicles.csv"
