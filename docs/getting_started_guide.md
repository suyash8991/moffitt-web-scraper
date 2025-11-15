# Getting Started Guide

**Difficulty Level:** 🟢 Beginner

**Time Required:** 20-30 minutes

**Prerequisites:** None! This guide assumes zero programming experience.

---

## Table of Contents

1. [What You'll Need](#what-youll-need)
2. [Installing Python](#installing-python)
3. [Downloading the Project](#downloading-the-project)
4. [Setting Up Your Environment](#setting-up-your-environment)
5. [Installing Dependencies](#installing-dependencies)
6. [Running Your First Scrape](#running-your-first-scrape)
7. [Understanding the Output](#understanding-the-output)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps](#next-steps)

---

## What You'll Need

Before we begin, make sure you have:

- ✅ A computer with Windows, Mac, or Linux
- ✅ Internet connection
- ✅ About 500 MB of free disk space
- ✅ 15-30 minutes of time
- ✅ Administrator/sudo access (to install software)

---

## Installing Python

The scraper is written in Python, so we need to install it first.

### What is Python?

Python is a programming language - think of it as the "language" the computer uses to understand the scraper's instructions. Don't worry, you don't need to learn Python to use this tool!

### Check If You Already Have Python

**Windows:**
1. Press `Win + R` keys together
2. Type `cmd` and press Enter
3. Type `python --version` and press Enter

**Mac/Linux:**
1. Press `Cmd + Space` (Mac) or `Ctrl + Alt + T` (Linux)
2. Type `terminal` and press Enter
3. Type `python3 --version` and press Enter

**What you're looking for:**
- If you see something like `Python 3.8.0` or higher → **You're all set!**
- If you see `command not found` or `Python 2.x.x` → **Continue with installation**

### Installing Python (If Needed)

#### Windows

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow "Download Python" button
3. Run the downloaded installer
4. **IMPORTANT**: Check the box that says "Add Python to PATH"
5. Click "Install Now"
6. Wait for installation to complete
7. Verify installation by opening Command Prompt and typing `python --version`

#### Mac

**Option 1: Using Homebrew (Recommended)**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Option 2: Official Installer**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the macOS installer
3. Run the installer
4. Verify with `python3 --version`

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**For other Linux distributions**, use your package manager (yum, pacman, etc.)

---

## Downloading the Project

### Option 1: Download ZIP (Easiest)

1. Go to the project repository (where you got this link)
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to a folder (like `Documents/motiff-web-scraper`)

### Option 2: Using Git (For developers)

```bash
git clone https://github.com/your-username/motiff-web-scraper.git
cd motiff-web-scraper
```

---

## Setting Up Your Environment

### What is a Virtual Environment?

Think of a virtual environment like a separate "workspace" for this project. It keeps all the tools and libraries needed for this scraper separate from other Python projects on your computer.

**Analogy**: It's like having a separate toolbox for each home project, so your woodworking tools don't mix with your gardening tools.

### Creating the Virtual Environment

**Step 1: Open your terminal/command prompt**

**Windows:**
- Press `Win + R`
- Type `cmd`
- Press Enter

**Mac:**
- Press `Cmd + Space`
- Type `terminal`
- Press Enter

**Linux:**
- Press `Ctrl + Alt + T`

**Step 2: Navigate to the project folder**

```bash
# Replace with where you extracted/downloaded the project
cd path/to/motiff-web-scraper

# Example Windows:
cd C:\Users\YourName\Documents\motiff-web-scraper

# Example Mac/Linux:
cd /Users/YourName/Documents/motiff-web-scraper
```

**Step 3: Create the virtual environment**

**Windows:**
```bash
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

This creates a folder called `venv` with your isolated Python environment.

**Step 4: Activate the virtual environment**

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

**How to know it worked:**
You should see `(venv)` at the beginning of your command prompt:
```
(venv) C:\Users\YourName\Documents\motiff-web-scraper>
```

---

## Installing Dependencies

### What are Dependencies?

Dependencies are additional tools/libraries the scraper needs to work. Think of them like ingredients needed for a recipe.

The scraper needs:
- **crawl4ai** - To fetch web pages
- **pandas** - To read Excel files
- **aiofiles** - To save files efficiently
- And a few others...

### Install All Dependencies at Once

Make sure your virtual environment is activated (you see `(venv)` in your prompt), then run:

```bash
pip install -r requirements.txt
```

**What this does**: Automatically installs all required libraries.

**How long it takes**: 2-5 minutes depending on your internet speed.

**What you'll see**: Lots of text scrolling as packages are downloaded and installed.

### Troubleshooting Installation

**Problem: "pip: command not found"**

*Solution:* Try `pip3` instead of `pip`, or reinstall Python making sure to check "Add to PATH"

**Problem: "Permission denied" or "Access is denied"**

*Solution (Windows):* Run Command Prompt as Administrator

*Solution (Mac/Linux):* Don't use `sudo` with pip when in a virtual environment

**Problem: Installation fails with "no module named setuptools"**

*Solution:*
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

## Running Your First Scrape

### Quick Test: Scrape One Researcher

Let's start simple and scrape just one researcher's data.

**Command:**
```bash
python main.py --url "https://www.moffitt.org/research-science/researchers/ahmad-tarhini/" --department "immunology"
```

**What this does:**
- `python main.py` - Runs the main scraper program
- `--url` - Specifies which researcher to scrape
- `--department` - Specifies their department

**Expected output:**
```
2025-11-14 10:30:45 - INFO - Processing researcher: https://...
2025-11-14 10:30:47 - INFO - Crawling https://...
2025-11-14 10:30:52 - INFO - Saved HTML to data/raw_html/ahmad-tarhini.html
2025-11-14 10:30:52 - INFO - Saved markdown to data/markdown/ahmad-tarhini.md
2025-11-14 10:30:53 - INFO - Saved structured data to data/processed/ahmad-tarhini.json
```

**Success!** 🎉

### Scrape Multiple Researchers

To scrape all researchers from the Excel file:

```bash
python main.py
```

To scrape just the first 5 researchers (for testing):

```bash
python main.py --limit 5
```

**This will take longer** - about 10-15 seconds per researcher due to polite rate limiting.

---

## Understanding the Output

After running the scraper, you'll have three new folders:

```
motiff-web-scraper/
├── data/
│   ├── raw_html/        # Original web pages
│   ├── markdown/        # Readable text versions
│   └── processed/       # Organized JSON data
```

### Exploring Your Data

**1. Check the raw HTML (optional):**
```bash
# Navigate to the folder
cd data/raw_html

# Open a file in your browser
# Windows: start ahmad-tarhini.html
# Mac: open ahmad-tarhini.html
# Linux: xdg-open ahmad-tarhini.html
```

**2. Read the Markdown (easier to read):**
```bash
cd data/markdown

# Open in any text editor
# The .md files are just text files
```

**3. Examine the JSON (structured data):**
```bash
cd data/processed

# Open in any text editor or JSON viewer
# Recommendation: Use VS Code, Sublime Text, or an online JSON viewer
```

### What's in the JSON?

Open any `.json` file to see structured data like:

```json
{
  "researcher_id": "24764",
  "researcher_name": "ahmad tarhini",
  "degrees": ["MD", "PhD"],
  "primary_program": "cutaneous oncology",
  "department": "immunology",
  "publications": [
    {
      "authors": "Long GV, Nair N, ...",
      "title": "Neoadjuvant PD-1 and LAG-3...",
      "journal": "Nat Med",
      "year": "2025"
    }
  ],
  "grants": [
    {
      "title": "Predictors of Immunotherapeutic Benefits...",
      "sponsor": "COMMUNITY FOUNDATION OF TAMPA",
      "award_number": "N/A"
    }
  ]
}
```

See [Understanding the Data](understanding_the_data.md) for a detailed explanation of all fields.

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "ModuleNotFoundError: No module named 'crawl4ai'"

**Cause**: Dependencies not installed

**Solution**:
```bash
# Make sure virtual environment is activated
# Look for (venv) in your prompt

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: "FileNotFoundError: researcher_links.xlsx"

**Cause**: Excel file with URLs not found

**Solution**:
- Make sure `researcher_links.xlsx` is in the project root
- OR use `--url` to scrape a single URL instead

#### Issue: Scraper runs but no data appears

**Cause**: Check for error messages in the output

**Solution**:
1. Look at the logs in `moffitt_scraper.log`
2. Check your internet connection
3. Verify the URL is correct
4. Try with `--limit 1` to test one researcher

#### Issue: "Permission denied" when saving files

**Cause**: Don't have write permissions in the folder

**Solution** (Windows):
- Right-click the folder → Properties → Security → Edit permissions

**Solution** (Mac/Linux):
```bash
chmod -R 755 data/
```

#### Issue: Very slow or timing out

**Cause**: Network issues or website is slow

**Solution**:
- Check your internet connection
- Try again later
- The scraper waits 2-5 seconds between requests (this is normal and polite)

### Getting Help

If you're still stuck:

1. Check the [FAQ](FAQ.md)
2. Review the [Troubleshooting Guide](troubleshooting_guide.md)
3. Look at the log file: `moffitt_scraper.log`
4. Make sure you're using Python 3.8 or higher

---

## Next Steps

Congratulations! You've successfully run the Moffitt Researcher Scraper! 🎉

### To Learn More:

**Understand what just happened:**
- Read [How It Works (Simple)](how_it_works_simple.md) for a visual walkthrough
- Check [Understanding the Data](understanding_the_data.md) to make sense of the JSON

**Go deeper:**
- Read [Design Decisions](design_decisions.md) to understand why it works this way
- Explore [System Overview](1_system_overview.md) for technical details

**Use the data:**
- See [Working with the Data](working_with_data.md) for analysis examples
- Read [Extending the Scraper](extending_the_scraper.md) to modify it

### Quick Reference Commands

**Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**Scrape one researcher:**
```bash
python main.py --url "https://www.moffitt.org/research-science/researchers/RESEARCHER-NAME/" --department "DEPT-NAME"
```

**Scrape all researchers:**
```bash
python main.py
```

**Scrape first N researchers:**
```bash
python main.py --limit N
```

**Deactivate virtual environment:**
```bash
deactivate
```

---

**Remember**: The scraper is polite and waits 2-5 seconds between requests. This is normal and ethical web scraping behavior. Don't try to speed it up!

**Need help?** Check the [FAQ](FAQ.md) or [Troubleshooting Guide](troubleshooting_guide.md).
