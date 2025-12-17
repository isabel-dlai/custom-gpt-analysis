#!/usr/bin/env python3
"""
Compare URLs between deduplicated CSV and archived URL list
"""

import csv
import re


def clean_url(url: str) -> str:
    """
    Clean GPT URL by removing query parameters and trailing slashes
    """
    # Remove query parameters
    if '?' in url:
        url = url.split('?')[0]

    # Remove trailing slashes
    url = url.rstrip('/')

    return url.lower()


def extract_gpt_id(url: str) -> str:
    """Extract the GPT ID from a URL"""
    match = re.search(r'/g/(g-[A-Za-z0-9]+)', url)
    return match.group(1).lower() if match else None


# Read URLs from the archived deduplicated-gpt-urls.txt
archived_urls = set()
archived_gpt_ids = set()

print("Reading archived URLs from archive/deduplicated-gpt-urls.txt...")
with open('archive/deduplicated-gpt-urls.txt', 'r', encoding='utf-8') as f:
    for line in f:
        url = clean_url(line.strip())
        if url:
            archived_urls.add(url)
            gpt_id = extract_gpt_id(url)
            if gpt_id:
                archived_gpt_ids.add(gpt_id)

print(f"  Found {len(archived_urls):,} archived URLs")
print(f"  Found {len(archived_gpt_ids):,} unique GPT IDs in archive")

# Read URLs from the deduplicated CSV
csv_urls = set()
csv_gpt_ids = set()

print("\nReading URLs from outputs/serper_collected_gpts_deduplicated.csv...")
with open('outputs/serper_collected_gpts_deduplicated.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = clean_url(row['url'])
        if url:
            csv_urls.add(url)
            gpt_id = extract_gpt_id(url)
            if gpt_id:
                csv_gpt_ids.add(gpt_id)

print(f"  Found {len(csv_urls):,} URLs in deduplicated CSV")
print(f"  Found {len(csv_gpt_ids):,} unique GPT IDs in CSV")

# Calculate overlaps
url_overlap = archived_urls.intersection(csv_urls)
gpt_id_overlap = archived_gpt_ids.intersection(csv_gpt_ids)

# Find unique entries
only_in_archive = archived_gpt_ids - csv_gpt_ids
only_in_csv = csv_gpt_ids - archived_gpt_ids

# Statistics
print("\n" + "=" * 60)
print("COMPARISON RESULTS")
print("=" * 60)
print(f"\nArchived file (deduplicated-gpt-urls.txt):")
print(f"  Total URLs:              {len(archived_urls):,}")
print(f"  Unique GPT IDs:          {len(archived_gpt_ids):,}")

print(f"\nNew CSV file (serper_collected_gpts_deduplicated.csv):")
print(f"  Total URLs:              {len(csv_urls):,}")
print(f"  Unique GPT IDs:          {len(csv_gpt_ids):,}")

print(f"\nOverlap Analysis:")
print(f"  Matching exact URLs:     {len(url_overlap):,} ({len(url_overlap)/len(csv_urls)*100:.1f}% of CSV)")
print(f"  Matching GPT IDs:        {len(gpt_id_overlap):,} ({len(gpt_id_overlap)/len(csv_gpt_ids)*100:.1f}% of CSV)")

print(f"\nUnique Entries:")
print(f"  Only in archive:         {len(only_in_archive):,}")
print(f"  Only in new CSV:         {len(only_in_csv):,}")
print(f"  New GPTs discovered:     {len(only_in_csv):,}")

print(f"\nCombined Dataset:")
print(f"  Total unique GPT IDs:    {len(archived_gpt_ids.union(csv_gpt_ids)):,}")
