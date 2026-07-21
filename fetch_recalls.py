import requests
import pandas as pd
import time
BASE_URL = "https://api.fda.gov/device/recall.json"
def fetch_recalls(limit=100, max_records=500):
    all_results = []
    skip = 0

    while skip < max_records:
        params = {"limit": limit, "skip": skip}
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)
        skip += limit
        time.sleep(0.5)

    return all_results

if __name__ == "__main__":
    records = fetch_recalls()
    df = pd.DataFrame(records)
    df.to_csv("device_recalls_raw.csv", index=False)
    print(f"Saved {len(df)} records to device_recalls_raw.csv")
