# Moffitt Cancer Center Web Scraper: System Overview

## 1. Introduction

The Moffitt Cancer Center Web Scraper is a specialized Python application designed to collect, process, and structure researcher profile information from the Moffitt Cancer Center website. It forms part of a larger project to build an Agentic RAG (Retrieval-Augmented Generation) system that can analyze and reason over researcher data.

## 2. System Architecture

The system follows a structured pipeline approach to gather data and transform it into usable JSON format:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │     │                 │
│ Input Sources   │────▶│ Web Crawler     │────▶│ Parser          │────▶│ Storage         │
│ (Excel File)    │     │ (HTML → MD)     │     │ (MD → JSON)     │     │ (Files & JSON)  │
│                 │     │                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
                               ▲                        ▲                        ▲
                               │                        │                        │
                               │                        │                        │
                               │                        │                        │
                          ┌────┴────────────────────────┴────────────────────────┴────┐
                          │                                                           │
                          │                Main Orchestrator                          │
                          │           (MoffittResearcherScraper)                      │
                          │                                                           │
                          └───────────────────────────────────────────────────────────┘
```

## 3. Core Components

The system is built around five main components:

### 3.1. Input Source Processing (`src/url_reader.py`)
- Extracts researcher URLs and department information from Excel spreadsheets
- Auto-detects appropriate columns for URL and department data
- Returns a dictionary mapping URLs to their department information

### 3.2. Web Crawling Engine (`src/crawl.py`)
- Fetches webpage content with proper rate limiting (2-5 seconds between requests)
- Respects robots.txt directives
- Converts HTML to Markdown automatically
- Implements error handling and logging

### 3.3. Data Parsing Module (`src/parse.py`)
- Extracts structured data from Markdown using regex patterns
- Parses researcher details including:
  - Name and degrees
  - Title and programs
  - Research interests
  - Education history
  - Publications
  - Contact information
  - Grants information

### 3.4. Storage Management (Handled in main.py)
- Organizes data in multiple formats:
  - Raw HTML files (`data/raw_html/`)
  - Intermediate Markdown files (`data/markdown/`)
  - Processed JSON data (`data/processed/`)
- Generates summary statistics across all researchers

### 3.5. Main Orchestrator (`main.py`)
- Provides command-line interface
- Coordinates the entire pipeline
- Handles error reporting and logging
- Generates summary statistics

## 4. Data Flow

The complete data flow through the system:

1. **URL Extraction**: Read researcher URLs and departments from Excel file
2. **Web Crawling**: Fetch HTML content with rate limiting
3. **Markdown Conversion**: Convert HTML to more processable Markdown
4. **Data Extraction**: Parse Markdown to extract structured information
5. **Validation**: Verify data against JSON schema (optional)
6. **Storage**: Save processed data to JSON files
7. **Summary Generation**: Create analytics across all researchers

## 5. Key Features

- **Rate Limiting**: Ethical crawling with randomized delays
- **Fault Tolerance**: Error handling and recovery
- **Structured Output**: Consistent JSON format for all researchers
- **Multi-format Storage**: Raw, intermediate, and processed data preserved
- **Extensible Architecture**: Modular design for easy enhancement

## 6. File Structure

```
motiff-web-scraper/
│
├── data/                  # Data storage directory
│   ├── raw_html/          # Original HTML files
│   ├── markdown/          # Converted markdown files
│   └── processed/         # Structured JSON data
│
├── schemas/               # JSON schemas
│   └── researcher.json    # Schema for researcher data
│
├── src/                   # Source code modules
│   ├── crawl.py           # Web crawler implementation
│   ├── parse.py           # Markdown parser
│   ├── url_reader.py      # Excel file processor
│   └── validate.py        # Schema validation
│
├── docs/                  # Documentation files
│
├── main.py                # Main script and orchestration
├── requirements.txt       # Python dependencies
└── researcher_links.xlsx  # Input data with URLs
```

## 7. Technologies Used

- **Python 3.6+**: Core programming language
- **crawl4ai**: Web crawling with JavaScript rendering support
- **pandas**: Excel file processing
- **asyncio**: Asynchronous I/O operations
- **aiofiles**: Asynchronous file operations
- **jsonschema**: JSON validation
- **Regular expressions**: Pattern matching for data extraction