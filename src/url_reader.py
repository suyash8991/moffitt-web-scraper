"""
Module for reading researcher URLs from Excel file.
"""
import pandas as pd
import os
import logging
from urllib.parse import urlparse, urlunparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def normalize_url(url):
    """
    Normalize a URL by ensuring it has a scheme and no trailing slashes.

    Args:
        url (str): The URL to normalize

    Returns:
        str: The normalized URL
    """
    parsed = urlparse(url)

    # Add https scheme if missing
    if not parsed.scheme:
        parsed = parsed._replace(scheme='https')

    # Ensure no trailing slash
    path = parsed.path.rstrip('/')
    if not path:
        path = '/'

    parsed = parsed._replace(path=path)

    return urlunparse(parsed)


def read_urls_from_excel(file_path, url_column=None):
    """
    Read researcher URLs from an Excel file.

    Args:
        file_path (str): Path to the Excel file
        url_column (str, optional): Name of the column containing URLs.
                                   If None, tries to auto-detect.

    Returns:
        list: List of URLs
    """
    if not os.path.exists(file_path):
        logger.error(f"Excel file not found: {file_path}")
        return []

    try:
        # Read the Excel file
        df = pd.read_excel(file_path)

        # If URL column name not provided, try to auto-detect
        if url_column is None:
            # Look for columns that might contain URLs
            possible_columns = [col for col in df.columns if any(
                keyword in col.lower() for keyword in ['url', 'link', 'website', 'profile']
            )]

            if not possible_columns:
                # If no obvious URL column, check the data itself for URLs
                for col in df.columns:
                    sample_values = df[col].dropna().astype(str).head(5).tolist()
                    if any('http' in val or 'www' in val or 'moffitt.org' in val for val in sample_values):
                        possible_columns.append(col)

            if possible_columns:
                url_column = possible_columns[0]
                logger.info(f"Auto-detected URL column: {url_column}")
            else:
                logger.error("Could not auto-detect URL column")
                return []

        # Extract URLs
        urls = df[url_column].dropna().astype(str).tolist()

        # Normalize URLs
        normalized_urls = [normalize_url(url) for url in urls]

        logger.info(f"Read {len(normalized_urls)} URLs from {file_path}")
        return normalized_urls

    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        return []


def get_researcher_urls(file_path='researcher_links.xlsx'):
    """
    Convenience function to get researcher URLs from the default Excel file.

    Args:
        file_path (str, optional): Path to the Excel file.
                                   Defaults to 'researcher_links.xlsx'.

    Returns:
        list: List of URLs
    """
    return read_urls_from_excel(file_path)


if __name__ == "__main__":
    # Test the module
    urls = get_researcher_urls()
    for i, url in enumerate(urls[:5]):  # Print first 5 URLs as sample
        print(f"{i+1}. {url}")
    print(f"Total URLs: {len(urls)}")