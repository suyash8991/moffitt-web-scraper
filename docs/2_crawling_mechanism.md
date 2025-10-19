# Moffitt Cancer Center Web Scraper: Crawling Mechanism

## 1. Crawling Architecture Overview

The web crawling functionality is implemented in `src/crawl.py` through the `ResearcherCrawler` class. This module is responsible for fetching HTML content from researcher profile pages with sophisticated rate limiting and error handling.

```python
class ResearcherCrawler:
    def __init__(self, output_dir='data/raw_html', respect_robots=True):
        # Initialize crawler with output directory and robots.txt settings

    async def crawl_url(self, url):
        # Fetch a single URL with rate limiting

    async def crawl_urls(self, urls):
        # Process multiple URLs with concurrency controls
```

The crawler uses asynchronous programming (with Python's `asyncio`) to efficiently handle web requests while maintaining proper rate limiting.

## 2. Rate Limiting Implementation

The system implements a sophisticated rate limiting mechanism to ensure ethical crawling and prevent server overload:

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│               │     │               │     │               │     │               │
│ Request 1     │────▶│ Wait 2-5s     │────▶│ Request 2     │────▶│ Wait 2-5s     │
│               │     │               │     │               │     │               │
└───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘
```

### 2.1 Rate Limiting Constants

The crawler defines several constants to control request frequency:

```python
# Constants for rate limiting
MIN_DELAY = 2.0  # Minimum delay between requests in seconds
MAX_DELAY = 5.0  # Maximum delay between requests in seconds
MAX_CONCURRENT = 3  # Maximum concurrent requests
```

### 2.2 Delay Mechanism

Each request uses a randomized delay between the minimum and maximum values to avoid detection patterns:

```python
async def _wait_for_rate_limit(self):
    """Wait to respect rate limiting."""
    now = time.time()
    elapsed = now - self.last_request_time

    # Random delay between MIN_DELAY and MAX_DELAY
    delay = random.uniform(MIN_DELAY, MAX_DELAY)

    # If we need to wait more, do so
    if elapsed < delay:
        await asyncio.sleep(delay - elapsed)

    self.last_request_time = time.time()
```

### 2.3 Concurrency Control

The system uses an asyncio Semaphore to limit the number of concurrent requests, ensuring the server is not overwhelmed:

```python
self.semaphore = asyncio.Semaphore(MAX_CONCURRENT)
```

In the `crawl_url` method, the semaphore is used:

```python
async with self.semaphore:
    # Perform the actual web request
```

## 3. HTML Fetching with crawl4ai

The crawler leverages the `crawl4ai` library to handle the actual HTTP requests and content processing:

```python
async with AsyncWebCrawler() as crawler:
    crawl_result = await crawler.arun(
        url=url,
        respect_robots_txt=self.respect_robots
    )
```

### 3.1 Key Features of crawl4ai

- **JavaScript Rendering**: Handles dynamic content that requires JavaScript execution
- **Markdown Conversion**: Automatically converts HTML to more processable Markdown
- **Robots.txt Compliance**: Respects website crawling directives (configurable)

### 3.2 Error Handling

The crawling process is wrapped in a try/except block to gracefully handle various issues:
- Network errors
- Timeouts
- Invalid URLs
- Server errors

```python
try:
    # Crawling code
    # ...
except Exception as e:
    error_msg = f"Error crawling {url}: {str(e)}"
    logger.error(error_msg)
    result['error'] = error_msg
    return result
```

## 4. Output File Management

For each successfully crawled URL, the crawler saves the raw HTML content to disk:

```python
async def _save_html(self, filename, content):
    """Save HTML content to a file."""
    file_path = os.path.join(self.output_dir, filename)
    try:
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(content)
        logger.info(f"Saved HTML to {file_path}")
    except Exception as e:
        logger.error(f"Error saving HTML to {file_path}: {e}")
```

### 4.1 Filename Generation

The crawler extracts the researcher name from the URL path to use as the filename:

```python
def _get_filename(self, url):
    """Generate a filename for the given URL."""
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')

    # Use the last part of the path as the base filename
    base_name = path_parts[-1] if path_parts else 'index'

    return f"{base_name}.html"
```

## 5. Crawling Process Flow Diagram

The complete flow for processing a single URL:

```
┌──────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│              │     │               │     │               │     │               │
│ Start        │────▶│ Wait for      │────▶│ Fetch with    │────▶│ Save HTML     │
│ Request      │     │ Rate Limit    │     │ Semaphore     │     │ to Disk       │
│              │     │               │     │               │     │               │
└──────────────┘     └───────────────┘     └───────────────┘     └───────────────┘
                                                  │
                                                  │
                                                  ▼
                          ┌───────────────────────────────────────┐
                          │                                       │
                          │ Return Result Dictionary              │
                          │ (url, success, html, markdown, error) │
                          │                                       │
                          └───────────────────────────────────────┘
```

## 6. Result Format

For each crawled URL, the system returns a dictionary with:

```python
result = {
    'url': url,             # Original URL
    'success': True/False,  # Boolean indicating success/failure
    'html': '...',          # Raw HTML content
    'markdown': '...',      # Converted Markdown content
    'error': None           # Error message (if applicable)
}
```

## 7. Batch Processing

The `crawl_urls` method handles processing multiple URLs, leveraging the asyncio library for better performance:

```python
async def crawl_urls(self, urls):
    """Crawl multiple URLs with rate limiting and error handling."""
    logger.info(f"Starting to crawl {len(urls)} URLs")

    tasks = [self.crawl_url(url) for url in urls]
    results = await asyncio.gather(*tasks)

    # Log summary
    success_count = sum(1 for r in results if r['success'])
    logger.info(f"Crawl complete: {success_count}/{len(urls)} successful")

    return results
```

## 8. Integration with Main Pipeline

The crawler is integrated into the main pipeline through the `MoffittResearcherScraper` class in `main.py`:

```python
# Initialize components
self.crawler = ResearcherCrawler(output_dir=self.output_dirs["raw_html"])

# ... later in process_researcher method
crawl_result = await self.crawler.crawl_url(url)

if not crawl_result['success']:
    logger.error(f"Failed to crawl {url}: {crawl_result.get('error', 'Unknown error')}")
    return None

# Use markdown result for further processing
markdown_content = crawl_result['markdown']
```

## 9. Ethical Considerations

The crawler is designed with ethical web scraping principles in mind:
- Proper rate limiting to avoid server overload
- Respect for robots.txt directives
- Clear user-agent identification
- Error handling to avoid repeated failing requests