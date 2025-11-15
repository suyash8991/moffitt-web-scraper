# Design Decisions

> Why the code is structured the way it is

This document explains the reasoning behind major architectural and implementation decisions in the Moffitt Cancer Center Researcher Data Scraper.

**Reading time**: 20 minutes

---

## Table of Contents

1. [Architecture Decisions](#architecture-decisions)
2. [Data Format Decisions](#data-format-decisions)
3. [Parsing Decisions](#parsing-decisions)
4. [Recent Improvements (Nov 2025)](#recent-improvements-nov-2025)
5. [Trade-offs and Alternatives](#trade-offs-and-alternatives)

---

## Architecture Decisions

### Decision 1: Three-Stage Pipeline (HTML → Markdown → JSON)

**What we did**: Save data in three formats instead of directly converting HTML to JSON.

**Why**:

1. **Resilience**: If we improve the parsing logic, we can re-parse from HTML without re-downloading
2. **Debugging**: Markdown is human-readable, making it easy to verify quality
3. **Flexibility**: Different consumers can use different formats:
   - AI systems → JSON
   - Full-text search → Markdown
   - Archive/audit → HTML

**Alternative considered**: Direct HTML → JSON conversion

**Why we didn't**: Would require re-downloading every time we improve parsing logic. During development, we discovered several parsing bugs that required re-processing all 127 researchers. Having the HTML cached saved hours of re-downloading.

**Cost**: Additional disk space (~3x more storage), but disk is cheap and the benefits outweigh the cost.

---

### Decision 2: Asynchronous Processing (async/await)

**What we did**: Use Python's `async/await` for I/O operations (network requests, file writes).

**Why**:

1. **Performance**: While waiting for a network response, the program can process other researchers
2. **Scalability**: Can handle 100+ researchers efficiently
3. **Rate limiting integration**: Easy to implement delays without blocking the entire program

**Alternative considered**: Synchronous (sequential) processing

**Why we didn't**: Would take 10+ minutes to process all researchers (vs. 5-7 minutes with async). The time adds up during development when you run the scraper dozens of times.

**Example benefit**:
```
Synchronous: Download 1 → Process 1 → Download 2 → Process 2
             [========][====]       [========][====]
             Total: 24 seconds for 2 researchers

Async:       Download 1 → Process 1
             [========][====]
                Download 2 → Process 2
                [========][====]
             Total: 14 seconds for 2 researchers (overlapping)
```

---

### Decision 3: Rate Limiting (2-5 Second Delays)

**What we did**: Wait 2-5 seconds (random) between requests to the Moffitt website.

**Why**:

1. **Ethical scraping**: Prevents overloading the server
2. **Avoid IP bans**: Mimics human browsing behavior
3. **Sustainability**: Ensures we can continue using this tool long-term
4. **Legal compliance**: Demonstrates good faith and respectful use

**Alternative considered**: No delays (faster scraping)

**Why we didn't**:
- Risk of getting blocked by the website
- Unethical to potentially impact website performance
- Violates common web scraping best practices

**Trade-off**: Slower processing (5-7 minutes instead of 2-3 minutes), but worth it for ethical and practical reasons.

---

### Decision 4: Content Hashing for Change Detection

**What we did**: Calculate SHA-256 hash of page content and store it. Skip re-processing if hash hasn't changed.

**Why**:

1. **Efficiency**: Don't waste time re-processing unchanged pages
2. **Bandwidth**: Don't re-download if not needed
3. **Respectful**: Minimize requests to the source website
4. **Incremental updates**: Can run the scraper regularly to catch only new changes

**How it works**:
```python
new_hash = hashlib.sha256(html_content.encode()).hexdigest()
if new_hash == old_hash:
    print("Content unchanged, skipping")
    return
```

**Alternative considered**: Always re-process everything

**Why we didn't**: Wasteful. In a typical re-run, 95% of researcher pages haven't changed. Processing all 127 researchers every time would take 5-7 minutes vs. 30 seconds for just the changed ones.

---

## Data Format Decisions

### Decision 5: Excel File for Input URLs

**What we did**: Use an Excel file (`researcher_links.xlsx`) to store the list of researcher URLs.

**Why**:

1. **User-friendly**: Non-technical users can edit Excel files
2. **Flexible**: Easy to add/remove researchers without touching code
3. **Additional metadata**: Can include department info or notes in extra columns
4. **Familiarity**: Most people already know how to use Excel

**Alternative considered**: Text file, CSV, or hardcoded list

**Why we didn't**:
- Text/CSV: Less user-friendly for non-technical users
- Hardcoded: Requires editing Python code to add/remove researchers
- Excel is a good balance of accessibility and structure

**Trade-off**: Requires `openpyxl` dependency, but it's a small, well-maintained library.

---

### Decision 6: JSON for Structured Output

**What we did**: Use JSON as the final structured data format.

**Why**:

1. **Universal**: Supported by virtually every programming language
2. **RAG-friendly**: Easy to load into vector databases (ChromaDB, Pinecone, etc.)
3. **Human-readable**: Unlike binary formats, you can inspect JSON in a text editor
4. **Queryable**: Can be loaded into databases or processed with jq, pandas, etc.

**Alternative considered**: SQL database, CSV, XML

**Why we didn't**:
- **SQL database**: Adds complexity (server setup, migrations), overkill for 127 records
- **CSV**: Can't represent nested structures (publications, grants)
- **XML**: More verbose, less popular than JSON in modern systems

**Example**: Easy to load into a RAG system:
```python
import json
data = json.load(open('data/processed/researcher-name.json'))
# Ready to insert into vector database
```

---

## Parsing Decisions

### Decision 7: Using Crawl4AI Library

**What we did**: Use the Crawl4AI library instead of writing custom parsing from scratch.

**Why**:

1. **Proven**: Battle-tested library used by many projects
2. **Maintained**: Active development and bug fixes
3. **Features**: Built-in rate limiting, markdown conversion, async support
4. **Focus**: Lets us focus on domain logic (what to extract) vs. infrastructure (how to fetch)

**Alternative considered**: Requests + BeautifulSoup (traditional approach)

**Why we didn't**: Would require implementing:
- Async/await handling
- Rate limiting
- HTML → Markdown conversion
- Error handling and retries
- User-agent management

Crawl4AI provides all of this out of the box.

**Trade-off**: Additional dependency, but it's a small price for significant functionality.

---

### Decision 8: Markdown as Intermediate Format

**What we did**: Convert HTML to Markdown before extracting structured data.

**Why**:

1. **Simplicity**: Markdown is easier to parse than HTML (no tags, simpler structure)
2. **Readability**: Can manually review the Markdown to verify quality
3. **Text-based patterns**: Can use simple regex on clean text instead of DOM traversal
4. **Reusability**: Markdown files can be used for other purposes (documentation, search)

**Alternative considered**: Parse directly from HTML using CSS selectors

**Why we didn't**: HTML structure can change (CSS classes renamed, tags reorganized). Markdown is more stable because it's based on semantic content, not styling.

**Example**:
```html
<!-- HTML: Complex and fragile -->
<div class="researcher-bio-section-v2">
  <p class="bio-text">Dr. Smith is a researcher...</p>
</div>

<!-- Markdown: Simple and stable -->
## Overview
Dr. Smith is a researcher...
```

---

## Recent Improvements (Nov 2025)

The following decisions were made during the November 2025 enhancement phase.

### Decision 9: Publication Parsing Using Period Delimiters

**What we did**: Use the first two periods (`.`) in a citation to separate authors, title, and journal.

**Why**:

1. **Reliable**: Citations follow a consistent format: `Authors. Title. Journal. Year.`
2. **Simple**: Don't need complex NLP or citation parsing libraries
3. **Accurate**: Tested on 100+ actual citations from the dataset

**Alternative considered**:
- Citation parsing library (like `anystyle`, `citeproc`)
- Machine learning model
- Split on last period (original approach)

**Why we didn't**:
- **Library**: Overkill for our simple format, adds dependencies
- **ML**: Too complex for a rule-based problem
- **Last period**: Failed because journal details often have periods (e.g., "vol. 15, no. 3")

**Example failure of old approach**:
```
Citation: "Smith J, Doe A. New treatment. Nature Med. 2024."
Old logic: Split on last period
  → authors + title: "Smith J, Doe A. New treatment. Nature Med"
  → year: "2024"
  Problem: Title and journal are mixed!

New logic: Split on first two periods
  → authors: "Smith J, Doe A"
  → title: "New treatment"
  → journal: "Nature Med"
  ✓ Correct!
```

**Code location**: [src/parse.py:334-380](../src/parse.py)

---

### Decision 10: Structured Grant Extraction with Labeled Fields

**What we did**: Extract grant information using labeled field prefixes (`Title:`, `Award Number:`, `Sponsor:`).

**Why**:

1. **Consistent format**: Moffitt website uses consistent labeling
2. **Queryable**: Can filter researchers by funding source, award number
3. **Structured**: Enables analysis (e.g., "Who are NIH-funded researchers?")
4. **Investigator roles**: Preserves who is PI vs. Co-I

**Alternative considered**:
- Store entire grant as single text blob (original approach)
- Use NLP to extract entities

**Why we didn't**:
- **Text blob**: Not queryable, hard to analyze
- **NLP**: Overkill when we have labeled fields

**Example**:
```markdown
Input:
Title: Mechanisms of immune evasion in melanoma
Award Number: R01CA123456
Sponsor: National Cancer Institute

Output JSON:
{
  "title": "Mechanisms of immune evasion in melanoma",
  "award_number": "R01CA123456",
  "sponsor": "National Cancer Institute"
}
```

**Benefits realized**:
- Can query: "All researchers with NIH grants"
- Can track: "Publications from R01CA123456"
- Can analyze: "Collaboration networks by co-investigators"

**Code location**: [src/parse.py:417-507](../src/parse.py)

---

### Decision 11: Lowercase Normalization for Categorical Fields

**What we did**: Convert all program names, departments, and researcher names to lowercase.

**Why**:

1. **Consistency**: "Immunology" and "immunology" should be the same category
2. **Querying**: Makes searching case-insensitive by default
3. **Grouping**: Enables accurate counts (e.g., "How many immunology researchers?")
4. **Sorting**: Alphabetical sorting works correctly

**Alternative considered**:
- Keep original capitalization
- Title case (capitalize first letter of each word)
- Normalize during query time

**Why we didn't**:
- **Original**: Causes duplicate categories
- **Title case**: Inconsistent (is it "Thoracic Oncology" or "Thoracic oncology"?)
- **Query normalization**: Extra work for every query, error-prone

**Example problem solved**:
```
Before normalization:
  researchers = [
    {"program": "Immunology"},
    {"program": "immunology"},
    {"program": "IMMUNOLOGY"}
  ]

  group_by_program() → {
    "Immunology": 1,
    "immunology": 1,
    "IMMUNOLOGY": 1
  } ❌ Wrong! Should be 3

After normalization:
  researchers = [
    {"program": "immunology"},
    {"program": "immunology"},
    {"program": "immunology"}
  ]

  group_by_program() → {
    "immunology": 3
  } ✓ Correct!
```

**Trade-off**: Lose original capitalization, but it's not meaningful information (we're not displaying this directly to users, and we can always title-case it for display).

**Code location**: [src/parse.py:143,155](../src/parse.py), [main.py:109,112,227,256](../main.py)

---

### Decision 12: Remove "Program" Suffix from Program Names

**What we did**: Strip " Program" suffix from program names before storing.

**Why**:

1. **Redundant**: The field is called `primary_program`, so "Program" is implied
2. **Consistency**: Some programs had suffix, others didn't
3. **Cleaner queries**: Filter by "immunology" instead of "immunology program"
4. **Data normalization**: Standard practice to remove redundant information

**Alternative considered**: Keep " Program" suffix

**Why we didn't**: Creates inconsistency. Database shows:
```
Programs:
- immunology
- immunology program  ← Duplicate!
- cancer biology
- cancer biology program  ← Duplicate!
```

**Example**:
```
Input: "Immunology Program"
Remove suffix: "Immunology"
Lowercase: "immunology"
Final: "immunology" ✓
```

**Code location**: [src/parse.py:135-156](../src/parse.py)

---

## Trade-offs and Alternatives

### What We Sacrificed

Every design decision involves trade-offs. Here's what we gave up:

1. **Speed for Ethics**: Rate limiting makes scraping slower, but it's the right thing to do
2. **Storage for Flexibility**: Three formats use 3x disk space, but enable re-parsing and debugging
3. **Simplicity for Accuracy**: Complex parsing logic (period detection, regex) vs. simple text extraction
4. **Real-time for Batch**: Process all researchers at once instead of on-demand (simpler, sufficient for use case)

### What We Could Improve (Future Work)

1. **Incremental processing**: Only process researchers whose pages changed (partially implemented via content hashing)
2. **Parallel processing**: Process multiple researchers simultaneously (currently sequential with async I/O)
3. **Validation**: Add JSON schema validation to ensure data quality
4. **Monitoring**: Add logging and metrics (processing time, error rates, etc.)
5. **API**: Provide a REST API instead of just file-based output

### Why We Made These Choices

The guiding principles were:

1. **Simplicity**: Easy to understand and maintain
2. **Reliability**: Prefer robust solutions over clever hacks
3. **Ethics**: Respectful web scraping practices
4. **Flexibility**: Support future improvements without major rewrites
5. **User-focused**: Make it accessible to non-experts

---

## Lessons Learned

### What Worked Well

1. **Three-format storage**: Saved countless hours during development
2. **Crawl4AI**: Solid library, minimal issues
3. **Incremental improvements**: Could enhance parsing without re-downloading
4. **Test-driven**: Analyzing actual data before implementing parsing logic

### What We'd Do Differently

1. **Start with structured extraction**: Original version dumped everything into description fields. Should have structured it from the start.
2. **More comprehensive testing**: Some edge cases in publications weren't discovered until processing all 127 researchers
3. **Documentation-first**: Writing docs revealed gaps in our understanding and design

---

## Questions?

- **For technical details**: See the numbered documentation (1-5)
- **For usage**: See [Getting Started Guide](getting_started_guide.md)
- **For understanding output**: See [Understanding the Data](understanding_the_data.md)
- **For terms**: See [Glossary](glossary.md)
