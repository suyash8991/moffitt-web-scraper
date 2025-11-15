# Glossary of Terms

**Purpose:** Quick reference for technical terms used in this project

**How to use:** Press `Ctrl+F` (Windows/Linux) or `Cmd+F` (Mac) to search for a term

---

## A

### API (Application Programming Interface)
**Simple explanation:** A set of rules that lets different software programs talk to each other.

**Example:** Like a menu at a restaurant - it tells you what you can order and how to order it.

**In this project:** Not heavily used, but Python libraries have APIs we interact with.

---

### Async/Await (Asynchronous Programming)
**Simple explanation:** A way to do multiple things at once without waiting for each to finish.

**Example:** Like cooking where you put water on to boil, then chop vegetables while waiting, rather than standing and staring at the pot.

**In this project:** Used to fetch web pages efficiently while respecting rate limits.

**Technical:** `async` marks a function as asynchronous, `await` pauses execution until a result is ready.

---

## C

### Command Line / Terminal
**Simple explanation:** A text-based way to interact with your computer by typing commands.

**Example:** Instead of clicking icons, you type "python main.py" to run the program.

**Windows:** Called "Command Prompt" or "PowerShell"
**Mac/Linux:** Called "Terminal"

---

### Crawl4ai
**Simple explanation:** A Python library that helps download web pages automatically.

**Why we use it:** It handles JavaScript rendering, converts HTML to Markdown, and respects website rules.

**Alternative tools:** BeautifulSoup, Scrapy, Selenium

---

### Crawling (Web Crawling)
**Simple explanation:** Automatically visiting web pages to download their content.

**Example:** Like a robot going to each page in a phone book and copying the information.

**In this project:** We crawl researcher profile pages on the Moffitt website.

---

### CSV (Comma-Separated Values)
**Simple explanation:** A way to store data in a text file where commas separate different fields.

**Example:**
```
Name,Age,City
John,30,Boston
Jane,25,Seattle
```

**In this project:** Not directly used, but similar concept to how we organize data.

---

## D

### Data Extraction
**Simple explanation:** Pulling specific pieces of information from a larger document.

**Example:** Reading a recipe and writing down just the ingredients list, ignoring the photos and stories.

**In this project:** Extracting researcher names, publications, grants, etc. from web pages.

---

### Data Parsing
**Simple explanation:** Reading through text/code and understanding its structure to extract information.

**Example:** Looking at "Dr. John Doe, MD, PhD" and recognizing "John Doe" is the name and "MD, PhD" are degrees.

**In this project:** The `parse.py` file contains all our parsing logic.

---

### Dependency
**Simple explanation:** Another piece of software that a program needs to work.

**Example:** Like needing batteries for a flashlight - the flashlight depends on the batteries.

**In this project:** We depend on libraries like crawl4ai, pandas, aiofiles, etc.

---

## E

### Excel File (.xlsx)
**Simple explanation:** A spreadsheet file created by Microsoft Excel.

**Example:** Like a digital table with rows and columns.

**In this project:** We read researcher URLs from an Excel file called `researcher_links.xlsx`.

---

## H

### HTML (HyperText Markup Language)
**Simple explanation:** The code that websites are written in.

**Example:**
```html
<h1>Dr. John Doe</h1>
<p>Professor of Immunology</p>
```

**What you see:** "Dr. John Doe" as a big heading and "Professor of Immunology" as regular text.

**In this project:** We download HTML from Moffitt's website and extract information from it.

---

### HTTP/HTTPS
**Simple explanation:** The protocol (set of rules) for transferring web pages over the internet.

**HTTPS:** The secure version with encryption.

**Example:** Like the postal service rules for sending letters - HTTPS adds a locked box.

---

## J

### JSON (JavaScript Object Notation)
**Simple explanation:** A format for storing structured data that's easy for computers to read.

**Example:**
```json
{
  "name": "John Doe",
  "age": 30,
  "degrees": ["MD", "PhD"]
}
```

**Why use it:** Perfect for databases, APIs, and data analysis.

**In this project:** Our final output format - structured researcher data.

---

## L

### Library (Python Library)
**Simple explanation:** Pre-written code that adds functionality to Python.

**Example:** Like buying a pre-made cake mix instead of making everything from scratch.

**In this project:** We use libraries like pandas, crawl4ai, aiofiles, etc.

---

### Logging
**Simple explanation:** Keeping a record of what a program does, especially errors.

**Example:** Like a diary of everything the program tried to do and whether it worked.

**In this project:** We log to both the console and `moffitt_scraper.log` file.

---

## M

### Markdown (.md)
**Simple explanation:** A simple way to format text without HTML tags.

**Example:**
```markdown
# Big Heading
## Smaller Heading
**bold text**
*italic text*
```

**Why use it:** Easier to read than HTML, easier to process than plain text.

**In this project:** Intermediate format between HTML and JSON.

---

## P

### Pandas
**Simple explanation:** A Python library for working with data in tables/spreadsheets.

**In this project:** We use it to read the Excel file with researcher URLs.

---

### Parsing
See [Data Parsing](#data-parsing)

---

### pip
**Simple explanation:** Python's package installer - a tool to download and install libraries.

**Example:** Like an app store for Python code.

**Commands:**
- `pip install pandas` - Install pandas library
- `pip install -r requirements.txt` - Install all required libraries

---

### Python
**Simple explanation:** A popular programming language known for being beginner-friendly.

**Why we use it:** Great for data processing, web scraping, and has lots of helpful libraries.

**File extension:** `.py`

---

## R

### RAG (Retrieval-Augmented Generation)
**Simple explanation:** An AI technique where the AI looks up information before answering, instead of relying only on what it was trained on.

**Example:** Like a student who can use textbooks during a test (RAG) vs. relying only on memory (regular AI).

**In this project:** The bigger goal is to build a RAG system using this scraped data.

---

### Rate Limiting
**Simple explanation:** Limiting how fast requests are sent to avoid overwhelming a server.

**Example:** Like taking turns instead of everyone shouting at once.

**In this project:** We wait 2-5 seconds between each request to be polite to Moffitt's servers.

---

### Regex (Regular Expression)
**Simple explanation:** A pattern-matching language for finding text that matches a specific format.

**Example:** Find all phone numbers in format (123) 456-7890, regardless of what the actual numbers are.

**Pattern example:** `\d{4}` matches any 4-digit number

**In this project:** Used extensively to extract information from markdown text.

---

### Requirements.txt
**Simple explanation:** A file listing all the Python libraries a project needs.

**Example:**
```
crawl4ai>=0.7.0
pandas>=1.5.0
aiofiles>=0.8.0
```

**How to use:** `pip install -r requirements.txt`

---

## S

### Scraping (Web Scraping)
See [Web Scraping](#web-scraping)

---

### Schema
**Simple explanation:** A blueprint or structure that defines what data should look like.

**Example:** Like a form that says "Name goes here, Age goes here, etc."

**In this project:** We validate our JSON output against a schema to ensure data quality.

---

### Script
**Simple explanation:** A program file, usually one that automates tasks.

**In this project:** `main.py` is our main script.

---

## U

### URL (Uniform Resource Locator)
**Simple explanation:** A web address.

**Example:** `https://www.moffitt.org/research-science/researchers/ahmad-tarhini/`

**Parts:**
- `https://` - Protocol
- `www.moffitt.org` - Domain
- `/research-science/researchers/ahmad-tarhini/` - Path

---

## V

### Virtual Environment
**Simple explanation:** An isolated Python installation for a specific project.

**Why use it:** Keeps this project's dependencies separate from other Python projects.

**Example:** Like having separate toolboxes for different hobbies - your art supplies don't mix with your cooking tools.

**How to create:**
- Windows: `python -m venv venv`
- Mac/Linux: `python3 -m venv venv`

**How to activate:**
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

---

## W

### Web Crawling
See [Crawling](#crawling-web-crawling)

---

### Web Scraping
**Simple explanation:** Automatically extracting information from websites.

**Example:** Having a robot read 100 restaurant menus and organize the information into a spreadsheet.

**Legal when:**
- Public information
- Respecting rate limits
- Following robots.txt rules
- Not violating terms of service

**In this project:** We scrape public researcher profiles from Moffitt's website.

---

## Project-Specific Terms

### Award Number
**Simple explanation:** The unique identifier for a research grant.

**Example:** "5R01CA258089-05" or "22B09"

**In this project:** Extracted from grant entries and stored as a separate field.

---

### Content Hash
**Simple explanation:** A unique fingerprint for a piece of data.

**Why use it:** To detect if data has changed since last scrape.

**Technical:** We use SHA-256 hashing algorithm.

---

### Department
**Simple explanation:** The academic department a researcher belongs to.

**Example:** "Immunology", "Tumor Microenvironment and Metastasis"

**In this project:** Stored in lowercase for consistency (e.g., "immunology").

---

### Grant
**Simple explanation:** Funding awarded to researchers for their work.

**Example:** "$500,000 from NIH to study melanoma treatments"

**In this project:** We extract grant title, award number, sponsor, and investigators.

---

### Investigator
**Simple explanation:** A researcher working on a grant.

**Roles:**
- **PI (Principal Investigator):** The lead researcher
- **Co-PI:** A co-lead researcher
- **Co-I:** A contributing researcher

---

### Primary Program
**Simple explanation:** The main research program a researcher belongs to.

**Example:** "Molecular Medicine", "Immuno-Oncology"

**In this project:** Stored in lowercase with "Program" suffix removed.

---

### Publication
**Simple explanation:** A research paper published in a journal.

**Parts we extract:**
- Authors
- Title
- Journal name
- Year
- PubMed ID (unique identifier)

---

### Researcher ID (PERID)
**Simple explanation:** Moffitt's unique ID number for each researcher.

**Example:** "24764"

**In this project:** Extracted from the profile URL.

---

### Research Program
**Simple explanation:** Academic programs the researcher is affiliated with.

**Example:** "Molecular Medicine, Immuno-Oncology"

**In this project:** Can be comma-separated list, stored in lowercase.

---

## Still Confused?

If a term isn't explained here:

1. Check the [FAQ](FAQ.md)
2. Read the [Introduction for Beginners](0_introduction_for_beginners.md)
3. Search online - sites like Wikipedia often have good explanations
4. Look at the context where the term is used in the documentation

**Remember:** Every expert started as a beginner. Don't be afraid to look things up!
