# Moffitt Cancer Center Web Scraper: Usage and Main Script

## 1. Main Script Overview

The main script (`main.py`) serves as the orchestrator for the entire web scraping pipeline. It provides a command-line interface for various operations and coordinates the flow between different components.

## 2. Command-Line Interface

The script supports several command-line options for flexible usage:

```
Usage:
  python main.py [--excel EXCEL_FILE] [--url URL] [--department DEPT] [--limit N]

Options:
  --excel EXCEL_FILE    Path to Excel file with researcher URLs (default: researcher_links.xlsx)
  --url URL             Single researcher URL to scrape
  --department DEPT     Department for the single URL (when using --url)
  --limit N             Limit the number of researchers to process
```

This interface is implemented using the `argparse` module:

```python
# Parse command line arguments
parser = argparse.ArgumentParser(description="Scrape researcher profiles from Moffitt Cancer Center")
parser.add_argument("--excel", help="Path to Excel file with researcher URLs", default="researcher_links.xlsx")
parser.add_argument("--url", help="Single researcher URL to scrape")
parser.add_argument("--department", help="Department for the single URL (when using --url)")
parser.add_argument("--limit", type=int, help="Limit the number of researchers to process")
args = parser.parse_args()
```

## 3. Main Script Architecture

The main script defines the `MoffittResearcherScraper` class which orchestrates the entire pipeline:

```python
class MoffittResearcherScraper:
    """
    Main class for scraping, processing, and storing researcher data.
    """

    def __init__(self, output_base_dir="data"):
        # Initialize directories and components

    async def process_researcher(self, url, department=""):
        # Process a single researcher URL

    async def process_researchers(self, urls_data, limit=None):
        # Process multiple researcher URLs

    @staticmethod
    def generate_summary(researchers):
        # Generate summary statistics
```

The `main()` function handles the command-line arguments and initiates the appropriate processing:

```python
async def main():
    """
    Main function to run the scraper.
    """
    # Parse command line arguments
    # ...

    # Initialize scraper
    scraper = MoffittResearcherScraper()

    if args.url:
        # Process a single URL with optional department
        await scraper.process_researcher(args.url, args.department or "")
    else:
        # Read URLs and department info from Excel file
        urls_data = read_urls_from_excel(args.excel)
        if not urls_data:
            logger.error(f"No URLs found in Excel file: {args.excel}")
            return

        # Process URLs with their department info
        researchers = await scraper.process_researchers(urls_data, args.limit)

        # Generate summary
        summary = scraper.generate_summary(researchers)

        # Save summary to file
        # ...
```

## 4. Usage Examples

### 4.1 Processing All Researchers from Excel

To process all researchers listed in the Excel file:

```bash
python main.py
```

This command:
1. Reads `researcher_links.xlsx` for URLs and department information
2. Processes each URL sequentially with rate limiting
3. Generates a summary of all processed researchers

### 4.2 Processing a Single Researcher

To process a specific researcher URL:

```bash
python main.py --url "https://www.moffitt.org/research-science/researchers/ahmad-tarhini/" --department "Immunology"
```

This command:
1. Processes only the specified URL
2. Uses the provided department information
3. Saves the results to the standard output locations

### 4.3 Limiting the Number of Researchers

To process only a subset of researchers:

```bash
python main.py --limit 5
```

This command:
1. Processes only the first 5 researchers from the Excel file
2. Useful for testing the pipeline without processing all URLs

### 4.4 Using a Custom Excel File

To use a different Excel file as the source:

```bash
python main.py --excel "custom_researchers.xlsx"
```

This command:
1. Reads URLs and department information from the specified Excel file
2. Follows the same processing pipeline as the default command

## 5. Process Flow

### 5.1 Single Researcher Processing Flow

```
┌──────────────┐     ┌─────────────────┐     ┌─────────────────┐
│              │     │                 │     │                 │
│ Extract Name │────▶│ Crawl URL       │────▶│ Save Markdown   │
│ from URL     │     │ (HTML+Markdown) │     │ to File         │
│              │     │                 │     │                 │
└──────────────┘     └─────────────────┘     └─────────────────┘
                                                     │
                                                     ▼
┌──────────────┐     ┌─────────────────┐     ┌─────────────────┐
│              │     │                 │     │                 │
│ Save JSON    │◀────│ Add Department  │◀────│ Parse Markdown  │
│ to File      │     │ Information     │     │ to JSON         │
│              │     │                 │     │                 │
└──────────────┘     └─────────────────┘     └─────────────────┘
```

### 5.2 Multiple Researchers Processing Flow

```
┌──────────────┐     ┌─────────────────┐     ┌─────────────────┐
│              │     │                 │     │                 │
│ Read URLs    │────▶│ Process URLs    │────▶│ Generate        │
│ from Excel   │     │ Sequentially    │     │ Summary         │
│              │     │                 │     │                 │
└──────────────┘     └─────────────────┘     └─────────────────┘
                           │                         │
                           ▼                         ▼
                     ┌─────────────────┐     ┌─────────────────┐
                     │                 │     │                 │
                     │ Individual      │     │ Save Summary    │
                     │ Processing Flow │     │ to JSON File    │
                     │                 │     │                 │
                     └─────────────────┘     └─────────────────┘
```

## 6. Key Components of the Main Script

### 6.1 MoffittResearcherScraper Class

The central orchestrator class has these key responsibilities:

1. **Directory Management**: Creates and manages output directories
   ```python
   # Set up output directories
   self.output_dirs = {
       "raw_html": os.path.join(output_base_dir, "raw_html"),
       "markdown": os.path.join(output_base_dir, "markdown"),
       "processed": os.path.join(output_base_dir, "processed")
   }
   ```

2. **Component Initialization**: Initializes the crawler and parser
   ```python
   # Initialize components
   self.crawler = ResearcherCrawler(output_dir=self.output_dirs["raw_html"])
   self.parser = ResearcherProfileParser()
   ```

3. **Single Researcher Processing**: Handles the end-to-end process for one URL
   ```python
   async def process_researcher(self, url, department=""):
       # Extract researcher name
       # Crawl URL to get HTML and markdown
       # Save markdown to file
       # Parse markdown to structured data
       # Add researcher_name and department
       # Save structured data to JSON
   ```

4. **Batch Processing**: Manages processing multiple URLs
   ```python
   async def process_researchers(self, urls_data, limit=None):
       # Process URLs sequentially with department info
       # Return list of processed researchers
   ```

5. **Summary Generation**: Creates aggregate statistics
   ```python
   @staticmethod
   def generate_summary(researchers):
       # Count by program, department, research interests
       # Return summary dictionary
   ```

### 6.2 Error Handling

The main script implements comprehensive error handling:

```python
try:
    # Processing code
    # ...
except Exception as e:
    logger.error(f"Error processing {url}: {str(e)}")
    return None
```

This ensures that a failure with one researcher doesn't stop the entire pipeline.

### 6.3 Logging

The script sets up detailed logging to both console and file:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("moffitt_scraper.log"),
        logging.StreamHandler()
    ]
)
```

This provides visibility into the scraping process and helps with debugging.

## 7. Performance Considerations

### 7.1 Sequential Processing

The script processes URLs sequentially to be respectful to the server:

```python
# Process URLs sequentially to be respectful to the server
results = []
for url in urls:
    # Get department from the dictionary
    department = urls_data.get(url, "")

    # Process the researcher with the department info
    result = await self.process_researcher(url, department)
    if result:
        results.append(result)
```

This approach, combined with the rate limiting in the crawler, ensures ethical web scraping.

### 7.2 Asyncio Integration

The script uses Python's asyncio for better performance:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

This allows for efficient I/O operations while maintaining sequential processing of URLs.

## 8. Example Output

### 8.1 Terminal Output

When running the script, you'll see output similar to:

```
2025-10-18 15:30:45 - __main__ - INFO - Processing 3 researcher profiles...
2025-10-18 15:30:45 - src.crawl - INFO - Crawling https://www.moffitt.org/research-science/researchers/ahmad-tarhini/
2025-10-18 15:30:49 - src.crawl - INFO - Saved HTML to data/raw_html/ahmad-tarhini.html
2025-10-18 15:30:49 - __main__ - INFO - Saved markdown to data/markdown/ahmad-tarhini.md
2025-10-18 15:30:49 - __main__ - INFO - Saved structured data to data/processed/ahmad-tarhini.json
...
2025-10-18 15:31:58 - __main__ - INFO - Successfully processed 3/3 researcher profiles
2025-10-18 15:31:58 - __main__ - INFO - Processed 3 researchers. Summary saved to data/processed/summary.json
```

### 8.2 Summary JSON Example

The generated summary will look like:

```json
{
  "count": 3,
  "programs": {
    "Cutaneous Oncology": 1,
    "Molecular Medicine Program": 1,
    "Immuno-Oncology Program": 1
  },
  "departments": {
    "Immunology": 2,
    "Tumor Microenvironment and Metastasis": 1
  },
  "top_research_interests": {
    "As a clinical and translational physician-scientist...": 1,
    "Dr. Chiappori's research interests include...": 1,
    "The primary focus of Dr. Lazaryan's research is...": 1
  }
}
```

## 9. Advanced Usage

### 9.1 Using with Python Script

The scraper can be imported and used in another Python script:

```python
from main import MoffittResearcherScraper
import asyncio

async def run_custom_scrape():
    scraper = MoffittResearcherScraper(output_base_dir="custom_data")
    await scraper.process_researcher(
        "https://www.moffitt.org/research-science/researchers/ahmad-tarhini/",
        "Custom Department"
    )

asyncio.run(run_custom_scrape())
```

### 9.2 Custom Excel Format

If your Excel file has different column names, you can specify them explicitly:

```bash
python -c "from src.url_reader import read_urls_from_excel; print(read_urls_from_excel('custom.xlsx', url_column='Web Link', dept_column='Division'))"
```

## 10. Troubleshooting

Common issues and solutions:

1. **Excel File Not Found**: Ensure the Excel file exists in the correct location
   ```
   No URLs found in Excel file: researcher_links.xlsx
   ```

2. **URL Format Issues**: Check that URLs are properly formatted in the Excel file
   ```
   Error crawling [url]: Invalid URL
   ```

3. **Rate Limiting Too Strict**: Adjust the delay constants in `crawl.py` if needed
   ```python
   MIN_DELAY = 1.0  # Reduced from 2.0
   MAX_DELAY = 3.0  # Reduced from 5.0
   ```

4. **Missing Department Information**: Check Excel column names and data
   ```
   Could not auto-detect department column
   ```