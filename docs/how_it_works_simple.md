# How It Works: A Visual Walkthrough

> A beginner-friendly explanation of how the Moffitt scraper transforms web pages into structured data

**Reading time**: 15 minutes

## The Big Picture

The scraper performs a three-stage transformation:

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Web Page   │  →   │   Markdown   │  →   │     JSON     │
│    (HTML)    │      │    (Text)    │      │  (Database)  │
└──────────────┘      └──────────────┘      └──────────────┘
  Unstructured         Semi-structured        Fully structured
```

**Why three stages?** Each format serves a different purpose:
- **HTML**: What the website sends (complex, hard to parse)
- **Markdown**: Human-readable middle format (easy to review)
- **JSON**: Machine-readable final format (ready for AI systems)

## Stage-by-Stage Walkthrough

### Stage 0: Preparation

**What happens**: The system reads a list of researcher URLs from an Excel file.

**Input**: `researcher_links.xlsx`
```
Name                   | URL
-----------------------|--------------------------------------------
Michael Vogelbaum      | https://www.moffitt.org/research-science/...
Anna Giuliano          | https://www.moffitt.org/research-science/...
```

**Code responsible**: `src/url_reader.py`

**Output**: A list of URLs to process

---

### Stage 1: Crawling (Fetching Web Pages)

**What happens**: The system visits each researcher's profile page and downloads the HTML.

```
┌─────────────┐
│  Internet   │
│   (Moffitt  │
│   Website)  │
└─────┬───────┘
      │ HTTP Request
      │ "Give me this page please"
      ↓
┌─────────────────────────────┐
│  Crawl4AI                   │
│  (Visits page like a        │
│   browser, gets HTML)       │
└─────────────┬───────────────┘
              │
              ↓
        Saves to file
              │
              ↓
┌─────────────────────────────┐
│  data/raw_html/             │
│  researcher-name.html       │
└─────────────────────────────┘
```

**Important details**:
- **Rate limiting**: Waits 2-5 seconds between requests (to be polite to the server)
- **Error handling**: Retries if the connection fails
- **Caching**: Checks if we already have the HTML before downloading again

**Code responsible**: `src/crawl.py`

**Example output**: `data/raw_html/michael-vogelbaum.html`

---

### Stage 2: Markdown Conversion

**What happens**: The messy HTML is converted into clean, readable Markdown.

**Input**: HTML with navigation bars, ads, styling, scripts
```html
<div class="header">
  <nav>...</nav>
</div>
<div class="content">
  <h1>Dr. Michael Vogelbaum, MD, PhD</h1>
  <p class="bio">Dr. Vogelbaum is a neurosurgeon...</p>
</div>
<footer>...</footer>
```

**Process**:
```
HTML Parser
    ↓
Remove: navigation, ads, scripts, styling
    ↓
Keep: headings, paragraphs, lists, links
    ↓
Convert to Markdown format
```

**Output**: Clean Markdown
```markdown
# Dr. Michael Vogelbaum, MD, PhD

**Title:** Chair, Department of Neuro-Oncology

**Program:** Cancer Biology

## Overview

Dr. Vogelbaum is a neurosurgeon specializing in...

## Research Interests

- Brain tumor biology
- Novel therapeutic approaches
```

**Code responsible**: `src/parse.py` (uses Crawl4AI's markdown converter)

**Example output**: `data/markdown/michael-vogelbaum.md`

---

### Stage 3: Data Extraction (The Smart Part)

**What happens**: The scraper reads the Markdown and extracts specific pieces of information into structured fields.

This is where the "intelligence" of the scraper lives. It knows:
- Where to find the researcher's name (usually first heading)
- How to parse degrees (MD, PhD, etc.)
- How to separate publication authors from titles
- How to extract grant information

#### Example: Parsing a Publication

**Input** (from Markdown):
```
Smith J, Doe A, Johnson B. Novel approaches to cancer treatment. Nature Medicine 15(3):234-245. 2024 Mar. PubMed
```

**Parsing logic**:
```
Step 1: Find periods (.) that separate components
        ↓
Positions: [24, 69, 96]
        ↓
Step 2: Extract components
        ↓
Before 1st period → Authors: "Smith J, Doe A, Johnson B"
Between 1st & 2nd → Title: "Novel approaches to cancer treatment"
After 2nd period  → Journal: "Nature Medicine 15(3):234-245"
        ↓
Step 3: Parse additional details
        ↓
Extract year: "2024"
Extract PubMed ID: (link)
```

**Output** (JSON):
```json
{
  "authors": "Smith J, Doe A, Johnson B",
  "title": "Novel approaches to cancer treatment",
  "journal": "Nature Medicine",
  "journal_details": "15(3):234-245",
  "year": "2024",
  "publication_date": "2024 Mar",
  "pubmed_id": "12345678"
}
```

#### Example: Parsing a Grant

**Input** (from Markdown):
```
Title: Mechanisms of immune evasion in melanoma
Award Number: R01CA123456
Sponsor: National Cancer Institute
Smith, J. (Principal Investigator)
Doe, A. (Co-Investigator)
```

**Parsing logic**:
```
Step 1: Look for labeled fields
        ↓
"Title:" → "Mechanisms of immune evasion in melanoma"
"Award Number:" → "R01CA123456"
"Sponsor:" → "National Cancer Institute"
        ↓
Step 2: Parse investigators (name + role pattern)
        ↓
Regex: (\w+,\s*\w\.)\s*\((.*?)\)
        ↓
Match 1: "Smith, J." + "Principal Investigator"
Match 2: "Doe, A." + "Co-Investigator"
```

**Output** (JSON):
```json
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
  ]
}
```

**Code responsible**: `src/parse.py` (functions: `extract_publications()`, `extract_grants()`)

---

### Stage 4: Data Normalization

**What happens**: Clean up and standardize the extracted data.

**Normalization steps**:
1. **Lowercase conversion**: All program names, departments, researcher names → lowercase
2. **Remove redundancy**: Strip " Program" suffix from program names
3. **Trim whitespace**: Remove extra spaces
4. **Validate**: Check that required fields are present

**Example**:
```
Before normalization:
  primary_program: "Immunology Program"
  department: "Thoracic Oncology"
  researcher_name: "John Smith"

After normalization:
  primary_program: "immunology"
  department: "thoracic oncology"
  researcher_name: "john smith"
```

**Why?** Consistent formatting enables accurate searching and grouping. Without this, "Immunology" and "immunology" would be treated as different categories.

---

### Stage 5: Save to JSON

**What happens**: The structured data is saved as a JSON file.

**Output**: `data/processed/michael-vogelbaum.json`

```json
{
  "researcher_id": "michael-vogelbaum",
  "researcher_name": "michael vogelbaum",
  "degrees": ["md", "phd"],
  "title": "chair, department of neuro-oncology",
  "primary_program": "cancer biology",
  "department": "neuro-oncology",
  "overview": "Dr. Vogelbaum is a neurosurgeon...",
  "publications": [...],
  "grants": [...],
  "profile_url": "https://...",
  "last_updated": "2025-11-15T10:30:00"
}
```

Additionally, a summary file is created: `data/processed/summary.json`

This contains basic info about all researchers in one file for quick lookups.

---

## The Complete Flow

Here's what happens when you run `python main.py`:

```
1. Read researcher_links.xlsx
   ↓
2. For each researcher:
   ├─ Check if we need to download (compare content hash)
   ├─ If yes: Crawl → Save HTML
   ├─ Convert HTML → Markdown
   ├─ Extract data → Parse fields
   ├─ Normalize → Clean up data
   └─ Save JSON
   ↓
3. Create summary.json (all researchers)
   ↓
4. Done!
```

**Progress tracking**: The script shows you what it's doing:
```
Processing researcher 1/127: Michael Vogelbaum
  ✓ Downloaded HTML (2.3s)
  ✓ Converted to Markdown
  ✓ Extracted 47 publications, 12 grants
  ✓ Saved JSON

Processing researcher 2/127: Anna Giuliano
  → Skipped (content unchanged)
...
```

---

## Why This Design?

### Three-Format Storage

**Question**: Why save HTML, Markdown, AND JSON?

**Answer**: Each serves a purpose:

1. **HTML** = Archive
   - If we improve the parsing logic, we can re-parse without re-downloading
   - Preserves the original source
   - Useful for debugging

2. **Markdown** = Human review
   - Easy to read and verify quality
   - Can be used for full-text search
   - Good for manual corrections

3. **JSON** = AI consumption
   - Structured data ready for databases
   - Perfect for RAG systems
   - Queryable by specific fields

### Rate Limiting

**Question**: Why wait 2-5 seconds between requests?

**Answer**: To be respectful to the Moffitt website:
- Prevents overloading their servers
- Avoids getting our IP blocked
- Mimics human browsing behavior
- Ethical web scraping practice

### Content Hashing

**Question**: What's the "content_hash" field?

**Answer**: A fingerprint of the page content. If we re-run the scraper and the hash hasn't changed, we know the page hasn't been updated and can skip re-processing. This saves time and bandwidth.

---

## Real-World Example: Complete Process

Let's follow one researcher through the entire pipeline:

### Input
Excel file contains: `https://www.moffitt.org/research-science/researchers/anna-giuliano/`

### Step 1: Download
```
GET https://www.moffitt.org/research-science/researchers/anna-giuliano/
↓
Save: data/raw_html/anna-giuliano.html (87 KB)
```

### Step 2: Convert to Markdown
```
Parse HTML → Extract main content → Convert formatting
↓
Save: data/markdown/anna-giuliano.md (12 KB)
```

### Step 3: Extract Data
```
Parse markdown for:
- Name: "Anna R. Giuliano"
- Degrees: ["PhD"]
- Program: "Cancer Epidemiology"
- 143 publications
- 8 grants
↓
Create structured object
```

### Step 4: Normalize
```
Apply lowercase:
- "Anna R. Giuliano" → "anna r. giuliano"
- "Cancer Epidemiology Program" → "cancer epidemiology"
```

### Step 5: Save
```
Write: data/processed/anna-giuliano.json (234 KB)
Update: data/processed/summary.json
```

### Total time: ~5 seconds
(2s download + 3s processing)

---

## What Makes This Scraper "Smart"?

1. **Adaptive parsing**: Handles variations in how information is formatted
2. **Error recovery**: Continues even if one field fails to extract
3. **Incremental updates**: Only re-downloads changed pages
4. **Structured output**: Transforms unstructured HTML into queryable data
5. **Quality preservation**: Three-format storage means no data is lost

---

## Next Steps

Now that you understand how it works:

- **To use it**: See the [Getting Started Guide](getting_started_guide.md)
- **To modify it**: See [Design Decisions](design_decisions.md)
- **To understand the data**: See [Understanding the Data](understanding_the_data.md)
- **For technical details**: See the numbered documentation (1-5)

## Questions?

Check the [FAQ](FAQ.md) or look up terms in the [Glossary](glossary.md).
