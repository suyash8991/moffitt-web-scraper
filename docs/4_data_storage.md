# Moffitt Cancer Center Web Scraper: Data Storage and File Structure

## 1. Data Storage Overview

The Moffitt Cancer Center Web Scraper implements a multi-level storage approach that preserves data in three different formats at various stages of processing. This design enables easier debugging, data validation, and provides flexibility for future enhancements.

## 2. Storage Directory Structure

```
data/
├── raw_html/          # Original HTML files from web crawling
│   ├── ahmad-tarhini.html
│   ├── alberto-chiappori.html
│   └── ...
│
├── markdown/          # Converted markdown files
│   ├── ahmad-tarhini.md
│   ├── alberto-chiappori.md
│   └── ...
│
└── processed/         # Structured JSON data
    ├── ahmad-tarhini.json
    ├── alberto-chiappori.json
    ├── ...
    └── summary.json   # Generated summary statistics
```

This structure is initialized in the `MoffittResearcherScraper` class constructor:

```python
# Set up output directories
self.output_dirs = {
    "raw_html": os.path.join(output_base_dir, "raw_html"),
    "markdown": os.path.join(output_base_dir, "markdown"),
    "processed": os.path.join(output_base_dir, "processed")
}

# Create output directories if they don't exist
for dir_path in self.output_dirs.values():
    os.makedirs(dir_path, exist_ok=True)
```

## 3. Storage Formats

### 3.1 Raw HTML Storage

The first stage of storage preserves the original HTML content fetched from the website:

- **Location**: `data/raw_html/*.html`
- **Format**: Raw HTML as retrieved from the web server
- **Naming**: Based on the last segment of the URL path (typically researcher's name)
- **Purpose**: Preservation of original content for debugging and reprocessing

The raw HTML is saved in the `ResearcherCrawler` class:

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

### 3.2 Markdown Storage

The second stage converts HTML to Markdown format for easier text processing:

- **Location**: `data/markdown/*.md`
- **Format**: Markdown text converted from HTML by crawl4ai
- **Naming**: Based on researcher name extracted from URL
- **Purpose**: Intermediate format for easier text processing and readability

The markdown is saved in the `process_researcher` method of `MoffittResearcherScraper`:

```python
# Step 2: Save markdown to file
markdown_filename = os.path.join(self.output_dirs["markdown"], f"{researcher_name}.md")
with open(markdown_filename, 'w', encoding='utf-8') as f:
    f.write(crawl_result['markdown'])
logger.info(f"Saved markdown to {markdown_filename}")
```

### 3.3 Processed JSON Storage

The final stage saves structured data in JSON format:

- **Location**: `data/processed/*.json`
- **Format**: Structured JSON data with consistent schema
- **Naming**: Based on researcher name extracted from URL
- **Purpose**: Machine-readable data for analysis and integration

The JSON is saved in the `process_researcher` method:

```python
# Step 4: Save structured data to JSON
json_filename = os.path.join(self.output_dirs["processed"], f"{researcher_name}.json")
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(researcher_data, f, indent=2)
logger.info(f"Saved structured data to {json_filename}")
```

### 3.4 Summary JSON

Additionally, a summary file is generated to provide aggregate statistics:

- **Location**: `data/processed/summary.json`
- **Format**: JSON with summary statistics
- **Content**: Counts of researchers by program, department, and top research interests
- **Purpose**: Quick overview of the entire dataset

The summary is generated in the `main` function:

```python
# Generate summary
summary = scraper.generate_summary(researchers)

# Save summary to file
summary_filename = os.path.join("data", "processed", "summary.json")
with open(summary_filename, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2)

logger.info(f"Processed {summary['count']} researchers. Summary saved to {summary_filename}")
```

## 4. JSON Data Schema

The processed JSON data follows a consistent schema defined in `schemas/researcher.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Moffitt Researcher Profile",
  "description": "Schema for a Moffitt Cancer Center researcher profile",
  "type": "object",
  "required": [
    "researcher_id",
    "name",
    "researcher_name",
    "program",
    "department",
    "profile_url",
    "content_hash",
    "last_updated"
  ],
  "properties": {
    "researcher_id": {
      "type": "string",
      "description": "Unique identifier for the researcher"
    },
    "name": {
      "type": "string",
      "description": "Full name of the researcher"
    },
    "researcher_name": {
      "type": "string",
      "description": "Name of the researcher"
    },
    "title": {
      "type": "string",
      "description": "Professional title of the researcher"
    },
    "program": {
      "type": "string",
      "description": "Research program the researcher belongs to"
    },
    "department": {
      "type": "string",
      "description": "Department the researcher belongs to"
    },
    "biography": {
      "type": "string",
      "description": "Biography/overview of the researcher in markdown format"
    },
    "research_interests": {
      "type": "array",
      "description": "List of research interests",
      "items": {
        "type": "string"
      }
    },
    "publications": {
      "type": "array",
      "description": "List of publications",
      "items": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "description": "Publication title"
          },
          "authors": {
            "type": "string",
            "description": "List of authors"
          },
          "journal": {
            "type": "string",
            "description": "Journal name"
          },
          "year": {
            "type": "string",
            "description": "Publication year"
          },
          "url": {
            "type": "string",
            "description": "URL to the publication, if available"
          }
        },
        "required": ["title"]
      }
    },
    "contact": {
      "type": "object",
      "description": "Contact information for the researcher",
      "properties": {
        "email": {
          "type": "string",
          "format": "email",
          "description": "Email address"
        },
        "phone": {
          "type": "string",
          "description": "Phone number"
        },
        "location": {
          "type": "string",
          "description": "Office location"
        }
      }
    },
    "profile_url": {
      "type": "string",
      "format": "uri",
      "description": "URL of the original researcher profile"
    },
    "content_hash": {
      "type": "string",
      "description": "Hash of the content for change detection"
    },
    "last_updated": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp of when the data was last updated"
    }
  }
}
```

## 5. Schema Validation

The system includes schema validation capability in the `src/validate.py` module:

```python
def validate_researcher(data, schema=None):
    """
    Validate a researcher profile against the schema.

    Args:
        data (dict): The researcher profile data
        schema (dict, optional): The schema to validate against.
                              If None, the default schema is loaded.

    Returns:
        tuple: (is_valid, errors) where is_valid is a boolean and errors is a list
    """
    if schema is None:
        schema_path = os.path.join('schemas', 'researcher.json')
        schema = load_schema(schema_path)

    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, []
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)
```

This validation can be used to ensure that all generated JSON data conforms to the expected schema.

## 6. Department Information from Excel

A key feature of the storage process is incorporating department information from the Excel file. The `url_reader.py` module extracts this information and passes it to the main pipeline:

```python
# Read URLs and department info from Excel file
urls_data = read_urls_from_excel(args.excel)
```

In the `process_researcher` method, the department information is added to the researcher data:

```python
# Add department from Excel if available
if department:
    researcher_data['department'] = department
```

Example Excel file structure:
| Program | Department | Researcher Name | Profile URL |
|---------|------------|----------------|-------------|
| Molecular Medicine Program | Immunology | Ahmad Tarhini | https://www.moffitt.org/research-science/researchers/ahmad-tarhini/ |
| Molecular Medicine Program | Tumor Microenvironment and Metastasis | Alberto Chiappori | https://www.moffitt.org/research-science/researchers/alberto-chiappori/ |
| Immuno-Oncology | Immunology | Aleksandr Lazaryan | https://www.moffitt.org/research-science/researchers/aleksandr-lazaryan/ |

## 7. Summary Generation

The system generates a summary of all processed researchers to provide aggregate statistics:

```python
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
```

## 8. Content Hash Generation

For change detection and caching purposes, the system generates a content hash for each researcher profile:

```python
def generate_content_hash(content):
    """
    Generate a hash of the content for change detection.

    Args:
        content (str): The content to hash

    Returns:
        str: The hash of the content
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()
```

This hash is included in the researcher JSON data:

```python
# Generate content hash
content_str = json.dumps(researcher, sort_keys=True)
researcher["content_hash"] = hashlib.sha256(content_str.encode('utf-8')).hexdigest()
```

## 9. Data Storage Flow Diagram

```
┌──────────────┐     ┌─────────────────┐     ┌─────────────────┐
│              │     │                 │     │                 │
│ Crawler      │────▶│ Raw HTML        │     │ Parser          │
│ (fetch)      │     │ Storage         │     │ (extract)       │
│              │     │                 │     │                 │
└──────────────┘     └─────────────────┘     └─────────────────┘
                           │                         ▲
                           │                         │
                           ▼                         │
                     ┌─────────────────┐     ┌─────────────────┐
                     │                 │     │                 │
                     │ Markdown        │────▶│ JSON            │
                     │ Storage         │     │ Storage         │
                     │                 │     │                 │
                     └─────────────────┘     └─────────────────┘
                                                     │
                                                     │
                                                     ▼
                                             ┌─────────────────┐
                                             │                 │
                                             │ Summary         │
                                             │ Generation      │
                                             │                 │
                                             └─────────────────┘
```

## 10. Benefits of the Multi-level Storage Approach

1. **Data Preservation**: Original content is preserved for future reprocessing
2. **Debugging Support**: Easier to diagnose issues at different processing stages
3. **Format Flexibility**: Different formats for different purposes (raw, readable, structured)
4. **Incremental Processing**: Can restart processing from intermediate stages
5. **Change Detection**: Content hashes enable detection of changes over time
6. **Summary Statistics**: Aggregate data provides overview of the complete dataset