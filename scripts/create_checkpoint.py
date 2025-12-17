#!/usr/bin/env python3
"""
Create checkpoint from existing CSV to avoid duplicate queries
"""
import csv
import json
import re

def extract_original_url_from_query(query):
    """
    Extract the original GPT URL from the search query
    Query format: "chatgpt g-XXXXX name words"
    We need to reconstruct the URL
    """
    # Extract ID and name from query
    parts = query.replace('chatgpt ', '').strip().split(' ', 1)
    if len(parts) >= 1:
        gpt_id = parts[0]  # g-XXXXX
        name = parts[1] if len(parts) > 1 else ''
        name_slug = name.replace(' ', '-')

        if name_slug:
            return f"https://chatgpt.com/g/{gpt_id}-{name_slug}"
        else:
            return f"https://chatgpt.com/g/{gpt_id}"
    return None

# Read existing CSV and extract processed URLs
processed_urls = set()

with open('serper_collected_gpts.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        query = row.get('source_query', '').strip()
        if query:
            # Reconstruct original URL from query
            url = extract_original_url_from_query(query)
            if url:
                processed_urls.add(url)

print(f"Found {len(processed_urls)} processed URLs")

# Save checkpoint
with open('serper_checkpoint.json', 'w') as f:
    json.dump({'processed_urls': list(processed_urls)}, f, indent=2)

print(f"Checkpoint saved to serper_checkpoint.json")
print(f"These {len(processed_urls)} URLs will be skipped in future runs")
