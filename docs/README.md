# Moffitt Cancer Center Web Scraper Documentation

## Overview

This documentation covers the Moffitt Cancer Center Web Scraper, a specialized Python application designed to collect, process, and structure researcher profile information from the Moffitt Cancer Center website. The system is part of a larger project to build an Agentic RAG (Retrieval-Augmented Generation) system for analyzing researcher data.

## Documentation Sections

1. [**System Overview**](1_system_overview.md) - High-level architecture and components
   - System architecture diagram
   - Core components
   - Data flow
   - File structure
   - Technologies used

2. [**Crawling Mechanism**](2_crawling_mechanism.md) - Web crawling implementation details
   - Crawler architecture
   - Rate limiting implementation
   - HTML fetching with crawl4ai
   - Error handling
   - Output file management
   - Crawling process flow

3. [**Data Extraction Process**](3_data_extraction.md) - Parsing and structuring data
   - Parser architecture
   - Regular expression patterns
   - Extraction methods for different data types
   - Complex data handling (publications, education, grants)
   - Output data structure
   - Content hash generation

4. [**Data Storage & File Structure**](4_data_storage.md) - Data persistence approach
   - Multi-level storage architecture
   - Storage formats (HTML, Markdown, JSON)
   - Directory structure
   - JSON schema
   - Schema validation
   - Department information management
   - Summary generation

5. [**Usage & Main Script**](5_usage_and_main_script.md) - How to use the system
   - Command-line interface
   - Usage examples
   - Main script architecture
   - Error handling and logging
   - Performance considerations
   - Example output
   - Advanced usage
   - Troubleshooting

## Quick Start

To use the scraper:

```bash
# Install dependencies
pip install -r requirements.txt

# Process all researchers from Excel file
python main.py

# Process a single researcher
python main.py --url "https://www.moffitt.org/research-science/researchers/ahmad-tarhini/" --department "Immunology"

# Process limited number of researchers
python main.py --limit 5
```

## Data Input Format

The scraper expects an Excel file with the following columns:
- Program
- Department
- Researcher Name
- Profile URL

Example:
| Program | Department | Researcher Name | Profile URL |
|---------|------------|----------------|-------------|
| Molecular Medicine Program | Immunology | Ahmad Tarhini | https://www.moffitt.org/research-science/researchers/ahmad-tarhini/ |
| Molecular Medicine Program | Tumor Microenvironment and Metastasis | Alberto Chiappori | https://www.moffitt.org/research-science/researchers/alberto-chiappori/ |
| Immuno-Oncology | Immunology | Aleksandr Lazaryan | https://www.moffitt.org/research-science/researchers/aleksandr-lazaryan/ |

## Output Structure

The scraper generates three types of output:

1. **Raw HTML** (`data/raw_html/*.html`): Original webpage content
2. **Markdown** (`data/markdown/*.md`): Converted text for easier processing
3. **JSON** (`data/processed/*.json`): Structured data with consistent schema

A summary file (`data/processed/summary.json`) provides statistics across all processed researchers.

## System Requirements

- Python 3.6+
- Required packages:
  - crawl4ai>=0.7.0
  - pandas>=1.5.0
  - openpyxl>=3.1.0
  - aiofiles>=0.8.0
  - jsonschema>=4.0.0