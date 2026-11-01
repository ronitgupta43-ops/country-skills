"""Engagement rate and a CPM-based price range for a sponsored post.
Usage: python rates.py posts.csv --followers 25000 --cpm-low 15 --cpm-high 30
posts.csv columns: views,likes,comments,saves,shares   (one row per recent post, 10 to 20 posts)
CPM = price per 1,000 views. Use rates from the creator's own past deals or the brand's budget; this script doesn't invent them.
"""
import argparse
import csv
from statistics import median


def stats(rows, followers):
    eng = [sum(float(r.get(k) or 0) for k in ("likes", "comments", "saves", "shares")) for r in rows]
    views = [float(r["views"]) for r in rows]
    return {
        "median_views": median(views),
        "engagement_rate_followers": median(eng) / followers,
        "engagement_rate_views": median(e / v for e, v in zip(eng, views) if v),
    }


def price_range(median_views, cpm_low, cpm_high):
    return round(median_views / 1000 * cpm_low), round(median_views / 1000 * cpm_high)


if __name__ == "__main__":
    s = stats([{"views": "10000", "likes": "800", "comments": "50", "saves": "100", "shares": "50"},
               {"views": "20000", "likes": "900", "comments": "60", "saves": "20", "shares": "20"}], 20000)
    assert s["median_views"] == 15000 and s["engagement_rate_followers"] == 0.05
    assert price_range(15000, 20, 40) == (300, 600)

    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--followers", type=float, required=True)
    p.add_argument("--cpm-low", type=float, required=True)
    p.add_argument("--cpm-high", type=float, required=True)
    a = p.parse_args()
    with open(a.csv, newline="") as f:
        s = stats(list(csv.DictReader(f)), a.followers)
    lo, hi = price_range(s["median_views"], a.cpm_low, a.cpm_high)
    print(f"Median views per post: {s['median_views']:,.0f}")
    print(f"Engagement rate: {s['engagement_rate_followers']:.2%} of followers, {s['engagement_rate_views']:.2%} of views")
    print(f"One post at CPM {a.cpm_low:g} to {a.cpm_high:g}: {lo:,} to {hi:,} (same currency as the CPM)")
    print("Add for: usage rights, exclusivity, extra deliverables, rush timelines.")
