import sqlite3
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-whitegrid")

conn = sqlite3.connect("recalls.db")
cur = conn.cursor()

# Restrict the yearly chart to records from 2003 onward.
cur.execute(
    """
    SELECT strftime('%Y', event_date_initiated) AS year, COUNT(*) AS count
    FROM recalls
    WHERE strftime('%Y', event_date_initiated) >= '2003'
    GROUP BY year
    ORDER BY year ASC
    """
)
yearly_results = cur.fetchall()

years = [row[0] for row in yearly_results]
counts = [row[1] for row in yearly_results]

plt.figure(figsize=(10, 5))
bars = plt.bar(years, counts, color="#4C72B0")
for bar in bars:
    bar_height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar_height,
        f"{int(bar_height)}",
        ha="center",
        va="bottom",
        fontsize=9,
    )

plt.annotate(
    "2 firms drove this spike",
    xy=("2018", 32),
    xytext=("2015", 45),
    arrowprops=dict(arrowstyle="->"),
)
plt.title("Device Recall Volume by Year")
plt.xlabel("Year")
plt.ylabel("Number of Recalls")
plt.xticks(rotation=45, ha="right")
avg_count = sum(counts) / len(counts)
plt.axhline(
    y=avg_count,
    color="red",
    linestyle="--",
    linewidth=1,
    label=f"Average: {avg_count:.0f}/year",
)
plt.legend()
plt.tight_layout()
plt.figtext(0.5, -0.05, "Source: openFDA Device Recalls API", ha="center", fontsize=8)
plt.savefig("charts/volume_by_year.png", bbox_inches="tight")
print("Saved chart to charts/volume_by_year.png")

# Compare the average time to recall across the top 10 root causes.
cur.execute(
    """
    SELECT root_cause_description,
           AVG(julianday(event_date_terminated) - julianday(event_date_initiated)) AS days,
           COUNT(*) AS num_recalls
    FROM recalls
    WHERE event_date_terminated IS NOT NULL
      AND event_date_initiated IS NOT NULL
      AND root_cause_description IN (
          SELECT root_cause_description
          FROM recalls
          GROUP BY root_cause_description
          ORDER BY COUNT(*) DESC
          LIMIT 10
      )
    GROUP BY root_cause_description
    ORDER BY days ASC
    """
)

root_cause_results = cur.fetchall()

causes = [row[0] for row in root_cause_results]
days_to_recall = [row[1] for row in root_cause_results]

# Shorten a long label so the chart remains readable.
label_map = {
    "Radiation Control for Health and Safety Act": "Radiation Control",
}
causes_short = [label_map.get(cause, cause) for cause in causes]

plt.figure(figsize=(10, 5))
plt.barh(causes_short, days_to_recall, color="#4C72B0")
plt.title("Time to Recall by Root Cause")
plt.xlabel("Number of Days to recall")
plt.ylabel("Root Cause")
plt.xticks(rotation=45, ha="right")
avg_days = sum(days_to_recall) / len(days_to_recall)
plt.axvline(
    x=avg_days,
    color="red",
    linestyle="--",
    linewidth=1,
    label=f"Avg (top 10 causes): {avg_days:.0f} days",
)
plt.legend(loc="lower right", framealpha=1, facecolor="white", edgecolor="black")
plt.tight_layout()
plt.figtext(0.5, -0.05, "Source: openFDA Device Recalls API", ha="center", fontsize=8)
plt.savefig("charts/Time_by_Root_Cause.png", bbox_inches="tight")
print("Saved chart to charts/Time_by_Root_Cause.png")

conn.close()
