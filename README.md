# Moffitt Cancer Center Researcher Data Scraper

This project scrapes researcher profiles from the Moffitt Cancer Center website and structures the data for use in a Retrieval-Augmented Generation (RAG) system. It extracts researcher information including biographies, research interests, publications, education, and grants.

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

## Output Format

Data is stored in three formats:
1. Raw HTML: The original HTML content from the website
2. Markdown: Converted content in markdown format
3. JSON: Structured data extracted from the markdown

The JSON format follows this structure:

```json
{
  "researcher_id": "unique_identifier",
  "name": "Researcher Full Name",
  "degrees": ["MD", "PhD"],
  "title": "Professional Title",
  "primary_program": "Research Program",
  "research_program": "Program Affiliation",
  "overview": "Biography text in markdown",
  "research_interests": ["Interest 1", "Interest 2"],
  "associations": ["Association 1", "Association 2"],
  "education": [
    {
      "type": "Graduate",
      "institution": "University Name",
      "degree": "Ph.D.",
      "field": "Field of Study"
    }
  ],
  "publications": [
    {
      "title": "Publication Title",
      "authors": "Authors list",
      "journal": "Journal name",
      "year": "Publication year",
      "pubmed_id": "PubMed ID"
    }
  ],
  "grants": [
    {
      "description": "Grant description",
      "id": "Grant ID",
      "source": "Funding source",
      "period": "Funding period"
    }
  ],
  "contact": {
    "contact_url": "Contact form URL"
  },
  "photo_url": "URL to profile photo",
  "profile_url": "Original profile URL",
  "content_hash": "Hash for change detection",
  "last_updated": "ISO timestamp"
}
```

## Ethical Considerations

This scraper:
- Implements rate limiting to avoid overloading the server
- Respects robots.txt
- Only extracts publicly available information
- Is intended for research and educational purposes only

## Next Steps

Phase 2 of this project will involve:
1. Building a vector database using the extracted data
2. Creating embeddings for semantic search
3. Implementing an Agentic RAG system for natural language queries