# Moffitt Cancer Center Web Scraper: Data Extraction Process

## 1. Data Extraction Overview

The data extraction functionality is implemented in `src/parse.py` through the `ResearcherProfileParser` class. This module is responsible for extracting structured information from markdown content that was previously converted from HTML.

## 2. Parser Architecture

The parser uses regular expression patterns to identify and extract different sections of researcher information from markdown content:

```python
class ResearcherProfileParser:
    """Parser for Moffitt researcher profile markdown files."""

    def __init__(self):
        self.section_patterns = {
            'name': r'#\s+(.*?),?\s*(?:MD|PhD|M\.D\.|Ph\.D\.)*',
            'title_program': r'Program Lead|Program Leader|Director|Chair|Professor|Associate Professor|Assistant Professor',
            'overview': r'##\s+Overview\n(.*?)(?=###|##|$)',
            'research_interests': r'##\s+Research\s+Interest\n(.*?)(?=###|##|$)',
            'education': r'###\s+Education\s+&\s+Training\n(.*?)(?=###|##|$)',
            'publications': r'##\s+Publications\n(.*?)(?=###|##|$)',
            'perid': r'PERID=(\d+)',
            'associations': r'###\s+Associations\n(.*?)(?=###|##|$)',
            'grants': r'##\s+Grants\n(.*?)(?=###|##|$)',
        }
```

The parser provides specialized methods to extract each type of information, and a main `parse_markdown` method that orchestrates the extraction process.

## 3. Extraction Process Flow

```
┌──────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│              │     │                 │     │                 │     │                 │
│ Read         │────▶│ Extract Core    │────▶│ Extract Detailed│────▶│ Generate Content │
│ Markdown     │     │ Information     │     │ Information     │     │ Hash            │
│              │     │                 │     │                 │     │                 │
└──────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
                                                                             │
                                                                             │
                                                                             ▼
                                                        ┌─────────────────────────────────┐
                                                        │                                 │
                                                        │  Return Complete Researcher     │
                                                        │  Object                         │
                                                        │                                 │
                                                        └─────────────────────────────────┘
```

## 4. Core Information Extraction

The parser extracts basic researcher information first:

### 4.1 Researcher ID

```python
def extract_researcher_id(self, markdown: str) -> str:
    """Extract the researcher ID from the markdown content."""
    match = re.search(self.section_patterns['perid'], markdown)
    if match:
        return match.group(1)
    return "unknown"
```

### 4.2 Researcher Name

```python
def extract_name(self, markdown: str) -> str:
    """Extract the researcher's name from the markdown content."""
    match = re.search(self.section_patterns['name'], markdown)
    if match:
        # Clean up name (remove degrees)
        name = match.group(1)
        name = re.sub(r',?\s*(?:MD|PhD|M\.D\.|Ph\.D\.)*$', '', name)
        return name.strip()
    return "Unknown Researcher"
```

### 4.3 Degrees

```python
def extract_degrees(self, markdown: str) -> List[str]:
    """Extract the researcher's degrees from the markdown content."""
    degrees = []

    # Look for degrees in the header
    header_match = re.search(r'#\s+.*?(MD|PhD|M\.D\.|Ph\.D\.)', markdown)
    if header_match:
        degrees_text = header_match.group(0)
        if "MD" in degrees_text or "M.D." in degrees_text:
            degrees.append("MD")
        if "PhD" in degrees_text or "Ph.D." in degrees_text:
            degrees.append("PhD")

    # Also check education section for degrees
    # ...

    return degrees
```

## 5. Detailed Information Extraction

After extracting basic information, the parser processes more detailed sections:

### 5.1 Title and Programs

```python
def extract_title_and_programs(self, markdown: str) -> Dict[str, str]:
    """Extract the researcher's title and program affiliations."""
    result = {
        "title": "",
        "primary_program": "",
        "research_program": ""
    }

    # Find the section after the name and before the overview
    # ...

    return result
```

### 5.2 Overview/Biography

```python
def extract_overview(self, markdown: str) -> str:
    """Extract the researcher's overview/biography."""
    match = re.search(self.section_patterns['overview'], markdown, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""
```

### 5.3 Research Interests

```python
def extract_research_interests(self, markdown: str) -> List[str]:
    """Extract the researcher's research interests."""
    interests = []

    # First try to find a Research Interest section
    match = re.search(self.section_patterns['research_interests'], markdown, re.DOTALL)
    if match:
        interests_text = match.group(1)
        # Return the whole paragraph for now
        return [interests_text.strip()]

    # If no specific section, look for Associations section
    # ...

    return interests
```

## 6. Complex Data Extraction

The parser handles more complex data structures like education history, publications, and grants:

### 6.1 Education History

```python
def extract_education(self, markdown: str) -> List[Dict[str, str]]:
    """Extract the researcher's education and training."""
    education = []

    match = re.search(self.section_patterns['education'], markdown, re.DOTALL)
    if match:
        education_text = match.group(1)

        # Parse different education types
        education_types = ["Graduate", "Medical School", "Internship", "Residency", "Fellowship", "Board Certification"]

        for edu_type in education_types:
            # Extract and process each education type
            # ...

    return education
```

### 6.2 Publications

```python
def extract_publications(self, markdown: str) -> List[Dict[str, str]]:
    """Extract the researcher's publications."""
    publications = []

    match = re.search(self.section_patterns['publications'], markdown, re.DOTALL)
    if match:
        publications_text = match.group(1)

        # Each publication typically starts with a bullet point
        pub_entries = re.findall(r'\s*\*\s+(.*?)(?=\s*\*\s+|\Z)', publications_text, re.DOTALL)

        for entry in pub_entries:
            pub = {"title": ""}

            # Extract publication details
            # - PubMed ID
            # - PMC ID
            # - Year
            # - Journal
            # - Title and authors
            # ...

            publications.append(pub)

    return publications
```

### 6.3 Grants Information

```python
def extract_grants(self, markdown: str) -> List[Dict[str, str]]:
    """Extract the researcher's grants information."""
    grants = []

    # Look for the Grants section
    match = re.search(self.section_patterns['grants'], markdown, re.DOTALL)
    if match:
        grants_text = match.group(1)

        # Extract individual grant entries
        grant_entries = re.findall(r'\s*\*\s+(.*?)(?=\s*\*\s+|\Z)', grants_text, re.DOTALL)

        for entry in grant_entries:
            grant = {"description": entry.strip()}

            # Extract grant details
            # - Grant ID
            # - Funding source
            # - Amount
            # - Period
            # ...

            grants.append(grant)

    return grants
```

## 7. Main Parsing Function

The main parsing function orchestrates the extraction of all information and returns a complete researcher object:

```python
def parse_markdown(self, markdown: str, profile_url: str) -> Dict[str, Any]:
    """Parse markdown content into a structured researcher profile."""
    researcher = {
        "profile_url": profile_url,
        "last_updated": datetime.utcnow().isoformat()
    }

    # Extract researcher ID
    researcher["researcher_id"] = self.extract_researcher_id(markdown)

    # Extract name
    researcher["name"] = self.extract_name(markdown)

    # Extract degrees
    researcher["degrees"] = self.extract_degrees(markdown)

    # Extract title and programs
    title_programs = self.extract_title_and_programs(markdown)
    researcher.update(title_programs)

    # Extract overview
    researcher["overview"] = self.extract_overview(markdown)

    # Extract research interests
    researcher["research_interests"] = self.extract_research_interests(markdown)

    # Extract associations
    researcher["associations"] = self.extract_associations(markdown)

    # Extract education
    researcher["education"] = self.extract_education(markdown)

    # Extract publications (limit to first 10 for efficiency)
    publications = self.extract_publications(markdown)
    researcher["publications"] = publications[:10] if len(publications) > 10 else publications

    # Extract grants
    researcher["grants"] = self.extract_grants(markdown)

    # Extract photo URL
    researcher["photo_url"] = self.extract_photo_url(markdown)

    # Extract contact information
    researcher["contact"] = self.extract_contact_info(markdown)

    # Generate content hash
    content_str = json.dumps(researcher, sort_keys=True)
    researcher["content_hash"] = hashlib.sha256(content_str.encode('utf-8')).hexdigest()

    return researcher
```

## 8. File-Based Parsing

For convenience, the parser also provides a method to parse directly from a file:

```python
def parse_markdown_file(self, file_path: str, profile_url: str = "") -> Dict[str, Any]:
    """Parse a markdown file into a structured researcher profile."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown = f.read()

        # If profile_url not provided, try to generate from filename
        if not profile_url:
            filename = os.path.basename(file_path)
            name = os.path.splitext(filename)[0]
            profile_url = f"https://www.moffitt.org/research-science/researchers/{name}/"

        return self.parse_markdown(markdown, profile_url)

    except Exception as e:
        logger.error(f"Error parsing markdown file {file_path}: {e}")
        return {"error": str(e)}
```

## 9. Extracted Data Structure

The final output is a comprehensive JSON object with the following structure:

```json
{
  "researcher_id": "24764",
  "profile_url": "https://www.moffitt.org/research-science/researchers/ahmad-tarhini/",
  "researcher_name": "Ahmad Tarhini",
  "degrees": ["MD", "PhD"],
  "title": "",
  "primary_program": "Cutaneous Oncology",
  "research_program": "Molecular Medicine Program,Immuno-Oncology Program",
  "overview": "As a clinical and translational physician-scientist...",
  "research_interests": ["As a clinical and translational physician-scientist..."],
  "associations": ["Cutaneous Oncology", "Immunology", ...],
  "education": [
    {
      "type": "Medical School",
      "institution": "Lithuanian University of Health Sciences",
      "degree": "MD"
    },
    ...
  ],
  "publications": [
    {
      "title": "Long GV, Nair N, Marbach D, ...",
      "pubmed_id": "40993242",
      "year": "2025",
      "authors": ""
    },
    ...
  ],
  "grants": [
    {
      "description": "Title: Predictors of Immunotherapeutic Benefits...",
      "source": "COMMUNITY FOUNDATION OF TAMPA"
    },
    ...
  ],
  "photo_url": "https://www.moffitt.org/globalassets/images/researchers_bio/TarhiniAhmad_24764.jpg",
  "contact": {
    "contact_url": "https://eforms.moffitt.org/ContactResearchersForm?PERID=24764"
  },
  "content_hash": "e67fff4c2bcd92c197f6ff1a23b53db958d9cd64d88c5ad0aafcc768e7637c59",
  "last_updated": "2025-10-18T23:43:39.932256"
}
```

## 10. Key Features of the Parser

- **Regular Expression Based**: Uses regex patterns for flexible text extraction
- **Multi-section Processing**: Handles various content sections independently
- **Error Tolerance**: Gracefully handles missing or malformatted sections
- **Content Hashing**: Generates hash for change detection
- **Publication Limiting**: Restricts to first 10 publications for efficiency
- **Multi-format Support**: Can process various layout formats