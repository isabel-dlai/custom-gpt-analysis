#!/usr/bin/env python3
"""
Cluster analysis of GPT descriptions to find main themes and categories
"""

import csv
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
import numpy as np
from collections import Counter, defaultdict


def clean_text(text):
    """Clean and normalize text for better clustering"""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove "ChatGPT" mentions and common filler
    text = re.sub(r'ChatGPT\.?|Sign up|Log in|Attach|Create image|GPT Icon', '', text, flags=re.IGNORECASE)
    # Remove "By <author>" patterns
    text = re.sub(r'By [^.]+\.', '', text)
    # Remove messaging/agreement text
    text = re.sub(r'By messaging.*?\.', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_key_terms(cluster_docs, vectorizer, n_terms=10):
    """Extract most important terms for a cluster"""
    # Get TF-IDF for this cluster's documents
    if not cluster_docs:
        return []

    tfidf_matrix = vectorizer.transform(cluster_docs)
    # Sum TF-IDF scores across all docs in cluster
    scores = np.asarray(tfidf_matrix.sum(axis=0)).flatten()

    # Get top terms
    feature_names = vectorizer.get_feature_names_out()
    top_indices = scores.argsort()[-n_terms:][::-1]

    return [(feature_names[idx], scores[idx]) for idx in top_indices]


print("Loading GPT data from outputs/serper_collected_gpts_english_only.csv...")

descriptions = []
urls = []
full_data = []

with open('outputs/serper_collected_gpts_english_only.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        desc = clean_text(row['description'])
        if len(desc) > 20:  # Filter out very short descriptions
            descriptions.append(desc)
            urls.append(row['url'])
            full_data.append(row)

print(f"Loaded {len(descriptions):,} GPT descriptions\n")

# Create TF-IDF vectors
print("Creating TF-IDF vectors...")
vectorizer = TfidfVectorizer(
    max_features=1000,
    min_df=5,
    max_df=0.7,
    stop_words='english',
    ngram_range=(1, 2)
)
tfidf_matrix = vectorizer.fit_transform(descriptions)

print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")

# Reduce dimensionality for better clustering
print("Reducing dimensionality with SVD...")
svd = TruncatedSVD(n_components=100, random_state=42)
reduced_matrix = svd.fit_transform(tfidf_matrix)

# Perform K-means clustering
n_clusters = 15
print(f"\nPerforming K-means clustering with {n_clusters} clusters...")
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(reduced_matrix)

# Organize results by cluster
cluster_data = defaultdict(list)
for idx, cluster_id in enumerate(clusters):
    cluster_data[cluster_id].append({
        'description': descriptions[idx],
        'url': urls[idx],
        'full_data': full_data[idx]
    })

# Analyze each cluster
print("\n" + "=" * 80)
print("CLUSTER ANALYSIS RESULTS")
print("=" * 80)

cluster_summaries = []

for cluster_id in range(n_clusters):
    items = cluster_data[cluster_id]
    cluster_docs = [item['description'] for item in items]

    # Get key terms
    key_terms = extract_key_terms(cluster_docs, vectorizer, n_terms=8)

    # Get sample descriptions
    sample_size = min(5, len(items))
    samples = np.random.choice(len(items), size=sample_size, replace=False)

    print(f"\n{'─' * 80}")
    print(f"CLUSTER {cluster_id + 1}")
    print(f"{'─' * 80}")
    print(f"Size: {len(items):,} GPTs ({len(items)/len(descriptions)*100:.1f}%)")

    print(f"\nKey Terms:")
    for term, score in key_terms:
        print(f"  • {term} ({score:.2f})")

    print(f"\nSample GPTs:")
    for sample_idx in samples:
        item = items[sample_idx]
        # Extract GPT name from URL
        gpt_name = item['url'].split('/')[-1].replace('-', ' ').title()
        desc_preview = item['description'][:150] + "..." if len(item['description']) > 150 else item['description']
        print(f"\n  [{gpt_name}]")
        print(f"  {desc_preview}")

    # Store summary
    cluster_summaries.append({
        'id': cluster_id + 1,
        'size': len(items),
        'percentage': len(items)/len(descriptions)*100,
        'key_terms': [term for term, _ in key_terms[:5]],
        'top_description': items[0]['description']
    })

# Overall statistics
print(f"\n{'=' * 80}")
print("SUMMARY STATISTICS")
print(f"{'=' * 80}")
print(f"\nTotal GPTs analyzed: {len(descriptions):,}")
print(f"Number of clusters: {n_clusters}")
print(f"\nCluster sizes:")
cluster_sizes = sorted([(cid, len(items)) for cid, items in cluster_data.items()],
                       key=lambda x: x[1], reverse=True)
for cid, size in cluster_sizes:
    print(f"  Cluster {cid + 1}: {size:,} GPTs ({size/len(descriptions)*100:.1f}%)")

print(f"\n{'=' * 80}")
print("TOP CLUSTER THEMES")
print(f"{'=' * 80}")

# Sort by size and show top themes
sorted_summaries = sorted(cluster_summaries, key=lambda x: x['size'], reverse=True)
for i, summary in enumerate(sorted_summaries[:10], 1):
    print(f"\n{i}. Cluster {summary['id']} ({summary['size']:,} GPTs, {summary['percentage']:.1f}%)")
    print(f"   Key terms: {', '.join(summary['key_terms'])}")
