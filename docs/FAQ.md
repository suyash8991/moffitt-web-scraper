# Frequently Asked Questions (FAQ)

Quick answers to common questions. For detailed explanations, follow the links to other documentation.

---

## General Questions

### Q: What is this project?

**A:** It's a tool that automatically collects information about cancer researchers from the Moffitt Cancer Center website and organizes it into structured data files.

**Learn more:** [Introduction for Beginners](0_introduction_for_beginners.md)

---

### Q: Do I need to know programming to use this?

**A:** No! While programming knowledge helps, our [Getting Started Guide](getting_started_guide.md) is written for complete beginners. If you can follow step-by-step instructions and use a command line, you can use this tool.

---

### Q: Is web scraping legal?

**A:** Generally yes, when done responsibly:
- ✅ Scraping public information (researcher profiles are public)
- ✅ Using rate limiting (not overwhelming servers)
- ✅ Respecting robots.txt (website's rules for bots)
- ✅ For research/educational purposes

❌ **Not OK:** Scraping private data, ignoring terms of service, or commercial resale without permission.

**Always** check a website's terms of service before scraping.

---

### Q: Why would I want to use this?

**A:** If you need to:
- Build an AI system that can answer questions about cancer research
- Study collaboration patterns among researchers
- Analyze funding trends
- Create a searchable database of expertise
- Track publication patterns

**Learn more:** [Understanding the Data](understanding_the_data.md)

---

## Installation & Setup

### Q: What operating systems are supported?

**A:** Windows, Mac, and Linux. The tool works on all platforms that support Python 3.8+.

**Platform-specific help:** [Getting Started Guide](getting_started_guide.md)

---

### Q: What version of Python do I need?

**A:** Python 3.8 or higher. Python 2.x is **not** supported.

**Check your version:**
```bash
python --version   # Windows
python3 --version  # Mac/Linux
```

---

### Q: Do I need to install anything besides Python?

**A:** Yes, you need to install dependencies (additional Python libraries). This is easy:

```bash
pip install -r requirements.txt
```

**Learn more:** [Getting Started Guide - Installing Dependencies](getting_started_guide.md#installing-dependencies)

---

### Q: What is a virtual environment and do I need one?

**A:** A virtual environment keeps this project's dependencies separate from other Python projects on your computer.

**Do you need it?** Highly recommended but not strictly required.

**Analogy:** Like having separate toolboxes for different projects.

**How to create:** See [Getting Started Guide - Setting Up Environment](getting_started_guide.md#setting-up-your-environment)

---

## Using the Scraper

### Q: How do I scrape just one researcher?

**A:**
```bash
python main.py --url "https://www.moffitt.org/research-science/researchers/RESEARCHER-NAME/" --department "DEPARTMENT"
```

**Example:**
```bash
python main.py --url "https://www.moffitt.org/research-science/researchers/ahmad-tarhini/" --department "immunology"
```

---

### Q: How do I scrape all researchers?

**A:** Make sure you have a file called `researcher_links.xlsx` with all URLs, then run:

```bash
python main.py
```

---

### Q: How long does it take to scrape all researchers?

**A:** About 10-15 seconds per researcher due to polite rate limiting (2-5 second delays between requests).

**For 100 researchers:** ~20-25 minutes
**For 500 researchers:** ~2 hours

**Why so slow?** We're being respectful to Moffitt's servers. Faster scraping could overload their website.

---

### Q: Can I make it go faster?

**A:** **No, and you shouldn't try.** The rate limiting is there for ethical reasons:
- Prevents overloading Moffitt's servers
- Avoids getting blocked/banned
- Respects their website resources

**This is good practice** in web scraping.

---

### Q: Where does the data get saved?

**A:** In three folders:

- `data/raw_html/` - Original web pages
- `data/markdown/` - Readable text versions
- `data/processed/` - Structured JSON data

**Learn more:** [Understanding the Data](understanding_the_data.md)

---

## Understanding the Output

### Q: What's the difference between HTML, Markdown, and JSON files?

**A:**

| Format | What it is | Who it's for |
|--------|-----------|--------------|
| **HTML** | Original web page | Archival/reprocessing |
| **Markdown** | Simplified text | Human reading |
| **JSON** | Structured data | Computers/analysis |

**Learn more:** [How It Works (Simple)](how_it_works_simple.md)

---

### Q: How do I open/read the JSON files?

**A:** JSON files are just text files. You can open them with:
- Any text editor (Notepad, TextEdit, etc.)
- Code editors (VS Code, Sublime Text) - better formatting
- Online JSON viewers (search "JSON viewer online")

**For analysis:** Load them in Python, R, or other data analysis tools.

**Learn more:** [Working with the Data](working_with_data.md)

---

### Q: What data does the scraper extract?

**A:** For each researcher:
- Basic info (name, degrees, title)
- Department and program affiliations
- Research interests
- Publications (authors, title, journal, year)
- Grants (title, award number, sponsor, investigators)
- Education history
- Contact information

**See examples:** [Understanding the Data](understanding_the_data.md)

---

### Q: Why is everything in lowercase now?

**A:** Recent update (November 2025) converts program names, departments, and researcher names to lowercase for consistency.

**Why?** Makes searching and grouping easier:
- Before: "Immunology" and "immunology" treated as different
- After: Both are "immunology"

**Learn more:** [Changelog](changelog.md)

---

## Troubleshooting

### Q: I get "ModuleNotFoundError: No module named 'crawl4ai'"

**A:** Dependencies aren't installed. Run:

```bash
pip install -r requirements.txt
```

Make sure your virtual environment is activated (you should see `(venv)` in your command prompt).

---

### Q: I get "FileNotFoundError: researcher_links.xlsx"

**A:** Two solutions:

**Solution 1:** Put `researcher_links.xlsx` file in the project root folder

**Solution 2:** Scrape a single URL instead:
```bash
python main.py --url "https://www.moffitt.org/research-science/researchers/NAME/"
```

---

### Q: The scraper runs but produces no output

**A:** Check for errors:

1. Look at the console output for error messages
2. Check the log file: `moffitt_scraper.log`
3. Verify your internet connection
4. Make sure the URL is correct
5. Try with just one researcher: `--limit 1`

**Detailed troubleshooting:** [Troubleshooting Guide](troubleshooting_guide.md)

---

### Q: I get "Permission denied" errors

**A:**

**Windows:**
- Run Command Prompt as Administrator
- Check folder permissions

**Mac/Linux:**
- Don't use `sudo` with pip when in a virtual environment
- Check folder permissions: `chmod -R 755 data/`

---

### Q: The scraper is very slow or timing out

**A:**

1. **Check internet connection** - slow connection = slow scraping
2. **The website might be slow** - try again later
3. **This is normal** - 2-5 second delays are intentional rate limiting

If it completely stalls:
- Check `moffitt_scraper.log` for errors
- Try a single URL to test: `--limit 1`

---

## Technical Questions

### Q: What Python libraries does this use?

**A:**
- **crawl4ai** - Web crawling
- **pandas** - Excel file reading
- **aiofiles** - Asynchronous file operations
- **jsonschema** - Data validation
- And a few others (see `requirements.txt`)

---

### Q: How does it extract information from web pages?

**A:** Using **regular expressions (regex)** to find patterns in text.

**Example:** Find all 4-digit years, all email addresses, text between specific labels, etc.

**Learn more:** [Data Extraction](3_data_extraction.md)

---

### Q: Can I modify it to scrape other websites?

**A:** Yes, but you'll need to:
1. Update the URL patterns
2. Modify the regex patterns for the new website's format
3. Adjust the data schema

**Learn more:** [Extending the Scraper](extending_the_scraper.md)

---

### Q: Why use three different file formats?

**A:**

1. **HTML** - Preservation of original data for reprocessing
2. **Markdown** - Easier for humans and computers to read
3. **JSON** - Perfect for databases and AI systems

**Learn more:** [Design Decisions](design_decisions.md)

---

### Q: What is RAG and how does this relate?

**A:** RAG (Retrieval-Augmented Generation) is an AI technique where the AI looks up information before answering questions.

This scraper provides the structured data that a RAG system can search through.

**Think of it as:** Building a library that an AI can use to look up facts.

**Learn more:** [Glossary - RAG](glossary.md#rag-retrieval-augmented-generation)

---

## About the Project

### Q: Who created this?

**A:** This is an open-source project for building RAG systems with cancer research data.

---

### Q: Can I contribute improvements?

**A:** Yes! See [Extending the Scraper](extending_the_scraper.md) for guidelines on modifications.

---

### Q: What was recently updated?

**A:** November 2025 updates:
- ✅ Better publication parsing (separates authors/titles accurately)
- ✅ Enhanced grant extraction (structured fields)
- ✅ Lowercase conversion for consistency
- ✅ Automatic "Program" suffix removal

**Learn more:** [Changelog](changelog.md)

---

### Q: How do I report bugs or request features?

**A:** Check the project repository for issue tracking/contact information.

---

## Still Have Questions?

**Can't find your answer here?**

1. Check the [Glossary](glossary.md) for term definitions
2. Read the [Introduction for Beginners](0_introduction_for_beginners.md)
3. Review the [Troubleshooting Guide](troubleshooting_guide.md)
4. Look at specific technical docs in the [Documentation Index](README.md)

**For beginners:** Start with the [Getting Started Guide](getting_started_guide.md)

**For developers:** Check the [System Overview](1_system_overview.md)
