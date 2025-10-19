import pandas as pd
from src.url_reader import read_urls_from_excel

# Test the Excel reading function with explicit column names
def test_excel_reading():
    # Path to the Excel file
    excel_file = "researcher_links.xlsx"

    # Read the Excel file directly to check its contents
    print("Reading Excel file directly:")
    try:
        df = pd.read_excel(excel_file)
        print(f"Columns in Excel: {df.columns.tolist()}")
        print("\nFirst 5 rows:")
        print(df.head().to_string())
    except Exception as e:
        print(f"Error reading Excel directly: {e}")

    print("\n" + "-"*50 + "\n")

    # Test the read_urls_from_excel function with auto-detection
    print("Testing read_urls_from_excel with auto-detection:")
    try:
        result = read_urls_from_excel(excel_file)
        print(f"Found {len(result)} URLs with departments")

        # Print the first 5 URL-department pairs
        for i, (url, dept) in enumerate(list(result.items())[:5]):
            print(f"{i+1}. URL: {url}")
            print(f"   Department: '{dept}'")
    except Exception as e:
        print(f"Error in read_urls_from_excel: {e}")

    print("\n" + "-"*50 + "\n")

    # Test with explicit column names
    print("Testing read_urls_from_excel with explicit column names:")
    try:
        result = read_urls_from_excel(excel_file, url_column="Profile URL", dept_column="Department")
        print(f"Found {len(result)} URLs with departments")

        # Print the first 5 URL-department pairs
        for i, (url, dept) in enumerate(list(result.items())[:5]):
            print(f"{i+1}. URL: {url}")
            print(f"   Department: '{dept}'")
    except Exception as e:
        print(f"Error in read_urls_from_excel with explicit columns: {e}")

if __name__ == "__main__":
    test_excel_reading()