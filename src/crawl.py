"""
Module for crawling researcher profile pages with proper error handling and rate limiting.
"""
import asyncio
import logging
import os
import time
import random
from urllib.parse import urlparse
from crawl4ai import AsyncWebCrawler
import aiofiles

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants for rate limiting
MIN_DELAY = 2.0  # Minimum delay between requests in seconds
MAX_DELAY = 5.0  # Maximum delay between requests in seconds
MAX_CONCURRENT = 3  # Maximum concurrent requests


class ResearcherCrawler:
    """
    Crawler for Moffitt researcher profiles with rate limiting and error handling.
    """

    def __init__(self, output_dir='data/raw_html', respect_robots=True):
        """
        Initialize the crawler.

        Args:
            output_dir (str): Directory to save raw HTML files
            respect_robots (bool): Whether to respect robots.txt
        """
        self.output_dir = output_dir
        self.respect_robots = respect_robots
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT)
        self.last_request_time = 0

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

    async def _wait_for_rate_limit(self):
        """
        Wait to respect rate limiting.
        """
        now = time.time()
        elapsed = now - self.last_request_time

        # Random delay between MIN_DELAY and MAX_DELAY
        delay = random.uniform(MIN_DELAY, MAX_DELAY)

        # If we need to wait more, do so
        if elapsed < delay:
            await asyncio.sleep(delay - elapsed)

        self.last_request_time = time.time()

    def _get_filename(self, url):
        """
        Generate a filename for the given URL.

        Args:
            url (str): The URL to generate a filename for

        Returns:
            str: The generated filename
        """
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')

        # Use the last part of the path as the base filename
        base_name = path_parts[-1] if path_parts else 'index'

        return f"{base_name}.html"

    async def _save_html(self, filename, content):
        """
        Save HTML content to a file.

        Args:
            filename (str): The filename to save to
            content (str): The HTML content to save
        """
        file_path = os.path.join(self.output_dir, filename)
        try:
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(content)
            logger.info(f"Saved HTML to {file_path}")
        except Exception as e:
            logger.error(f"Error saving HTML to {file_path}: {e}")

    async def crawl_url(self, url):
        """
        Crawl a single URL with rate limiting and error handling.

        Args:
            url (str): The URL to crawl

        Returns:
            dict: A dictionary with keys 'url', 'success', 'html', 'markdown', 'error'
        """
        # Initialize result dictionary
        result = {
            'url': url,
            'success': False,
            'html': None,
            'markdown': None,
            'error': None
        }

        # Rate limit
        await self._wait_for_rate_limit()

        try:
            # Use semaphore to limit concurrent requests
            async with self.semaphore:
                logger.info(f"Crawling {url}")

                # Use Crawl4AI to fetch the page
                async with AsyncWebCrawler() as crawler:
                    # Pass the respect_robots_txt parameter directly if supported
                    # or just use the default settings if not
                    try:
                        crawl_result = await crawler.arun(
                            url=url,
                            respect_robots_txt=self.respect_robots
                        )
                    except TypeError:
                        # If respect_robots_txt isn't a supported parameter, use the default call
                        logger.info("Using default crawler settings (respect_robots_txt parameter not supported)")
                        crawl_result = await crawler.arun(
                            url=url
                        )

                # Extract results
                result['html'] = crawl_result.html
                result['markdown'] = crawl_result.markdown
                result['success'] = True

                # Save the HTML content
                filename = self._get_filename(url)
                await self._save_html(filename, crawl_result.html)

                return result

        except Exception as e:
            error_msg = f"Error crawling {url}: {str(e)}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result

    async def crawl_urls(self, urls):
        """
        Crawl multiple URLs with rate limiting and error handling.

        Args:
            urls (list): List of URLs to crawl

        Returns:
            list: List of result dictionaries
        """
        logger.info(f"Starting to crawl {len(urls)} URLs")

        tasks = [self.crawl_url(url) for url in urls]
        results = await asyncio.gather(*tasks)

        # Log summary
        success_count = sum(1 for r in results if r['success'])
        logger.info(f"Crawl complete: {success_count}/{len(urls)} successful")

        return results


async def crawl_researcher_profiles(urls, output_dir='data/raw_html'):
    """
    Crawl researcher profile pages.

    Args:
        urls (list): List of URLs to crawl
        output_dir (str): Directory to save raw HTML files

    Returns:
        list: List of result dictionaries
    """
    crawler = ResearcherCrawler(output_dir=output_dir)
    return await crawler.crawl_urls(urls)


# If run as a script, test with a sample URL
if __name__ == "__main__":
    async def test():
        sample_url = "https://www.moffitt.org/research-science/researchers/michael-vogelbaum/"
        crawler = ResearcherCrawler()
        result = await crawler.crawl_url(sample_url)
        if result['success']:
            print(f"Successfully crawled {sample_url}")
            print(f"Markdown snippet: {result['markdown'][:200]}...")
        else:
            print(f"Failed to crawl {sample_url}: {result['error']}")

    asyncio.run(test())