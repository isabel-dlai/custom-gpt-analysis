#!/usr/bin/env python3
"""
Analyze GPTs related to automation and task automation
"""

import csv
import re
import random

# Automation-related keywords
AUTOMATION_KEYWORDS = [
    'automat', 'workflow', 'pipeline', 'scheduler', 'batch',
    'streamline', 'routine', 'recurring', 'repetitive',
    'generate', 'creator', 'builder', 'maker', 'generator',
    'assistant', 'helper', 'tool', 'utility',
    'process', 'efficiency', 'productivity', 'optimize',
    'template', 'framework', 'system',
    'scrape', 'extract', 'collect', 'aggregate',
    'convert', 'transform', 'format',
    'schedule', 'manage', 'organize', 'track'
]

def is_automation_related(description, url):
    """Check if GPT is related to automation"""
    text = (description + ' ' + url).lower()

    # Check for automation keywords
    for keyword in AUTOMATION_KEYWORDS:
        if keyword in text:
            return True

    return False

def analyze_automation():
    """Analyze automation-related GPTs"""

    input_file = 'outputs/serper_collected_gpts_english_only.csv'

    all_gpts = []
    automation_gpts = []

    print("Loading GPTs...")
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_gpts.append(row)

            if is_automation_related(row['description'], row['url']):
                automation_gpts.append(row)

    # Calculate statistics
    total_count = len(all_gpts)
    automation_count = len(automation_gpts)
    automation_percentage = (automation_count / total_count) * 100

    print("\n" + "=" * 80)
    print("AUTOMATION ANALYSIS")
    print("=" * 80)
    print(f"\nTotal GPTs analyzed: {total_count:,}")
    print(f"Automation-related GPTs: {automation_count:,}")
    print(f"Percentage: {automation_percentage:.1f}%")

    # Get random sample
    sample_size = min(50, len(automation_gpts))
    random_sample = random.sample(automation_gpts, sample_size)

    print(f"\n" + "=" * 80)
    print(f"RANDOM SAMPLE OF {sample_size} AUTOMATION GPTs")
    print("=" * 80)

    for i, gpt in enumerate(random_sample, 1):
        # Extract GPT name from URL
        gpt_name = gpt['url'].split('/')[-1].replace('-', ' ').title()
        if len(gpt_name) > 60:
            gpt_name = gpt_name[:60] + "..."

        # Truncate description
        desc = gpt['description']
        if len(desc) > 150:
            desc = desc[:150] + "..."

        print(f"\n{i}. {gpt_name}")
        print(f"   {desc}")
        print(f"   {gpt['url']}")

    # Save automation GPTs to file
    output_file = 'outputs/automation_gpts.csv'
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'description', 'source_query'])
        writer.writeheader()
        writer.writerows(automation_gpts)

    print(f"\n" + "=" * 80)
    print(f"Full list saved to: {output_file}")
    print("=" * 80)

    # Categorize automation types
    print(f"\n" + "=" * 80)
    print("AUTOMATION CATEGORIES")
    print("=" * 80)

    categories = {
        'Content Generation': ['generate', 'creator', 'writer', 'maker'],
        'Document Creation': ['document', 'report', 'contract', 'template'],
        'Data Processing': ['extract', 'scrape', 'collect', 'analyze', 'process'],
        'Workflow Management': ['workflow', 'pipeline', 'process', 'system'],
        'Scheduling & Organization': ['schedule', 'calendar', 'organize', 'plan'],
        'Code/Technical Automation': ['code', 'script', 'deploy', 'build'],
        'Marketing Automation': ['seo', 'social media', 'email', 'campaign'],
        'Design Automation': ['logo', 'design', 'image', 'graphic']
    }

    category_counts = {cat: 0 for cat in categories}

    for gpt in automation_gpts:
        text = (gpt['description'] + ' ' + gpt['url']).lower()
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                category_counts[category] += 1

    # Sort by count
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

    for category, count in sorted_categories:
        percentage = (count / automation_count) * 100
        print(f"\n{category}: {count:,} ({percentage:.1f}% of automation GPTs)")

if __name__ == '__main__':
    random.seed(42)  # For reproducible random sample
    analyze_automation()
