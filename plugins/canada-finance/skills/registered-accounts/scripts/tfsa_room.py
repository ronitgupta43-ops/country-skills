"""TFSA contribution room. Usage: python tfsa_room.py --start 2022 [--year 2026] [--contributed X] [--withdrawn-before-this-year Y]"""
import argparse

# Update each January. ponytail: hardcoded table, add new year when CRA announces it.
LIMITS = {**{y: 5000 for y in range(2009, 2013)}, 2013: 5500, 2014: 5500, 2015: 10000,
          **{y: 5500 for y in range(2016, 2019)}, **{y: 6000 for y in range(2019, 2023)},
          2023: 6500, 2024: 7000, 2025: 7000, 2026: 7000}


def tfsa_room(start, year, contributed=0, withdrawn_before=0):
    start = max(start, 2009)
    if year not in LIMITS:
        raise ValueError(f"No TFSA limit for {year} yet - update LIMITS")
    return sum(LIMITS[y] for y in range(start, year + 1)) - contributed + withdrawn_before


if __name__ == "__main__":
    assert tfsa_room(2009, 2026) == 109000
    assert tfsa_room(2022, 2026, 5000, 1000) == 6000 + 6500 + 7000 * 3 - 4000
    p = argparse.ArgumentParser()
    p.add_argument("--start", type=int, required=True, help="later of: year turned 18, year became resident, 2009")
    p.add_argument("--year", type=int, default=max(LIMITS))
    p.add_argument("--contributed", type=float, default=0, help="all contributions ever made")
    p.add_argument("--withdrawn-before-this-year", type=float, default=0)
    a = p.parse_args()
    print(f"TFSA room for {a.year}: ${tfsa_room(a.start, a.year, a.contributed, a.withdrawn_before_this_year):,.0f}")
