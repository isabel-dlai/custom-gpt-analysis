#!/usr/bin/env python3
"""
Segment GPTs into clusters based on the taxonomy analysis
"""

import csv
import re
from collections import defaultdict, Counter


# Define cluster patterns based on the taxonomy analysis
CLUSTER_DEFINITIONS = {
    'Creative Content Generation': {
        'keywords': ['image', 'picture', 'creator', 'generator', 'art', 'visual', 'story', 'gif',
                    'illustration', 'creative', 'prompt', 'dall-e', 'artistic', 'design', 'draw',
                    'paint', 'sketch', 'anime', 'cartoon', 'logo', 'graphic'],
        'priority': 6
    },
    'Educational & Learning': {
        'keywords': ['study', 'learn', 'exam', 'tutor', 'student', 'education', 'practice', 'test',
                    'homework', 'course', 'teaching', 'solver', 'step-by-step', 'sat', 'act', 'academic',
                    'teacher', 'lesson', 'quiz', 'training', 'instructor'],
        'priority': 5
    },
    'Professional Business Tools': {
        'keywords': ['business', 'sales', 'pitch', 'deck', 'executive', 'strategy', 'growth',
                    'entrepreneur', 'startup', 'plan', 'proposal', 'saas', 'mckinsey', 'professional',
                    'marketing', 'revenue', 'investment', 'finance', 'consultant'],
        'priority': 6
    },
    'Technical & Coding': {
        'keywords': ['code', 'programming', 'sql', 'python', 'linux', 'devops', 'css', 'developer',
                    'coding', 'debug', 'script', 'colab', 'algorithm', 'software', 'api', 'database',
                    'javascript', 'react', 'frontend', 'backend', 'web dev'],
        'priority': 4
    },
    'Writing & Content Marketing': {
        'keywords': ['write', 'post', 'tweet', 'social media', 'viral', 'content', 'description',
                    'marketing', 'instagram', 'linkedin', 'engagement', 'copywriting', 'blog',
                    'newsletter', 'seo', 'brand'],
        'priority': 6
    },
    'Legal & Compliance': {
        'keywords': ['law', 'legal', 'contract', 'attorney', 'solicitor', 'regulation', 'compliance',
                    'court', 'nda', 'jurisdiction', 'disclaimer', 'terms', 'policy', 'lawyer'],
        'priority': 2
    },
    'Personal Development & Coaching': {
        'keywords': ['coach', 'personal', 'guide', 'mentor', 'habit', 'motivation', 'feedback',
                    'leadership', 'growth', 'transformation', 'quit', 'improve', 'development',
                    'mindset', 'productivity', 'goal'],
        'priority': 7
    },
    'Health & Wellness': {
        'keywords': ['health', 'medical', 'wellness', 'nutrition', 'advisor', 'dermatology', 'acne',
                    'diet', 'food', 'healthcare', 'skin', 'treatment', 'remedy', 'fitness', 'doctor',
                    'therapy', 'mental health'],
        'priority': 2
    },
    'Entertainment & Gaming': {
        'keywords': ['game', 'gaming', 'play', 'battle', 'challenge', 'rpg', 'score', 'player',
                    'simulator', 'sports', 'entertainment', 'interactive', 'dungeon', 'quest',
                    'adventure', 'trivia'],
        'priority': 7
    },
    'Specialized Domain Experts': {
        'keywords': ['expert', 'specialist', 'research', 'scientific', 'chemistry', 'physics',
                    'mathematics', 'molecular', 'biochemistry', 'equation', 'calculation', 'scholarly',
                    'theoretical', 'advanced', 'quantum', 'nano'],
        'priority': 1
    },
    'Spiritual & Mystical': {
        'keywords': ['spiritual', 'tarot', 'oracle', 'wisdom', 'horoscope', 'astrology', 'palm',
                    'divination', 'god', 'mystical', 'destiny', 'biorhythm', 'fortune', 'psychic',
                    'meditation', 'enlightenment'],
        'priority': 8
    },
    'Productivity & Organization': {
        'keywords': ['productivity', 'organize', 'task', 'project', 'management', 'planner',
                    'assistant', 'helper', 'journal', 'checklist', 'schedule', 'todoist', 'calendar',
                    'workflow', 'efficiency'],
        'priority': 7
    },
    'Niche Hobby & Lifestyle': {
        'keywords': ['hobby', 'swim', 'quilting', 'beekeeping', 'racing', 'diy', 'craft', 'enthusiast',
                    'tips', 'decorations', 'collector', 'recipe', 'cooking', 'travel', 'pet',
                    'gardening', 'photography'],
        'priority': 9
    }
}


def classify_gpt(description, url):
    """
    Classify a GPT into clusters based on description and URL
    Returns list of (cluster_name, score) tuples sorted by score
    """
    text = (description + ' ' + url).lower()

    cluster_scores = {}

    for cluster_name, cluster_info in CLUSTER_DEFINITIONS.items():
        score = 0
        keywords = cluster_info['keywords']

        # Count keyword matches
        for keyword in keywords:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = len(re.findall(pattern, text))
            score += matches

        # Adjust score by priority (lower priority = higher weight for tie-breaking)
        # We'll use raw score for primary sorting, priority for secondary
        cluster_scores[cluster_name] = {
            'score': score,
            'priority': cluster_info['priority']
        }

    # Sort by score (descending), then by priority (ascending)
    sorted_clusters = sorted(
        cluster_scores.items(),
        key=lambda x: (x[1]['score'], -x[1]['priority']),
        reverse=True
    )

    return sorted_clusters


def segment_gpts(input_file, output_dir='outputs/clusters'):
    """
    Segment GPTs from input CSV into cluster-specific CSV files
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Read all GPTs
    gpts = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gpts.append(row)

    print(f"Loaded {len(gpts):,} GPTs from {input_file}\n")

    # Classify each GPT
    cluster_assignments = defaultdict(list)
    unclassified = []

    for gpt in gpts:
        description = gpt.get('description', '')
        url = gpt.get('url', '')

        # Get classification scores
        classifications = classify_gpt(description, url)

        # Assign to best cluster if score > 0
        if classifications[0][1]['score'] > 0:
            best_cluster = classifications[0][0]
            cluster_assignments[best_cluster].append(gpt)
        else:
            unclassified.append(gpt)

    # Write cluster files
    print("=" * 80)
    print("CLUSTER DISTRIBUTION")
    print("=" * 80)

    total_classified = 0
    cluster_stats = []

    for cluster_name in sorted(CLUSTER_DEFINITIONS.keys()):
        gpts_in_cluster = cluster_assignments[cluster_name]
        count = len(gpts_in_cluster)
        total_classified += count

        if count > 0:
            # Write cluster file
            filename = cluster_name.lower().replace(' & ', '_').replace(' ', '_') + '.csv'
            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['url', 'description', 'source_query'])
                writer.writeheader()
                writer.writerows(gpts_in_cluster)

            cluster_stats.append((cluster_name, count, filepath))
            print(f"\n{cluster_name}:")
            print(f"  Count: {count:,} GPTs ({count/len(gpts)*100:.1f}%)")
            print(f"  File: {filepath}")

            # Show 3 examples
            print(f"  Examples:")
            for i, gpt in enumerate(gpts_in_cluster[:3], 1):
                title = gpt['url'].split('/')[-1].replace('-', ' ').title()[:50]
                print(f"    {i}. {title}")

    # Write unclassified
    if unclassified:
        filepath = os.path.join(output_dir, 'unclassified.csv')
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['url', 'description', 'source_query'])
            writer.writeheader()
            writer.writerows(unclassified)

        print(f"\nUnclassified:")
        print(f"  Count: {len(unclassified):,} GPTs ({len(unclassified)/len(gpts)*100:.1f}%)")
        print(f"  File: {filepath}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total GPTs: {len(gpts):,}")
    print(f"Classified: {total_classified:,} ({total_classified/len(gpts)*100:.1f}%)")
    print(f"Unclassified: {len(unclassified):,} ({len(unclassified)/len(gpts)*100:.1f}%)")
    print(f"\nCluster files saved to: {output_dir}/")

    # Top 5 clusters
    print("\nTop 5 Largest Clusters:")
    sorted_stats = sorted(cluster_stats, key=lambda x: x[1], reverse=True)
    for i, (name, count, _) in enumerate(sorted_stats[:5], 1):
        print(f"  {i}. {name}: {count:,} GPTs")


if __name__ == '__main__':
    segment_gpts('outputs/serper_collected_gpts_english_only.csv')
