#!/usr/bin/env python3
"""
Deduplicate CSV GPT data using FastText for language detection
Removes duplicate URLs, chat-specific URLs, and URL parameters
Creates three versions:
1. Original data (unchanged)
2. Deduplicated data (all languages)
3. English-only deduplicated data
"""

import csv
import re
import os
import fasttext
import urllib.request
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


class FastTextLanguageDetector:
    def __init__(self):
        """Initialize FastText language detector with pre-trained model"""
        self.model_path = Path("lid.176.bin")

        # Download model if not exists
        if not self.model_path.exists():
            logger.info("Downloading FastText language identification model...")
            url = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
            urllib.request.urlretrieve(url, self.model_path)
            logger.info(f"Model downloaded to {self.model_path}")

        # Load the model
        logger.info("Loading FastText language model...")
        # Suppress FastText warnings
        fasttext.FastText.eprint = lambda x: None
        self.model = fasttext.load_model(str(self.model_path))
        logger.info("FastText model loaded successfully")

    def detect_language(self, text: str) -> tuple:
        """
        Detect language of text
        Returns: (language_code, confidence)
        """
        if not text or len(text.strip()) < 10:
            return ('en', 0.5)  # Default to English for very short texts

        # Clean text for better detection
        text = text.replace('\n', ' ').strip()

        # Workaround for NumPy 2.x compatibility issue
        import numpy as np
        old_copy = np.array  # Store original

        try:
            # Temporarily replace np.array to handle copy parameter
            def array_wrapper(obj, *args, **kwargs):
                if 'copy' in kwargs and not kwargs['copy']:
                    kwargs.pop('copy')
                    return np.asarray(obj)
                return old_copy(obj, *args, **kwargs)

            np.array = array_wrapper

            # Predict language
            predictions = self.model.predict(text, k=1)  # Get top prediction

        finally:
            np.array = old_copy  # Restore original

        # Extract language code and confidence
        lang_label = predictions[0][0]  # Format: '__label__en'
        confidence = predictions[1][0]

        # Extract the language code
        lang_code = lang_label.replace('__label__', '')

        return (lang_code, confidence)

    def is_english(self, text: str, confidence_threshold: float = 0.5) -> bool:
        """
        Check if text is in English with confidence threshold
        """
        lang_code, confidence = self.detect_language(text)

        # Consider it English if:
        # 1. Detected as English with sufficient confidence
        # 2. Very short text (default assumption)
        if not text or len(text.strip()) < 10:
            return True

        return lang_code == 'en' and confidence >= confidence_threshold


def clean_url(url: str) -> str:
    """
    Clean GPT URL by removing:
    - Query parameters (locale, utm_source, etc.)
    - Chat-specific patterns
    - Trailing slashes
    """
    # Remove query parameters
    if '?' in url:
        url = url.split('?')[0]

    # Remove locale parameters embedded in path
    url = re.sub(r'\?locale=[a-z\-A-Z]+', '', url)

    # Remove trailing slashes
    url = url.rstrip('/')

    # Ensure it's a GPT URL (not a chat URL)
    if '/g/g-' not in url:
        return None

    return url


def extract_gpt_id(url: str) -> str:
    """Extract the GPT ID from a URL"""
    match = re.search(r'/g/(g-[A-Za-z0-9]+)', url)
    return match.group(1) if match else None


def deduplicate_csv(input_file: str, output_all: str, output_english: str, detector: FastTextLanguageDetector):
    """
    Deduplicate CSV data and create filtered versions

    Args:
        input_file: Original CSV file
        output_all: Deduplicated CSV (all languages)
        output_english: Deduplicated CSV (English only)
        detector: FastText language detector instance
    """
    # Dictionary to store best entry for each GPT ID
    # Key: GPT ID, Value: (url, description, source_query, is_english, lang_confidence)
    id_to_entry = {}

    total_rows = 0
    skipped_invalid = 0
    language_stats = {}

    # Read CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            total_rows += 1

            if total_rows % 1000 == 0:
                logger.info(f"Processing row {total_rows}...")

            url = row.get('url', '').strip()
            description = row.get('description', '').strip()
            source_query = row.get('source_query', '').strip()

            # Clean URL
            clean_url_str = clean_url(url)
            if not clean_url_str:
                skipped_invalid += 1
                continue

            # Extract GPT ID
            gpt_id = extract_gpt_id(clean_url_str)
            if not gpt_id:
                skipped_invalid += 1
                continue

            # Detect language with FastText
            lang_code, confidence = detector.detect_language(description)
            is_eng = (lang_code == 'en')

            # Track language statistics
            if lang_code not in language_stats:
                language_stats[lang_code] = 0
            language_stats[lang_code] += 1

            # Determine if this entry should replace existing one
            should_replace = False

            if gpt_id not in id_to_entry:
                # New GPT ID
                should_replace = True
            else:
                existing = id_to_entry[gpt_id]

                # Prefer entries with:
                # 1. Higher language detection confidence
                # 2. Longer, more descriptive URLs (with name)
                # 3. Longer descriptions
                # 4. English descriptions

                url_score_new = len(clean_url_str)
                url_score_existing = len(existing[0])

                desc_score_new = len(description)
                desc_score_existing = len(existing[1])

                # Use confidence scores for language preference
                lang_score_new = (10 if is_eng else 0) + (confidence * 5)
                lang_score_existing = (10 if existing[3] else 0) + (existing[4] * 5)

                score_new = url_score_new + desc_score_new + lang_score_new
                score_existing = url_score_existing + desc_score_existing + lang_score_existing

                if score_new > score_existing:
                    should_replace = True

            if should_replace:
                id_to_entry[gpt_id] = (clean_url_str, description, source_query, is_eng, confidence)

    # Sort by GPT ID
    sorted_entries = sorted(id_to_entry.items())

    # Write deduplicated CSV (all languages)
    with open(output_all, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'description', 'source_query'])

        for gpt_id, (url, desc, source, is_eng, conf) in sorted_entries:
            writer.writerow([url, desc, source])

    # Write English-only CSV
    english_entries = [(gpt_id, data) for gpt_id, data in sorted_entries if data[3]]

    with open(output_english, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'description', 'source_query'])

        for gpt_id, (url, desc, source, is_eng, conf) in english_entries:
            writer.writerow([url, desc, source])

    # Statistics
    stats = {
        'total_rows': total_rows,
        'skipped_invalid': skipped_invalid,
        'unique_gpts': len(sorted_entries),
        'english_gpts': len(english_entries),
        'non_english_gpts': len(sorted_entries) - len(english_entries),
        'duplicates_removed': total_rows - len(sorted_entries),
        'language_distribution': dict(sorted(language_stats.items(), key=lambda x: x[1], reverse=True)[:10])
    }

    return stats


def main():
    import sys

    # Allow optional test mode with smaller file
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        input_file = 'test_sample.csv'
        output_all = 'test_deduplicated.csv'
        output_english = 'test_english_only.csv'
    else:
        input_file = 'outputs/serper_collected_gpts_cleaned.csv'
        output_all = 'outputs/serper_collected_gpts_deduplicated.csv'
        output_english = 'outputs/serper_collected_gpts_english_only.csv'

    logger.info("Initializing FastText language detector...")
    detector = FastTextLanguageDetector()

    logger.info(f"Processing {input_file}...")
    logger.info("This will create:")
    logger.info(f"  1. Original: {input_file} (unchanged)")
    logger.info(f"  2. Deduplicated: {output_all}")
    logger.info(f"  3. English-only: {output_english}")
    logger.info("")

    stats = deduplicate_csv(input_file, output_all, output_english, detector)

    logger.info("=" * 60)
    logger.info("DEDUPLICATION COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Total rows processed:     {stats['total_rows']:,}")
    logger.info(f"Invalid URLs skipped:     {stats['skipped_invalid']:,}")
    logger.info(f"Duplicates removed:       {stats['duplicates_removed']:,}")
    logger.info(f"")
    logger.info(f"Unique GPTs:              {stats['unique_gpts']:,}")
    logger.info(f"  - English:              {stats['english_gpts']:,}")
    logger.info(f"  - Non-English:          {stats['non_english_gpts']:,}")
    logger.info("")
    logger.info("Top 10 languages detected:")
    for lang, count in stats['language_distribution'].items():
        logger.info(f"  - {lang}: {count:,}")
    logger.info("")
    logger.info(f"✓ Saved to: {output_all}")
    logger.info(f"✓ Saved to: {output_english}")


if __name__ == "__main__":
    main()