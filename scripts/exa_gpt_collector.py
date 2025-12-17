#!/usr/bin/env python3
"""
Exa GPT Collector - Uses Exa API to find GPT URLs and descriptions
Supports checkpoint to avoid re-processing URLs
"""

import csv
import re
import time
import json
import os
from exa_py import Exa
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class ExaGPTCollector:
    def __init__(self):
        self.api_key = os.getenv('EXA_API_KEY')
        if not self.api_key:
            raise ValueError("EXA_API_KEY not found in .env file")

        self.exa = Exa(api_key=self.api_key)
        self.csv_file = 'serper_collected_gpts.csv'  # Use same file as Serper
        self.checkpoint_file = 'serper_checkpoint.json'  # Use same checkpoint
        self.processed_urls = self.load_checkpoint()
        self.init_csv()

    def load_checkpoint(self):
        """Load checkpoint to avoid re-processing URLs"""
        try:
            with open(self.checkpoint_file, 'r') as f:
                data = json.load(f)
                processed = set(data.get('processed_urls', []))
                logger.info(f"Loaded checkpoint: {len(processed)} URLs already processed")
                return processed
        except FileNotFoundError:
            logger.info("No checkpoint found - starting fresh")
            return set()

    def save_checkpoint(self):
        """Save current progress to checkpoint"""
        with open(self.checkpoint_file, 'w') as f:
            json.dump({'processed_urls': list(self.processed_urls)}, f, indent=2)

    def init_csv(self):
        """Initialize CSV file with headers"""
        try:
            with open(self.csv_file, 'r') as f:
                pass  # File exists
        except FileNotFoundError:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['url', 'description', 'source_query'])

    def parse_url(self, url):
        """Extract ID and name from GPT URL"""
        match = re.match(r'https://chatgpt\.com/g/(g-[a-zA-Z0-9]+)(?:-(.+))?', url)
        if match:
            gpt_id = match.group(1)
            name = match.group(2).replace('-', ' ') if match.group(2) else ''
            return gpt_id, name
        return None, None

    def search_exa(self, query):
        """Search using Exa API (search only, no contents to save credits)"""
        try:
            # Use search() only - much cheaper than search_and_contents()
            # Returns URLs, titles, and snippets without fetching full pages
            response = self.exa.search(
                query,
                num_results=10
            )
            return response
        except Exception as e:
            logger.error(f"Exa API error: {e}")
            return None

    def extract_description_from_text(self, text):
        """
        Extract the clean GPT description from Exa text.
        Pattern: Text comes after "By [author]" and before "Sign up to chat"

        Example:
        By Organizational.AI

        Optimizes call center operations for customer satisfaction and efficiency.

        Sign up to chat
        """
        if not text:
            return ''

        # Try to extract the description between "By" line and "Sign up" line
        # Pattern: Find text after "By [anything]" and before "Sign up"
        pattern = r'By\s+[^\n]+\s*\n\s*\n(.+?)\n\s*\n(?:Sign up|$)'
        match = re.search(pattern, text, re.DOTALL)

        if match:
            description = match.group(1).strip()
            # Clean up markdown, images, links
            description = self.clean_markdown(description)
            # Clean up any remaining newlines
            description = re.sub(r'\s+', ' ', description)
            return description[:500]

        # Fallback: Try to find any meaningful sentence in the text
        # Skip header/navigation elements
        lines = text.split('\n')
        meaningful_lines = []

        skip_patterns = [
            r'^\[.*\]$',  # Markdown links
            r'^!\[',      # Markdown images
            r'^Sign up',
            r'^Log in',
            r'^ChatGPT',
            r'^By\s+',
            r'^Create image',
            r'^Voice',
            r'^Attach',
            r'^Search',
            r'^#\s+',     # Headers
        ]

        for line in lines:
            line = line.strip()
            if not line or len(line) < 10:
                continue

            # Skip if matches any skip pattern
            if any(re.match(pattern, line, re.IGNORECASE) for pattern in skip_patterns):
                continue

            meaningful_lines.append(line)

        # Return the first meaningful line (likely the description)
        if meaningful_lines:
            description = ' '.join(meaningful_lines[:2])  # First 2 meaningful lines
            description = self.clean_markdown(description)
            return re.sub(r'\s+', ' ', description)[:500]

        return ''

    def clean_markdown(self, text):
        """Remove markdown formatting and images"""
        if not text:
            return ''

        # Remove markdown images: ![alt](url)
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

        # Remove markdown links but keep the text: [text](url) -> text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

        # Remove standalone links like [ChatGPT](url)
        text = re.sub(r'\[ChatGPT\]\([^\)]+\)', '', text)

        # Remove markdown headers
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)

        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def extract_gpts_from_results(self, search_results, query):
        """Extract all GPT URLs and descriptions from Exa search results"""
        gpts = []

        if not search_results or not hasattr(search_results, 'results'):
            return gpts

        # Process each result
        for result in search_results.results:
            url = result.url if hasattr(result, 'url') else ''

            # First try to extract description from text field if available
            description = ''
            if hasattr(result, 'text') and result.text:
                # Use the existing extraction method to get clean description from text
                description = self.extract_description_from_text(result.text)
                if description:
                    logger.debug(f"  Extracted description from text: {description[:100]}...")

            # Fallback to title if no good description from text
            if not description and hasattr(result, 'title'):
                description = result.title
                # Clean up "ChatGPT - " prefix if present
                description = re.sub(r'^ChatGPT\s*-\s*', '', description)
                description = description.strip()
                logger.debug(f"  Using title as description: {description[:100]}...")

            # Check if this is a GPT URL
            if 'chatgpt.com/g/g-' in url:
                gpts.append({
                    'url': url,
                    'description': description,
                    'source_query': query
                })

        return gpts

    def save_to_csv(self, gpts):
        """Append GPTs to CSV file"""
        if not gpts:
            return

        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for gpt in gpts:
                writer.writerow([
                    gpt['url'],
                    gpt['description'],
                    gpt['source_query']
                ])

    def process_url(self, url):
        """Process a single URL: search and collect GPTs"""
        # Check if already processed
        if url in self.processed_urls:
            logger.info(f"  ⏭  Skipping (already processed)")
            return []

        gpt_id, name = self.parse_url(url)
        if not gpt_id:
            logger.warning(f"Could not parse URL: {url}")
            self.processed_urls.add(url)
            return []

        # Build search query
        query = f"chatgpt {gpt_id} {name}"
        logger.info(f"Searching: {query}")

        # Search
        results = self.search_exa(query)

        if not results:
            logger.warning(f"No results returned")
            self.processed_urls.add(url)
            return []

        # Extract GPTs
        gpts = self.extract_gpts_from_results(results, query)

        # Save immediately
        self.save_to_csv(gpts)

        # Mark as processed
        self.processed_urls.add(url)

        return gpts

    def process_batch(self, urls, delay=1, save_checkpoint_every=10):
        """Process multiple URLs with checkpoint support"""
        total_found = 0
        processed_count = 0

        for i, url in enumerate(urls, 1):
            logger.info(f"\n[{i}/{len(urls)}] Processing: {url}")

            gpts = self.process_url(url)

            if gpts:
                logger.info(f"  ✓ Found {len(gpts)} GPT(s)")
                for gpt in gpts[:3]:  # Show first 3
                    logger.info(f"    • {gpt['url'][:60]}...")
                total_found += len(gpts)
            elif url not in self.processed_urls:
                logger.info(f"  ✗ No GPTs found")

            processed_count += 1

            # Save checkpoint periodically
            if processed_count % save_checkpoint_every == 0:
                self.save_checkpoint()
                logger.info(f"  💾 Checkpoint saved ({len(self.processed_urls)} URLs processed)")

            # Rate limiting
            if i < len(urls):
                time.sleep(delay)

        # Final checkpoint save
        self.save_checkpoint()

        logger.info(f"\n{'='*60}")
        logger.info(f"Total GPTs collected: {total_found}")
        logger.info(f"Total URLs processed: {processed_count}")
        logger.info(f"Results saved to: {self.csv_file}")
        logger.info(f"Checkpoint saved to: {self.checkpoint_file}")


def main():
    import sys

    # Load URLs from file
    urls = []
    with open('valid-gpt-urls.txt', 'r') as f:
        for line in f:
            url = line.strip()
            if url:
                urls.append(url)

    # Check for limit argument
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None

    if limit:
        logger.info(f"Loaded {len(urls)} total URLs (limiting to {limit} for testing)")
    else:
        logger.info(f"Loaded {len(urls)} total URLs")

    # Initialize collector (will skip already processed URLs from checkpoint)
    collector = ExaGPTCollector()

    # Filter out already processed URLs
    urls_to_process = [url for url in urls if url not in collector.processed_urls]

    # Apply limit if specified
    if limit:
        urls_to_process = urls_to_process[:limit]

    logger.info(f"URLs to process: {len(urls_to_process)}")
    logger.info(f"Already processed: {len(collector.processed_urls)}")
    logger.info("Starting collection with Exa API...")

    try:
        collector.process_batch(urls_to_process, delay=1, save_checkpoint_every=5)
    except KeyboardInterrupt:
        logger.info("\n" + "="*60)
        logger.info("Collection interrupted by user")
        collector.save_checkpoint()
        logger.info(f"Progress saved to: {collector.checkpoint_file}")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        collector.save_checkpoint()
        logger.info(f"Progress saved to: {collector.checkpoint_file}")
        raise


if __name__ == "__main__":
    main()
