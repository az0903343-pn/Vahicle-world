# Vehicle Budget Recommender 🚗💰

Enter a budget in PKR and the app shows what you can buy - from a cycle to a helicopter -
including combinations such as *"2 cycles + 1 electric bike"* - with a **floating chatbot (V-Bot)**
in the corner that answers questions about any vehicle.

![App screenshot](https://img.shields.io/badge/Streamlit-Live%20App-red)

## What it does

| Feature | Description |
|---|---|
| 💰 Budget search | 173 vehicles (15 categories, ~90 brands) with approximate PKR prices, fuel type, seats and top speed |
| 🧩 Combination search | Knapsack-style search: *"2 cycles + 1 electric bike"* combos that use most of the budget |
| 🤖 V-Bot chatbot | Floating chat widget (bottom-right): budget queries, vehicle info, cheapest/most expensive, combos |
| 🧮 Random Forest | Estimates the price of a vehicle from its specs (trained on log10 of the price) |
| 🔎 KNN | Finds vehicles similar to a chosen one (category, fuel, price, speed, seats) |
| 🎨 Modern UI | Dark glassmorphism theme, vehicle cards, Plotly charts, quick budget presets |

## Files

```
app.py                      Streamlit app (modern UI + chatbot)
chatbot.py                  floating rule-based chatbot widget (V-Bot)
recommender.py              shared helper code (combos, KNN, price estimate, emoji map)
images.py                   real vehicle photos (hotlinked from Wikimedia Commons)
train_vehicle_model.ipynb   Kaggle notebook - trains and saves model.joblib
vehicles.csv                dataset (173 vehicles, 15 categories)
requirements.txt            packages for deployment
model.joblib                created by the Kaggle notebook (download it and add it here)
```

> **Photos:** vehicle cards and the chatbot show real photos (`images.py`). Each vehicle
> uses its own photo where available and falls back to a category photo otherwise
> (cycle, car, helicopter, ...). Emoji badges are still shown on top of each photo.

## 1. Train on Kaggle

1. Kaggle -> **Datasets -> New Dataset** -> upload `vehicles.csv`.
2. Kaggle -> **Code -> New Notebook** -> **File -> Import Notebook** -> upload `train_vehicle_model.ipynb`.
3. In the notebook click **Add Input** and add your dataset.
4. **Run All**. At the end the notebook saves `model.joblib`.
5. Open the **Output** tab and download `model.joblib`.

> Tip: the app also works without `model.joblib` - it retrains from `vehicles.csv`
> automatically on start-up (slightly slower first load).

## 2. Upload to GitHub

Create a new repository and upload: `app.py`, `chatbot.py`, `recommender.py`, `vehicles.csv`,
`requirements.txt`, `README.md`, `model.joblib` and the notebook.
All files go in the **root** of the repository (not inside a folder).

## 3. Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io and sign in with GitHub.
2. **Create app** -> choose your repository, branch `main`, main file `app.py`.
3. Click **Deploy**.

## Run locally (optional)

```
pip install -r requirements.txt
streamlit run app.py
```

## V-Bot chatbot examples

```
100000 me kya aata hai?      -> vehicles that fit the budget
Honda CD 70                  -> full info + similar vehicles
sabse sasti car              -> cheapest vehicle of a category
mehngi helicopter            -> most expensive vehicle
10 lakh combo                -> a combination that uses the budget
sabse tez bike               -> fastest vehicle
```

The chatbot is fully rule-based and reads from `vehicles.csv` - no API key needed.

## Notes and limitations

- **Prices are approximate estimates**, not live market prices (see the `source` and `date` columns).
  Update `vehicles.csv` with real prices before submitting, and write the date you checked them.
  If you change the number of rows, run the Kaggle notebook again; the app will otherwise retrain
  from the CSV automatically.
- The dataset is small, so the Random Forest price estimate is rough
  (5-fold cross-validation R2 is about 0.85 on the log scale, and a typical estimate is within a factor of ~3 of the real price).
- If `model.joblib` is missing or was made with a different scikit-learn version, the app trains the models again from `vehicles.csv` on start-up.
