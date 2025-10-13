"""
Example script to run the Moffitt Researcher Scraper on a single URL
"""
import asyncio
import json
from main import MoffittResearcherScraper

async def run_example():
    # URL of a sample researcher profile
    url = "https://www.moffitt.org/research-science/researchers/michael-vogelbaum/"

    # Initialize the scraper
    scraper = MoffittResearcherScraper()

    # Process the researcher profile
    print(f"Processing researcher profile: {url}")
    result = await scraper.process_researcher(url)

    if result:
        print("\nProcessing successful!")
        print(f"Researcher: {result.get('name')}, {', '.join(result.get('degrees', []))}")
        print(f"Title: {result.get('title', 'Not found')}")
        print(f"Primary Program: {result.get('primary_program', 'Not found')}")

        # Display research interests
        print(f"\nResearch Interests: {', '.join(result.get('research_interests', []))}")

        # Display publications count
        print(f"\nPublications: {len(result.get('publications', []))} entries")

        # Display grants count
        print(f"\nGrants: {len(result.get('grants', []))} entries")

        print("\nData saved to:")
        print(f"  - HTML: data/raw_html/michael-vogelbaum.html")
        print(f"  - Markdown: data/markdown/michael-vogelbaum.md")
        print(f"  - JSON: data/processed/michael-vogelbaum.json")
    else:
        print("Processing failed. Check the log file for details.")

if __name__ == "__main__":
    asyncio.run(run_example())