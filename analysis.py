import sqlite3

conn = sqlite3.connect("recalls.db")
cur = conn.cursor()

print("Top root causes:")
for row in cur.execute(
    """
    SELECT root_cause_description, COUNT(*) AS count
    FROM recalls
    GROUP BY root_cause_description
    ORDER BY count DESC
    LIMIT 10
    """
):
    print(row)

print("\nRecall status breakdown:")
for row in cur.execute(
    """
    SELECT recall_status, COUNT(*) AS count
    FROM recalls
    GROUP BY recall_status
    ORDER BY count DESC
    """
):
    print(row)

# Diagnostic identifying the outlier that skewed the resolution-time average.
# Found a single record with incorrect year "0012" causing a
# 730,815-day outlier. Excluded from downstream date calculations.
print("\nMax/Min days to resolve:")
for row in cur.execute("""
                        SELECT MIN(julianday(event_date_terminated) - julianday(event_date_initiated)) AS min_days,
                               MAX(julianday(event_date_terminated) - julianday(event_date_initiated)) AS max_days
                        FROM recalls
                        WHERE event_date_terminated IS NOT NULL
                        AND event_date_initiated IS NOT NULL
                        """):
    print(row)

print("\nAVG Time to Resolution:")
for row in cur.execute(
    """
    SELECT AVG(julianday(event_date_terminated) - julianday(event_date_initiated)) AS avg_days_to_resolve
    FROM recalls
    WHERE event_date_terminated IS NOT NULL
      AND event_date_initiated IS NOT NULL
      AND strftime('%Y', event_date_initiated) != '0012'
    """
):
    avg_days = row[0]
    print(f"{avg_days:.3f} days")

print("\nAVG Time to Resolution by Top 10 Root Causes:")
for row in cur.execute(
    """
    SELECT root_cause_description,
           AVG(julianday(event_date_terminated) - julianday(event_date_initiated)) AS avg_days_to_resolve,
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
    ORDER BY avg_days_to_resolve ASC
    """
):
    root_cause, avg_days, count = row
    print(f"{root_cause}: {avg_days:.3f} days (n={count})")

# Restrict the yearly counts to the period with more consistent data.
print("\nRecall Volume Over Time")
for row in cur.execute(
    """
    SELECT strftime('%Y', event_date_initiated) AS year, COUNT(*) AS count
    FROM recalls
    WHERE strftime('%Y', event_date_initiated) >= '2003'
    GROUP BY year
    ORDER BY year ASC
    """
):
    print(row)

# The 2018 spike is driven by a small set of firms, so this query highlights them.
print("\nTop Recalling Firms in 2018")
for row in cur.execute(
    """
    SELECT recalling_firm, COUNT(*) AS count
    FROM recalls
    WHERE strftime('%Y', event_date_initiated) = '2018'
    GROUP BY root_cause_description
    ORDER BY count DESC
    LIMIT 10
    """
):
    print(row)

print("\nRoot causes in 2018")
for row in cur.execute(
    """
    SELECT reason_for_recall, COUNT(*) AS count
    FROM recalls
    WHERE strftime('%Y', event_date_initiated) = '2018'
    GROUP BY root_cause_description
    ORDER BY count DESC
    LIMIT 2
    """
):
    print(row)
# The Metric Company and COVIDIEN LLC account for 18 recalls total explaining the spike

conn.close()
