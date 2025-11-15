# Changelog

All notable changes to the Moffitt Cancer Center Researcher Data Scraper are documented in this file.

## [November 2025] - Major Data Extraction Improvements

This release focused on significantly improving the quality and structure of extracted data based on real-world analysis of scraped content.

### Enhanced Publication Parsing

**Problem**: Publications were not being correctly separated into authors, title, and journal name. The original logic used the last period (`.`) in the citation, which often incorrectly split the journal information.

**Solution**: Implemented intelligent period detection that uses the first two periods as delimiters:
- Text before first period = Authors list
- Text between first and second period = Paper title
- Text after second period = Journal name and details

**Impact**: Publications are now accurately structured with proper separation of authors, titles, and journal information.

**Example**:
```
Before: Everything lumped into one field
After:
  authors: "Smith J, Doe A, Johnson B"
  title: "Novel approaches to cancer treatment"
  journal: "Nature Medicine"
  journal_details: "15(3):234-245"
```

**Files Changed**: `src/parse.py` (lines 334-380)

**Commit**: `Fix publication extraction to properly separate authors and title`

---

### Structured Grant Data Extraction

**Problem**: Grant information was being stored as a single unstructured description field, making it difficult to query by sponsor, award number, or investigator.

**Solution**: Implemented structured field extraction using labeled prefixes:
- `Title:` → Extract grant title
- `Award Number:` → Extract award identifier (skip "N/A" values)
- `Sponsor:` → Extract funding organization
- Investigator names with roles → Parse into structured list

**Impact**: Grants are now queryable by specific fields, enabling analysis by funding source, investigator role, and award tracking.

**Example**:
```json
{
  "title": "Mechanisms of immune evasion in melanoma",
  "award_number": "R01CA123456",
  "sponsor": "National Cancer Institute",
  "investigators": [
    {
      "name": "Smith, J.",
      "role": "Principal Investigator"
    }
  ]
}
```

**Files Changed**: `src/parse.py` (lines 417-507)

**Commits**:
- `Add structured extraction of grant titles and award numbers`
- `Complete grant extraction improvements with sponsor and investigator information`

---

### Data Normalization - Lowercase Conversion

**Problem**: Field values had inconsistent capitalization (e.g., "Immunology" vs "immunology", "Cancer Biology" vs "cancer biology"), making grouping and filtering difficult.

**Solution**: Standardized all categorical fields to lowercase:
- `primary_program` → lowercase
- `research_program` → lowercase (applies to all programs in comma-separated list)
- `department` → lowercase
- `researcher_name` → lowercase

**Impact**: Consistent formatting enables accurate grouping, filtering, and searching across all researchers.

**Example**:
```
Before:
  primary_program: "Immunology"
  department: "Thoracic Oncology"
  researcher_name: "John Smith"

After:
  primary_program: "immunology"
  department: "thoracic oncology"
  researcher_name: "john smith"
```

**Files Changed**:
- `src/parse.py` (lines 143, 155)
- `main.py` (lines 109, 112, 227, 256)

**Commit**: `Convert program names, department, and researcher names to lowercase`

---

### Program Name Cleanup

**Problem**: Some program names had inconsistent " Program" suffixes (e.g., "Immunology Program" vs "Immunology"), creating duplicate categories.

**Solution**: Automatically strip " Program" suffix from program names before storage. Works with both single programs and comma-separated lists.

**Impact**: Clean, consistent program names without redundant suffixes.

**Example**:
```
Before:
  primary_program: "Immunology Program"
  research_program: "Cancer Biology Program, Drug Discovery Program"

After:
  primary_program: "immunology"
  research_program: "cancer biology, drug discovery"
```

**Files Changed**: `src/parse.py` (lines 135-156)

**Commit**: `Remove 'Program' suffix from program names during extraction`

---

### Documentation Improvements

**Added**: Comprehensive beginner-friendly documentation to make the project accessible to users without web scraping experience.

**New Files Created**:
- `docs/0_introduction_for_beginners.md` - What is web scraping and why this project exists
- `docs/getting_started_guide.md` - Step-by-step installation for all platforms
- `docs/glossary.md` - Technical terms explained simply
- `docs/FAQ.md` - Quick answers to common questions

**Updated Files**:
- `README.md` - Restructured with Quick Links organized by audience, recent improvements section
- `docs/3_data_extraction.md` - Updated to reflect new publication and grant parsing logic

**Impact**: Non-technical users can now understand and use the scraper. Developers can quickly find the information they need based on their experience level.

**Commit**: `Update documentation to reflect improvements in data extraction`

---

## Why These Changes Matter

These improvements transform the data from loosely structured text into properly structured, queryable fields. This enables:

1. **Better RAG Performance**: AI systems can more accurately retrieve relevant publications by author, title, or journal
2. **Grant Analysis**: Filter and group researchers by funding source, track collaborations
3. **Consistent Queries**: Lowercase normalization means searches work reliably regardless of capitalization
4. **Data Quality**: Structured fields are easier to validate and ensure completeness

## Migration Notes

**For Existing Data**: If you have previously scraped data, you should re-run the scraper to apply these improvements. The three-format storage system (HTML → Markdown → JSON) means you can re-parse from existing HTML files without re-downloading.

**Breaking Changes**: The JSON structure has changed for publications and grants. If you have code that depends on the old structure:
- Publications: Update code to use `authors`, `title`, `journal` instead of single field
- Grants: Update code to use `title`, `award_number`, `sponsor`, `investigators` fields

## Technical Details

For detailed technical information about how these changes were implemented, see:
- [Data Extraction Documentation](3_data_extraction.md) - Code examples and regex patterns
- [Data Storage Documentation](4_data_storage.md) - Field specifications and validation
