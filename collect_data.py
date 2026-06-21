import requests
import pandas as pd
import time

APP_ID          = 264710
POSITIVE_TARGET = 200
NEGATIVE_TARGET = 100
SINCE_DATE      = 1777636800  # June 1, 2026 (Unix timestamp)


def collect_reviews(review_type, target):
    cursor  = "*"
    results = []
    label   = ""  # filled in manually after reading

    print(f"\nCollecting {target} {review_type} reviews...")

    while True:  # collect everything in date range, sample later
        params = {
            "json":          1,
            "num_per_page":  100,
            "language":      "english",
            "filter":        "recent",
            "review_type":   review_type,
            "purchase_type": "steam",
            "cursor":        cursor,
        }

        try:
            r = requests.get(
                f"https://store.steampowered.com/appreviews/{APP_ID}",
                params=params,
                timeout=15,
            )
        except requests.exceptions.RequestException as e:
            print(f"  Request failed: {e}")
            break

        if r.status_code != 200:
            print(f"  Got {r.status_code} — stopping")
            break

        data  = r.json()
        items = data.get("reviews", [])

        if not items:
            print("  No more reviews.")
            break

        too_old = 0
        for item in items:
            ts = item.get("timestamp_created", 0)
            if ts < SINCE_DATE:
                too_old += 1
                continue

            text = " ".join(item.get("review", "").split()).strip()
            if not text:
                continue

            results.append({"text": text, "label": label, "notes": ""})

        if too_old == len(items):
            print("  Reached cutoff date — stopping.")
            break

        cursor = data.get("cursor", "")
        if not cursor:
            print("  No more pages.")
            break

        print(f"  {review_type} collected so far: {len(results)}")
        time.sleep(0.5)

    df = pd.DataFrame(results).drop_duplicates(subset="text")
    if len(df) < target:
        print(f"  ⚠️  Only found {len(df)} {review_type} reviews in date range "
              f"(needed {target}). Consider extending SINCE_DATE.")
        return df

    return df.sample(n=target, random_state=None)  # random_state=None = different each run


pos_df = collect_reviews("positive", POSITIVE_TARGET)
neg_df = collect_reviews("negative", NEGATIVE_TARGET)

df = pd.concat([pos_df, neg_df], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle

df.to_csv("steam_reviews.csv", index=False)
print(f"\nSaved {len(df)} reviews to steam_reviews.csv")
print(f"  positive: {len(pos_df)}  |  negative: {len(neg_df)}")
print(df.head(5).to_string())
