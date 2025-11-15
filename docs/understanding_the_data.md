# Understanding the Data

> A field-by-field guide to the scraped researcher data

This guide explains every field in the JSON output, what it contains, how it's used, and common questions about the data.

**Reading time**: 20 minutes

---

## Table of Contents

1. [File Structure](#file-structure)
2. [Basic Information Fields](#basic-information-fields)
3. [Academic Fields](#academic-fields)
4. [Research Fields](#research-fields)
5. [Publications](#publications)
6. [Grants](#grants)
7. [Metadata Fields](#metadata-fields)
8. [Summary File](#summary-file)
9. [Common Use Cases](#common-use-cases)
10. [Data Quality Notes](#data-quality-notes)

---

## File Structure

Each researcher has three files:

```
data/
├── raw_html/
│   └── researcher-name.html          (Original HTML)
├── markdown/
│   └── researcher-name.md            (Human-readable)
└── processed/
    ├── researcher-name.json          (Structured data)
    └── summary.json                  (All researchers, basic info only)
```

The JSON file contains the complete structured data. Let's examine each field.

---

## Basic Information Fields

### `researcher_id`

**Type**: `string`

**Example**: `"michael-vogelbaum"`

**Description**: Unique identifier for the researcher, derived from their URL slug.

**Format**: Lowercase, words separated by hyphens

**Use cases**:
- Database primary key
- Linking related records
- Generating file paths

**Notes**:
- Guaranteed to be unique across all researchers
- Doesn't change even if the researcher's name changes
- Safe for use in file names and URLs

---

### `researcher_name`

**Type**: `string`

**Example**: `"michael vogelbaum"`

**Description**: Full name of the researcher in lowercase.

**Format**: Lowercase, spaces between names

**Changes in Nov 2025**: Now lowercase for consistency (previously title case)

**Use cases**:
- Display to users (apply title case when displaying)
- Searching by name
- Sorting alphabetically

**Notes**:
- Does NOT include degrees (MD, PhD, etc.) - those are in a separate field
- Middle names/initials included when present
- Lowercased for data consistency

---

### `degrees`

**Type**: `array of strings`

**Example**: `["md", "phd"]`

**Description**: Academic and professional degrees held by the researcher.

**Common values**:
- `"md"` - Medical Doctor
- `"phd"` - Doctor of Philosophy
- `"mbbs"` - Bachelor of Medicine, Bachelor of Surgery
- `"mph"` - Master of Public Health
- `"do"` - Doctor of Osteopathic Medicine
- `"msph"` - Master of Science in Public Health
- `"ms"` - Master of Science

**Use cases**:
- Filter researchers by qualification (e.g., "all MDs")
- Display credentials after name: "Dr. Smith, MD, PhD"
- Analyze degree combinations

**Notes**:
- Always lowercase
- Order reflects how they appear on the profile
- Empty array `[]` if no degrees listed

---

### `title`

**Type**: `string`

**Example**: `"chair, department of neuro-oncology"`

**Description**: Professional title and position at Moffitt Cancer Center.

**Format**: Lowercase, may include multiple roles separated by commas or semicolons

**Use cases**:
- Display researcher's role
- Filter by position (e.g., "department chair")
- Understand institutional hierarchy

**Examples**:
```
"senior member"
"associate member"
"chair, department of neuro-oncology"
"professor, department of oncology"
```

**Notes**:
- Reflects current position (as of last scrape)
- May be empty if not listed on profile
- Lowercased in Nov 2025 update

---

## Academic Fields

### `primary_program`

**Type**: `string`

**Example**: `"cancer biology"`

**Description**: The main research program the researcher is affiliated with.

**Common values**:
- `"cancer biology"`
- `"immunology"`
- `"cancer epidemiology"`
- `"drug discovery"`
- `"cancer physiology"`
- `"quantitative science"`

**Changes in Nov 2025**:
- Lowercased for consistency
- Removed redundant " Program" suffix

**Use cases**:
- Group researchers by program
- Filter by research area
- Analyze program distribution

**Notes**:
- Single value (main affiliation)
- If researcher has multiple programs, see `research_program`

---

### `research_program`

**Type**: `string` (comma-separated list)

**Example**: `"immunology, drug discovery"`

**Description**: All research programs the researcher is affiliated with.

**Format**: Lowercase, comma-separated if multiple

**Use cases**:
- Identify cross-program researchers
- Map collaboration networks
- Filter by multiple programs

**Example values**:
```
"immunology"
"cancer biology, drug discovery"
"cancer epidemiology, cancer prevention"
```

**Changes in Nov 2025**:
- Lowercased
- Removed " Program" suffix from each program

**Notes**:
- May contain same value as `primary_program`
- To split into list: `programs = research_program.split(', ')`

---

### `department`

**Type**: `string`

**Example**: `"thoracic oncology"`

**Description**: The academic/clinical department the researcher belongs to.

**Common values**:
- `"thoracic oncology"`
- `"neuro-oncology"`
- `"gastrointestinal oncology"`
- `"malignant hematology"`
- `"cancer epidemiology"`

**Changes in Nov 2025**: Lowercased for consistency

**Use cases**:
- Group by department
- Identify department heads (cross-reference with `title`)
- Analyze departmental structure

**Notes**:
- May be empty if not specified on profile
- Different from `research_program` (department is organizational, program is thematic)

---

## Research Fields

### `overview`

**Type**: `string` (markdown formatted)

**Example**:
```markdown
Dr. Vogelbaum is a neurosurgeon specializing in brain tumors...

His research focuses on:
- Novel drug delivery methods
- Clinical trial design
```

**Description**: Biography and research overview in markdown format.

**Format**: Markdown with headings, lists, paragraphs, etc.

**Use cases**:
- Display on researcher profile pages
- Full-text search for keywords
- RAG system context retrieval
- Summarization with AI

**Notes**:
- Preserves formatting (bullets, paragraphs)
- Length varies (100-1000+ words)
- May include links to publications or projects

---

### `research_interests`

**Type**: `array of strings`

**Example**:
```json
[
  "brain tumor biology",
  "novel therapeutic approaches",
  "clinical trial design"
]
```

**Description**: List of specific research interests or focus areas.

**Use cases**:
- Filter researchers by topic
- Find experts in specific areas
- Identify overlapping interests for collaboration

**Notes**:
- Extracted from "Research Interests" section
- Variable number of items (typically 3-10)
- May be empty array if not listed

---

### `associations`

**Type**: `array of strings`

**Example**:
```json
[
  "American Association of Neurological Surgeons",
  "Society for Neuro-Oncology"
]
```

**Description**: Professional associations, societies, and memberships.

**Use cases**:
- Identify professional networks
- Filter by association membership
- Analyze cross-institutional connections

**Notes**:
- May be empty if not listed on profile
- Includes both national and international organizations

---

## Publications

### `publications`

**Type**: `array of objects`

**Description**: List of academic publications authored or co-authored by the researcher.

**Structure** (updated Nov 2025):
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

### Field Breakdown

#### `authors`

**Type**: `string`

**Example**: `"Smith J, Doe A, Johnson B"`

**Description**: Comma-separated list of all authors.

**Format**: Last name followed by initials, separated by commas

**Notes**:
- Researcher's name is included somewhere in this list
- Order typically reflects contribution (first author = primary)

---

#### `title`

**Type**: `string`

**Example**: `"Novel approaches to cancer treatment"`

**Description**: Full title of the publication.

**Notes**:
- No ending period
- Capitalization as it appears in original citation

---

#### `journal`

**Type**: `string`

**Example**: `"Nature Medicine"`

**Description**: Name of the journal where published.

**Notes**:
- Cleaned to extract just the journal name
- Volume/issue info separated into `journal_details`

---

#### `journal_details`

**Type**: `string` (optional)

**Example**: `"15(3):234-245"`

**Description**: Volume, issue, and page numbers.

**Format**: Varies, common formats:
- `"15(3):234-245"` (volume 15, issue 3, pages 234-245)
- `"42:1234-1250"` (volume 42, pages 1234-1250)

**Notes**:
- May be missing if not in original citation
- Added in Nov 2025 update

---

#### `year`

**Type**: `string`

**Example**: `"2024"`

**Description**: Publication year.

**Notes**:
- 4-digit year
- String (not number) for consistency

---

#### `publication_date`

**Type**: `string` (optional)

**Example**: `"2024 Mar"`

**Description**: More specific publication date if available.

**Format**: Year followed by month abbreviation

**Notes**:
- Added in Nov 2025 update
- May include just year or year + month

---

#### `pubmed_id`

**Type**: `string` (optional)

**Example**: `"12345678"`

**Description**: PubMed identifier for the publication.

**Use cases**:
- Link to full publication: `https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/`
- Retrieve additional metadata from PubMed API
- Citation management

**Notes**:
- Only present if publication has a PubMed entry
- Extracted from links in the original profile

---

### Publication Use Cases

**Find all publications by a researcher**:
```python
researcher = json.load(open('michael-vogelbaum.json'))
for pub in researcher['publications']:
    print(f"{pub['year']}: {pub['title']}")
```

**Filter publications by year**:
```python
recent_pubs = [p for p in researcher['publications'] if int(p['year']) >= 2020]
```

**Count publications**:
```python
total_pubs = len(researcher['publications'])
```

---

## Grants

### `grants`

**Type**: `array of objects`

**Description**: List of research grants received by the researcher.

**Structure** (enhanced Nov 2025):
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
  ],
  "description": "Full grant description with all details..."
}
```

### Field Breakdown

#### `title`

**Type**: `string`

**Example**: `"Mechanisms of immune evasion in melanoma"`

**Description**: Official title of the research grant.

**Notes**:
- Added in Nov 2025 update
- Extracted from "Title:" prefix in grant description

---

#### `award_number`

**Type**: `string` (optional)

**Example**: `"R01CA123456"`

**Description**: Unique identifier for the grant award.

**Common prefixes**:
- `R01` - NIH Research Project Grant
- `P01` - NIH Program Project Grant
- `U01` - NIH Cooperative Agreement
- `K08` - Career Development Award

**Use cases**:
- Track funding over time
- Link publications to grants
- Identify grant type by prefix

**Notes**:
- Added in Nov 2025 update
- May be missing if award number is "N/A" or not listed

---

#### `sponsor`

**Type**: `string`

**Example**: `"National Cancer Institute"`

**Description**: Organization providing the funding.

**Common values**:
- `"National Cancer Institute"`
- `"National Institutes of Health"`
- `"Department of Defense"`
- `"American Cancer Society"`

**Use cases**:
- Filter researchers by funding source
- Analyze funding patterns
- Identify government vs. private funding

**Notes**:
- Added in Nov 2025 update
- Extracted from "Sponsor:" prefix

---

#### `investigators`

**Type**: `array of objects`

**Example**:
```json
[
  {
    "name": "Smith, J.",
    "role": "Principal Investigator"
  },
  {
    "name": "Doe, A.",
    "role": "Co-Investigator"
  }
]
```

**Description**: List of investigators on the grant with their roles.

**Roles**:
- `"Principal Investigator"` - Lead researcher
- `"Co-Investigator"` - Collaborating researcher
- `"Co-Principal Investigator"` - Co-lead

**Use cases**:
- Identify grant collaborations
- Map research networks
- Find grants where researcher is PI vs. Co-I

**Notes**:
- Added in Nov 2025 update
- May be empty if investigator info not listed

---

#### `description`

**Type**: `string`

**Example**: Full text including all the above fields plus any additional details

**Description**: Complete grant description as it appears on the profile.

**Notes**:
- Preserved for backwards compatibility
- Contains all structured fields plus any additional text
- Use structured fields (`title`, `award_number`, etc.) for queries

---

### Grant Use Cases

**Find all NIH-funded researchers**:
```python
nih_researchers = []
for researcher in all_researchers:
    for grant in researcher['grants']:
        if 'sponsor' in grant and 'National Institutes of Health' in grant['sponsor']:
            nih_researchers.append(researcher['researcher_name'])
```

**Find Principal Investigators**:
```python
pis = []
for grant in researcher['grants']:
    if 'investigators' in grant:
        for inv in grant['investigators']:
            if inv['role'] == 'Principal Investigator':
                pis.append(inv['name'])
```

---

## Metadata Fields

### `contact`

**Type**: `object`

**Example**:
```json
{
  "contact_url": "https://www.moffitt.org/contact/michael-vogelbaum/"
}
```

**Description**: Contact information for the researcher.

**Notes**:
- Currently only contains contact form URL
- Future versions may include email, phone, office location

---

### `photo_url`

**Type**: `string` (optional)

**Example**: `"https://www.moffitt.org/media/12345/vogelbaum.jpg"`

**Description**: URL to the researcher's profile photo.

**Use cases**:
- Display researcher photo on profile pages
- Download for local storage

**Notes**:
- May be empty if no photo on profile
- URL points to Moffitt's media server

---

### `profile_url`

**Type**: `string`

**Example**: `"https://www.moffitt.org/research-science/researchers/michael-vogelbaum/"`

**Description**: URL to the original researcher profile on Moffitt's website.

**Use cases**:
- Link back to source
- Verify data accuracy
- Check for updates

**Notes**:
- Always present
- Permanent URL (doesn't change)

---

### `content_hash`

**Type**: `string`

**Example**: `"a3f2b...c9d1e"` (SHA-256 hash)

**Description**: Hash of the page content for change detection.

**Use cases**:
- Detect if profile has been updated
- Skip re-processing unchanged profiles
- Track version history

**Notes**:
- Calculated from HTML content
- Changes if any content on the page changes

---

### `last_updated`

**Type**: `string` (ISO 8601 timestamp)

**Example**: `"2025-11-15T10:30:00"`

**Description**: When this data was last scraped.

**Format**: `YYYY-MM-DDTHH:MM:SS`

**Use cases**:
- Show data freshness to users
- Schedule re-scraping
- Audit data age

**Notes**:
- UTC timezone (no timezone offset)
- Updates every time the scraper runs and detects changes

---

## Summary File

Location: `data/processed/summary.json`

**Structure**:
```json
[
  {
    "researcher_id": "michael-vogelbaum",
    "researcher_name": "michael vogelbaum",
    "title": "chair, department of neuro-oncology",
    "primary_program": "cancer biology",
    "profile_url": "https://..."
  },
  ...
]
```

**Description**: Contains basic information for all researchers in a single file.

**Use cases**:
- Quick lookups without loading individual files
- Build researcher directory
- Search by name or program
- Generate navigation lists

**Notes**:
- Only includes basic fields (no publications, grants, etc.)
- Smaller file size for faster loading
- Updated when any researcher is processed

---

## Common Use Cases

### Use Case 1: Find Researchers by Topic

```python
import json
import glob

# Load all researcher files
researchers = []
for file in glob.glob('data/processed/*.json'):
    if file != 'data/processed/summary.json':
        researchers.append(json.load(open(file)))

# Find immunology researchers
immunology_experts = [
    r for r in researchers
    if r.get('primary_program') == 'immunology'
]

print(f"Found {len(immunology_experts)} immunology researchers")
```

---

### Use Case 2: Build a RAG System

```python
from chromadb import Client

# Initialize vector database
client = Client()
collection = client.create_collection("researchers")

# Add researcher data
for researcher in researchers:
    # Combine relevant text fields
    text = f"{researcher['researcher_name']} {researcher['overview']}"

    # Add to database
    collection.add(
        documents=[text],
        metadatas=[{
            "name": researcher['researcher_name'],
            "program": researcher['primary_program']
        }],
        ids=[researcher['researcher_id']]
    )

# Query
results = collection.query(
    query_texts=["melanoma immunotherapy"],
    n_results=5
)
```

---

### Use Case 3: Analyze Collaboration Networks

```python
import networkx as nx

# Build collaboration graph from grants
G = nx.Graph()

for researcher in researchers:
    for grant in researcher.get('grants', []):
        if 'investigators' in grant:
            investigators = [inv['name'] for inv in grant['investigators']]
            # Add edges between all investigators on same grant
            for i in range(len(investigators)):
                for j in range(i+1, len(investigators)):
                    G.add_edge(investigators[i], investigators[j])

# Find most collaborative researchers
centrality = nx.degree_centrality(G)
top_collaborators = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
```

---

## Data Quality Notes

### Known Limitations

1. **Missing fields**: Not all researchers have all fields populated
2. **Parsing errors**: Complex citations may not parse perfectly
3. **Incomplete information**: Website may not list all publications/grants
4. **Name variations**: Same person may appear with different name formats in publications
5. **Update lag**: Data is only as current as the last scrape

### Quality Checks

To verify data quality:

1. **Check required fields**:
```python
required = ['researcher_id', 'researcher_name', 'profile_url']
for field in required:
    assert field in researcher, f"Missing {field}"
```

2. **Validate publication structure**:
```python
for pub in researcher.get('publications', []):
    assert 'title' in pub or 'authors' in pub, "Invalid publication"
```

3. **Check for empty collections**:
```python
if not researcher.get('publications'):
    print(f"Warning: {researcher['researcher_name']} has no publications")
```

---

## Questions?

- **For technical parsing details**: See [Data Extraction](3_data_extraction.md)
- **For recent changes**: See [Changelog](changelog.md)
- **For design rationale**: See [Design Decisions](design_decisions.md)
- **For terms**: See [Glossary](glossary.md)
