#!/usr/bin/env python3
"""
Serper GPT Collector - Parallel Threaded Version
Uses ThreadPoolExecutor to run multiple searches concurrently
"""

import csv
import re
import time
import requests
import os
from urllib.parse import quote
from dotenv import load_dotenv
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class ParallelSerperCollector:
    def __init__(self, max_workers=5):
        self.api_key = os.getenv('SERPER_API_KEY')
        if not self.api_key:
            raise ValueError("SERPER_API_KEY not found in .env file")

        self.csv_file = 'serper_collected_gpts.csv'
        self.checkpoint_file = 'serper_checkpoint.json'
        self.max_workers = max_workers
        self.csv_lock = Lock()  # Thread-safe CSV writing
        self.processed_urls = set()  # Track processed URLs
        self.init_csv()
        self.load_checkpoint()

    def init_csv(self):
        """Initialize CSV file with headers if it doesn't exist"""
        try:
            with open(self.csv_file, 'r') as f:
                # File exists, read existing URLs to avoid duplicates
                reader = csv.DictReader(f)
                for row in reader:
                    source = row.get('source_query', '')
                    # Extract original URL from source query if possible
                    # This is a simple heuristic - we'll track by source_query
                    pass
        except FileNotFoundError:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['url', 'description', 'source_query'])

    def load_checkpoint(self):
        """Load checkpoint of processed URLs"""
        try:
            with open(self.checkpoint_file, 'r') as f:
                data = json.load(f)
                self.processed_urls = set(data.get('processed_urls', []))
                logger.info(f"Loaded checkpoint: {len(self.processed_urls)} URLs already processed")
        except FileNotFoundError:
            self.processed_urls = set()

    def save_checkpoint(self):
        """Save checkpoint of processed URLs"""
        with open(self.checkpoint_file, 'w') as f:
            json.dump({'processed_urls': list(self.processed_urls)}, f)

    def parse_url(self, url):
        """Extract ID and name from GPT URL"""
        match = re.match(r'https://chatgpt\.com/g/(g-[a-zA-Z0-9]+)(?:-(.+))?', url)
        if match:
            gpt_id = match.group(1)
            name = match.group(2).replace('-', ' ') if match.group(2) else ''
            return gpt_id, name
        return None, None

    def search_serper(self, query):
        """Search using Serper API"""
        url = "https://google.serper.dev/search"

        payload = {
            'q': query,
            'num': 10
        }

        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Serper API error for '{query[:40]}...': {e}")
            return None

    def extract_gpts_from_results(self, search_results, query):
        """Extract all GPT URLs and descriptions from search results"""
        gpts = []

        if not search_results:
            return gpts

        # Check organic results
        for result in search_results.get('organic', []):
            link = result.get('link', '')
            snippet = result.get('snippet', '')
            title = result.get('title', '')

            # Check if this result contains a GPT URL
            if 'chatgpt.com/g/g-' in link:
                gpts.append({
                    'url': link,
                    'description': snippet,
                    'source_query': query
                })

            # Also check if the snippet or title mentions other GPT URLs
            gpt_urls = re.findall(r'https://chatgpt\.com/g/g-[a-zA-Z0-9\-]+', snippet + ' ' + title)
            for url in gpt_urls:
                if url != link:  # Don't duplicate the main link
                    gpts.append({
                        'url': url,
                        'description': snippet,
                        'source_query': query
                    })

        # Check related searches or people also ask sections
        for result in search_results.get('peopleAlsoAsk', []):
            snippet = result.get('snippet', '')
            gpt_urls = re.findall(r'https://chatgpt\.com/g/g-[a-zA-Z0-9\-]+', snippet)
            for url in gpt_urls:
                gpts.append({
                    'url': url,
                    'description': snippet,
                    'source_query': query
                })

        return gpts

    def save_to_csv(self, gpts):
        """Thread-safe append to CSV file"""
        if not gpts:
            return

        with self.csv_lock:
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
        # Skip if already processed
        if url in self.processed_urls:
            return url, []

        gpt_id, name = self.parse_url(url)
        if not gpt_id:
            logger.warning(f"Could not parse URL: {url}")
            return url, []

        # Build search query
        query = f"chatgpt {gpt_id} {name}"

        # Search
        results = self.search_serper(query)

        if not results:
            return url, []

        # Extract GPTs
        gpts = self.extract_gpts_from_results(results, query)

        # Save immediately
        self.save_to_csv(gpts)

        # Mark as processed
        with self.csv_lock:
            self.processed_urls.add(url)

        return url, gpts

    def process_batch_parallel(self, urls, checkpoint_interval=100):
        """Process URLs in parallel using ThreadPoolExecutor"""
        # Filter out already processed URLs
        urls_to_process = [url for url in urls if url not in self.processed_urls]

        logger.info(f"URLs to process: {len(urls_to_process)}")
        logger.info(f"Already processed: {len(self.processed_urls)}")
        logger.info(f"Using {self.max_workers} parallel workers")

        total_found = 0
        processed_count = 0

        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_url = {executor.submit(self.process_url, url): url for url in urls_to_process}

                # Process completed tasks
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    processed_count += 1

                    try:
                        original_url, gpts = future.result()

                        if gpts:
                            logger.info(f"[{processed_count}/{len(urls_to_process)}] ✓ {original_url[:60]}... - Found {len(gpts)} GPT(s)")
                            total_found += len(gpts)
                        else:
                            logger.info(f"[{processed_count}/{len(urls_to_process)}] ✗ {original_url[:60]}... - No GPTs")

                        # Save checkpoint periodically
                        if processed_count % checkpoint_interval == 0:
                            self.save_checkpoint()
                            logger.info(f"Checkpoint saved ({processed_count} URLs processed)")

                    except Exception as e:
                        logger.error(f"Error processing {url}: {e}")

        except KeyboardInterrupt:
            logger.info("\nInterrupted by user. Saving checkpoint...")
            self.save_checkpoint()
            logger.info(f"Checkpoint saved. {processed_count} URLs processed.")
            raise

        # Final checkpoint
        self.save_checkpoint()

        logger.info(f"\n{'='*60}")
        logger.info(f"Total GPTs collected: {total_found}")
        logger.info(f"URLs processed: {processed_count}")
        logger.info(f"Results saved to: {self.csv_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Parallel GPT collector using Serper API')
    parser.add_argument('--workers', '-w', type=int, default=5, help='Number of parallel workers (default: 5)')
    parser.add_argument('--limit', '-l', type=int, help='Limit number of URLs to process')
    parser.add_argument('--checkpoint-interval', '-c', type=int, default=100, help='Checkpoint save interval')

    args = parser.parse_args()

    # Load all URLs from file
    urls = []
    with open('valid-gpt-urls.txt', 'r') as f:
        for line in f:
            url = line.strip()
            if url:
                urls.append(url)
                if args.limit and len(urls) >= args.limit:
                    break

    logger.info(f"Loaded {len(urls)} URLs to process")
    logger.info(f"Workers: {args.workers}")
    logger.info("Starting parallel collection...")
    logger.info("Press Ctrl+C to stop and save checkpoint")

    collector = ParallelSerperCollector(max_workers=args.workers)

    try:
        collector.process_batch_parallel(urls, checkpoint_interval=args.checkpoint_interval)
    except Exception as e:
        if 'credit' in str(e).lower() or 'limit' in str(e).lower() or '429' in str(e):
            logger.info("\n" + "="*60)
            logger.info("Serper API credits exhausted!")
            logger.info(f"Partial results saved to: {collector.csv_file}")
        else:
            logger.error(f"Error occurred: {e}")
            raise


if __name__ == "__main__":
    main()