#!/usr/bin/env python3
"""
Fetch the previous day's Red Flag Domains list and produce an OpenCTI-compatible CSV.
"""

import csv
import urllib.request
from datetime import datetime, timedelta, timezone


BASE_URL = "https://dl.red.flag.domains/daily"
OUTPUT_FILE = "daily_domains.csv"

MARKING_TYPE = "TLP"
MARKING_VALUE = "TLP:CLEAR"
MARKING_PRIORITY = "1"


def stix_pattern(domain: str) -> str:
    return f"[domain-name:value = '{domain}']"


def main() -> None:
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")
    url = f"{BASE_URL}/{date_str}.txt"

    print(f"Fetching {url} ...")
    with urllib.request.urlopen(url) as response:
        raw = response.read().decode("utf-8")

    domains = [line.strip() for line in raw.splitlines() if line.strip()]
    print(f"Retrieved {len(domains)} domains for {date_str}")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow([
            "domain",
            "stix_pattern",
            "marking_type",
            "marking_value",
            "marking_priority",
        ])
        for domain in domains:
            writer.writerow([
                domain,
                stix_pattern(domain),
                MARKING_TYPE,
                MARKING_VALUE,
                MARKING_PRIORITY,
            ])

    print(f"Wrote {len(domains)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
