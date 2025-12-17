import pandas as pd
import re

# Read the creative content generation cluster
df = pd.read_csv('/Users/isabelgwara/Documents/GitHub/custom-gpt-scraper/outputs/clusters/creative_content_generation.csv')

print(f"Total GPTs in creative content generation cluster: {len(df)}")

# Define keywords that indicate image generation
image_keywords = [
    'image', 'img', 'picture', 'photo', 'visual', 'graphic', 'illustration',
    'draw', 'drawing', 'paint', 'painting', 'sketch', 'art', 'artist',
    'design', 'designer', 'dall', 'dalle', 'midjourney', 'stable diffusion',
    'generate image', 'create image', 'make image', 'logo', 'icon',
    'render', 'rendering', 'visualize', 'visualization', 'diagram',
    'infographic', 'poster', 'banner', 'thumbnail', 'avatar',
    'cartoon', 'anime', 'comic', 'character design', 'concept art',
    'pixel art', 'sprite', '3d model', 'texture', 'coloring'
]

# Function to check if text contains image-related keywords
def contains_image_keywords(text):
    if pd.isna(text):
        return False
    text_lower = str(text).lower()
    return any(keyword in text_lower for keyword in image_keywords)

# Check both url and description
df['is_image_related'] = df.apply(
    lambda row: contains_image_keywords(row.get('url', '')) or
                contains_image_keywords(row.get('description', '')),
    axis=1
)

# Count image generation GPTs
image_generation_count = df['is_image_related'].sum()
total_count = len(df)
proportion = (image_generation_count / total_count) * 100

print(f"\nImage generation related GPTs: {image_generation_count}")
print(f"Proportion: {proportion:.1f}%")

# Show some examples
print("\n=== Sample Image Generation GPTs ===")
image_gpts = df[df['is_image_related']].head(20)
for idx, row in image_gpts.iterrows():
    url = row.get('url', 'N/A')
    desc = row.get('description', 'N/A')
    if len(desc) > 100:
        desc = desc[:100] + "..."
    print(f"\n{url}")
    print(f"  {desc}")

# Show some non-image examples to verify
print("\n\n=== Sample Non-Image Generation GPTs ===")
non_image_gpts = df[~df['is_image_related']].head(10)
for idx, row in non_image_gpts.iterrows():
    url = row.get('url', 'N/A')
    desc = row.get('description', 'N/A')
    if len(desc) > 100:
        desc = desc[:100] + "..."
    print(f"\n{url}")
    print(f"  {desc}")

# Save the classification
output_path = '/Users/isabelgwara/Documents/GitHub/custom-gpt-scraper/outputs/creative_content_image_analysis.csv'
df[['url', 'description', 'is_image_related']].to_csv(output_path, index=False)
print(f"\n\nAnalysis saved to: {output_path}")
