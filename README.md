# Moffitt Cancer Center Researcher Data Scraper

> Automatically collect and structure researcher information from Moffitt Cancer Center for AI-powered research assistance

This project scrapes researcher profiles from the Moffitt Cancer Center website and transforms them into structured data for use in AI systems (specifically, Retrieval-Augmented Generation or RAG). It extracts comprehensive researcher information including biographies, research interests, publications, education, and grants.

**Status**: ✅ Scraping completed with all 127 researcher profiles processed

## Quick Links

**👋 New to Web Scraping?**
- [Introduction for Beginners](docs/0_introduction_for_beginners.md) - Start here if you're new to web scraping (10 min read)
- [Getting Started Guide](docs/getting_started_guide.md) - Step-by-step installation and first run (20-30 min)
- [Glossary](docs/glossary.md) - Understand all the technical terms used in this project
- [FAQ](docs/FAQ.md) - Quick answers to common questions

**📖 Using the Scraper**
- [Installation & Usage](#installation) - Quick setup and command reference
- [Data Model](#data-model) - What data is collected and how it's structured
- [Output Format](#output-format) - Understanding the three file formats (HTML, Markdown, JSON)

**🔧 Technical Documentation**
- [System Overview](docs/1_system_overview.md) - Architecture and design
- [Crawling Mechanism](docs/2_crawling_mechanism.md) - How data is fetched from the web
- [Data Extraction](docs/3_data_extraction.md) - How HTML is parsed into structured data
- [Data Storage](docs/4_data_storage.md) - File formats and organization
- [Main Script](docs/5_usage_and_main_script.md) - Pipeline orchestration

## Recent Improvements (November 2025)

This scraper has been recently enhanced with significant improvements:

- **🎯 Enhanced Publication Parsing**: Now correctly separates authors, titles, and journal names using intelligent period detection
- **📊 Structured Grant Data**: Extracts grant titles, award numbers, sponsors, and investigator roles
- **🧪 Clinical Trials Integration**: Captures participating clinical trials with trial ID, title, condition, intervention, and status
- **🔬 Lab Pages & Scholar Profiles**: Extracts personal lab page URLs and Google Scholar profile links
- **🔤 Data Normalization**: All program names, departments, and researcher names are lowercase for consistency
- **🧹 Cleaner Program Names**: Automatically removes redundant "Program" suffixes
- **📚 Comprehensive Documentation**: New beginner-friendly guides and technical references

See the [CHANGELOG](docs/changelog.md) for detailed information about recent changes.

## Project Structure

```
motiff-web-scraper/
├── data/
│   ├── raw_html/      # Original HTML snapshots
│   ├── markdown/      # Converted markdown files
│   └── processed/     # Final JSON data
├── src/
│   ├── crawl.py       # URL fetching with rate limiting
│   ├── parse.py       # HTML → Markdown → JSON conversion
│   ├── url_reader.py  # Extracts URLs from Excel file
│   └── validate.py    # Schema validation
├── schemas/
│   └── researcher.json  # JSON schema for validation
├── main.py            # Main pipeline script
└── researcher_links.xlsx  # Excel file with researcher URLs
```

## Requirements

- Python 3.8+
- Required packages:
  - crawl4ai
  - pandas
  - openpyxl
  - aiofiles

## Installation

1. Create a virtual environment (recommended):
   ```
   python -m venv crawl4ai-env
   source crawl4ai-env/bin/activate  # Linux/Mac
   crawl4ai-env\Scripts\activate      # Windows
   ```

2. Install required packages:
   ```
   pip install crawl4ai pandas openpyxl aiofiles
   ```

## Usage

### Process all researchers from Excel file

```
python main.py
```

### Process a single researcher URL

```
python main.py --url https://www.moffitt.org/research-science/researchers/michael-vogelbaum/
```

### Process only a limited number of researchers

```
python main.py --limit 5
```

### Specify a custom Excel file

```
python main.py --excel custom_links.xlsx
```

## Data Model

The scraper extracts the following information from each researcher profile:

- Basic Information
  - Name
  - Degrees (MD, PhD, etc.)
  - Title/Position
  - Primary Program
  - Research Program
  - Department

- Research Information
  - Overview/Biography
  - Research Interests
  - Associations
  - Grants

- Education & Training
  - Degrees
  - Institutions
  - Specialties

- Publications
  - Titles
  - Authors
  - Journals
  - Years
  - PubMed IDs

- Additional Information
  - Photo URL
  - Contact Information
  - Profile URL
  - Lab Page URL
  - Google Scholar Profile
  - Participating Clinical Trials

## Output Format

Data is stored in **three formats** for maximum flexibility:

1. **Raw HTML** (`data/raw_html/`) - The original HTML content from the website (for archival and re-parsing)
2. **Markdown** (`data/markdown/`) - Human-readable converted content (for easy review and text search)
3. **JSON** (`data/processed/`) - Structured data ready for AI systems and databases

### Why Three Formats?

Each format serves a specific purpose:
- **HTML**: Preserves the original source in case we need to re-parse with improved logic
- **Markdown**: Easy to read and edit by humans, useful for quality control
- **JSON**: Machine-readable structured data perfect for RAG systems, databases, and analysis

### JSON Structure

All field names use lowercase for consistency. Here's the structure:

```json
{
  "researcher_id": "unique-identifier",
  "researcher_name": "researcher full name",
  "degrees": ["md", "phd"],
  "title": "professional title",
  "primary_program": "cancer biology",
  "research_program": "immunology, drug discovery",
  "department": "thoracic oncology",
  "overview": "Biography text in markdown format...",
  "research_interests": ["interest 1", "interest 2"],
  "associations": ["association 1", "association 2"],
  "education": [
    {
      "type": "Graduate",
      "institution": "University Name",
      "degree": "Ph.D.",
      "field": "Molecular Biology"
    }
  ],
  "publications": [
    {
      "authors": "Smith J, Doe A, Johnson B",
      "title": "Novel approaches to cancer treatment",
      "journal": "Nature Medicine",
      "journal_details": "15(3):234-245",
      "year": "2024",
      "pubmed_id": "12345678",
      "publication_date": "2024 Mar"
    }
  ],
  "grants": [
    {
      "title": "Mechanisms of immune evasion in melanoma",
      "award_number": "R01CA123456",
      "sponsor": "National Cancer Institute",
      "investigators": [
        {
          "name": "Smith, J.",
          "role": "Principal Investigator"
        },
        {
          "name": "Doe, A.",
          "role": "Co-Investigator"
        }
      ],
      "description": "Full grant description..."
    }
  ],
  "contact": {
    "contact_url": "https://www.moffitt.org/contact/..."
  },
  "photo_url": "https://www.moffitt.org/media/...",
  "profile_url": "https://www.moffitt.org/research-science/researchers/...",
  "lab_page_url": "https://lab.moffitt.org/researcher/",
  "google_scholar_url": "https://scholar.google.com/citations?user=...",
  "participating_trials": [
    {
      "trial_id": "23320",
      "trial_url": "https://www.moffitt.org/clinical-trials-and-studies/clinical-trial-23320/",
      "title": "Phase 2 Study of Novel Treatment Approach",
      "condition": "Malignant Hematology",
      "intervention": "Drug X (); Drug Y ()",
      "status": "Open"
    }
  ],
  "content_hash": "sha256_hash_for_change_detection",
  "last_updated": "2025-11-15T10:30:00"
}
```

**Note**: Recent improvements (Nov 2025) added:
- Structured extraction for publications (separate authors, title, journal)
- Structured grant data (title, award number, sponsor, investigators)
- Lab page URLs, Google Scholar profiles, and participating clinical trials

See [Data Extraction documentation](docs/3_data_extraction.md) for technical details.

## Ethical Considerations

This scraper:
- Implements rate limiting to avoid overloading the server
- Respects robots.txt
- Only extracts publicly available information
- Is intended for research and educational purposes only
