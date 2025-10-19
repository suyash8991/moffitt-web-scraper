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


def read_urls_from_excel(file_path, url_column=None, dept_column=None):
    """
    Read researcher URLs and departments from an Excel file.

    Args:
        file_path (str): Path to the Excel file
        url_column (str, optional): Name of the column containing URLs.
                                   If None, tries to auto-detect.
        dept_column (str, optional): Name of the column containing department information.
                                    If None, tries to auto-detect.

    Returns:
        dict: Dictionary with URLs as keys and department info as values
    """
    if not os.path.exists(file_path):
        logger.error(f"Excel file not found: {file_path}")
        return {}

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
                return {}

        # If department column name not provided, try to auto-detect
        if dept_column is None:
            # Look for columns that might contain department info
            possible_dept_columns = [col for col in df.columns if any(
                keyword in col.lower() for keyword in ['department', 'dept', 'division', 'section']
            )]

            if possible_dept_columns:
                dept_column = possible_dept_columns[0]
                logger.info(f"Auto-detected Department column: {dept_column}")
            else:
                # If we can't find a department column by keyword, check all columns
                for col in df.columns:
                    if 'department' in col.lower():
                        dept_column = col
                        logger.info(f"Found Department column: {dept_column}")
                        break

                # If still not found, log a warning
                if dept_column is None:
                    logger.warning("Could not auto-detect department column")

            # Force the exact column name if we know it should be there
            if 'Department' in df.columns:
                dept_column = 'Department'
                logger.info(f"Using exact Department column match: {dept_column}")

        # Create a dictionary mapping URLs to departments
        result = {}

        for idx, row in df.iterrows():
            if pd.notna(row[url_column]):
                url = normalize_url(str(row[url_column]))

                # Extract department with better error handling
                dept = ""
                if dept_column:
                    try:
                        dept_value = row.get(dept_column)
                        if pd.notna(dept_value):
                            dept = str(dept_value).strip()
                    except Exception as e:
                        logger.warning(f"Error extracting department for {url}: {e}")

                # Add to result dictionary
                result[url] = dept

                # Log for debugging
                if dept:
                    logger.info(f"URL: {url} -> Department: {dept}")

        logger.info(f"Read {len(result)} URL-department pairs from {file_path}")

        # Log specific researcher for debugging
        for url, dept in result.items():
            if "ahmad-tarhini" in url.lower():
                logger.info(f"DEBUG: Ahmad Tarhini URL: {url} -> Department: {dept}")

        return result

    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        return {}


def get_researcher_urls(file_path='researcher_links.xlsx'):
    """
    Convenience function to get researcher URLs from the default Excel file.

    Args:
        file_path (str, optional): Path to the Excel file.
                                   Defaults to 'researcher_links.xlsx'.

    Returns:
        dict: Dictionary with URLs as keys and department info as values
    """
    return read_urls_from_excel(file_path)


if __name__ == "__main__":
    # Test the module
    url_dept_dict = get_researcher_urls()
    print("First 5 URLs with their departments:")
    for i, (url, dept) in enumerate(list(url_dept_dict.items())[:5]):  # Print first 5 URL-department pairs
        print(f"{i+1}. {url} -> Department: {dept}")
    print(f"Total URL-Department pairs: {len(url_dept_dict)}")