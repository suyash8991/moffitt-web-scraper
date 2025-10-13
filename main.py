"""
Moffitt Cancer Center Researcher Data Scraper

This script scrapes researcher profiles from the Moffitt Cancer Center website,
processes the data, and stores it in a structured format.

Usage:
  python main.py [--excel EXCEL_FILE] [--url URL] [--limit N]

Options:
  --excel EXCEL_FILE    Path to Excel file with researcher URLs (default: researcher_links.xlsx)
  --url URL             Single researcher URL to scrape
  --limit N             Limit the number of researchers to process

Example:
  python main.py                          # Process all URLs in the Excel file
  python main.py --url https://...        # Process a single URL
  python main.py --limit 5                # Process first 5 URLs from the Excel file
"""

import os
import sys
import json
import asyncio
import argparse
import logging
from datetime import datetime
from urllib.parse import urlparse

# Import our modules
from src.url_reader import read_urls_from_excel
from src.crawl import ResearcherCrawler
from src.parse import ResearcherProfileParser

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("moffitt_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MoffittResearcherScraper:
    """
    Main class for scraping, processing, and storing researcher data.
    """

    def __init__(self, output_base_dir="data"):
        """
        Initialize the scraper.

        Args:
            output_base_dir (str): Base directory for output files
        """
        # Set up output directories
        self.output_dirs = {
            "raw_html": os.path.join(output_base_dir, "raw_html"),
            "markdown": os.path.join(output_base_dir, "markdown"),
            "processed": os.path.join(output_base_dir, "processed")
        }

        # Create output directories if they don't exist
        for dir_path in self.output_dirs.values():
            os.makedirs(dir_path, exist_ok=True)

        # Initialize components
        self.crawler = ResearcherCrawler(output_dir=self.output_dirs["raw_html"])
        self.parser = ResearcherProfileParser()

    async def process_researcher(self, url):
        """
        Process a single researcher URL.

        Args:
            url (str): URL of the researcher profile

        Returns:
            dict: Processed researcher data or None if failed
        """
        try:
            logger.info(f"Processing researcher: {url}")

            # Extract researcher name from URL
            path_parts = urlparse(url).path.strip('/').split('/')
            researcher_name = path_parts[-1] if path_parts else 'unknown'

            # Step 1: Crawl the URL to get HTML and markdown
            crawl_result = await self.crawler.crawl_url(url)

            if not crawl_result['success']:
                logger.error(f"Failed to crawl {url}: {crawl_result.get('error', 'Unknown error')}")
                return None

            # Step 2: Save markdown to file
            markdown_filename = os.path.join(self.output_dirs["markdown"], f"{researcher_name}.md")
            with open(markdown_filename, 'w', encoding='utf-8') as f:
                f.write(crawl_result['markdown'])
            logger.info(f"Saved markdown to {markdown_filename}")

            # Step 3: Parse markdown to structured data
            researcher_data = self.parser.parse_markdown(crawl_result['markdown'], url)

            # Step 4: Save structured data to JSON
            json_filename = os.path.join(self.output_dirs["processed"], f"{researcher_name}.json")
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(researcher_data, f, indent=2)
            logger.info(f"Saved structured data to {json_filename}")

            return researcher_data

        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            return None

    async def process_researchers(self, urls, limit=None):
        """
        Process multiple researcher URLs.

        Args:
            urls (list): List of researcher profile URLs
            limit (int, optional): Limit the number of URLs to process

        Returns:
            list: List of processed researcher data
        """
        if limit and limit > 0:
            urls = urls[:limit]

        logger.info(f"Processing {len(urls)} researcher profiles...")

        # Process URLs sequentially to be respectful to the server
        results = []
        for url in urls:
            result = await self.process_researcher(url)
            if result:
                results.append(result)

        logger.info(f"Successfully processed {len(results)}/{len(urls)} researcher profiles")
        return results

    @staticmethod
    def generate_summary(researchers):
        """
        Generate a summary of processed researcher data.

        Args:
            researchers (list): List of processed researcher data

        Returns:
            dict: Summary statistics
        """
        if not researchers:
            return {"count": 0}

        programs = {}
        departments = {}
        research_interests = {}

        for r in researchers:
            # Count by program
            program = r.get('primary_program', '')
            if program:
                programs[program] = programs.get(program, 0) + 1

            # Count by department
            dept = r.get('department', '')
            if dept:
                departments[dept] = departments.get(dept, 0) + 1

            # Count research interests
            for interest in r.get('research_interests', []):
                research_interests[interest] = research_interests.get(interest, 0) + 1

        return {
            "count": len(researchers),
            "programs": programs,
            "departments": departments,
            "top_research_interests": dict(sorted(research_interests.items(), key=lambda x: x[1], reverse=True)[:10])
        }


async def main():
    """
    Main function to run the scraper.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Scrape researcher profiles from Moffitt Cancer Center")
    parser.add_argument("--excel", help="Path to Excel file with researcher URLs", default="researcher_links.xlsx")
    parser.add_argument("--url", help="Single researcher URL to scrape")
    parser.add_argument("--limit", type=int, help="Limit the number of researchers to process")
    args = parser.parse_args()

    # Initialize scraper
    scraper = MoffittResearcherScraper()

    if args.url:
        # Process a single URL
        await scraper.process_researcher(args.url)
    else:
        # Read URLs from Excel file
        urls = read_urls_from_excel(args.excel)
        if not urls:
            logger.error(f"No URLs found in Excel file: {args.excel}")
            return

        # Process URLs
        researchers = await scraper.process_researchers(urls, args.limit)

        # Generate summary
        summary = scraper.generate_summary(researchers)

        # Save summary to file
        summary_filename = os.path.join("data", "processed", "summary.json")
        with open(summary_filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Processed {summary['count']} researchers. Summary saved to {summary_filename}")


if __name__ == "__main__":
    asyncio.run(main())