"""
Parser for extracting structured data from researcher profile markdown.
"""
import re
import json
import os
import logging
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

    def extract_researcher_id(self, markdown: str) -> str:
        """
        Extract the researcher ID from the markdown content.

        Args:
            markdown (str): The markdown content

        Returns:
            str: The researcher ID
        """
        match = re.search(self.section_patterns['perid'], markdown)
        if match:
            return match.group(1)
        return "unknown"

    def extract_name(self, markdown: str) -> str:
        """
        Extract the researcher's name from the markdown content.

        Args:
            markdown (str): The markdown content

        Returns:
            str: The researcher's name
        """
        match = re.search(self.section_patterns['name'], markdown)
        if match:
            # Clean up name (remove degrees)
            name = match.group(1)
            name = re.sub(r',?\s*(?:MD|PhD|M\.D\.|Ph\.D\.)*$', '', name)
            return name.strip()
        return "Unknown Researcher"

    def extract_degrees(self, markdown: str) -> List[str]:
        """
        Extract the researcher's degrees from the markdown content.

        Args:
            markdown (str): The markdown content

        Returns:
            List[str]: The researcher's degrees
        """
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
        education_match = re.search(self.section_patterns['education'], markdown, re.DOTALL)
        if education_match:
            education_text = education_match.group(1)
            if "M.D." in education_text or "MD" in education_text:
                if "MD" not in degrees:
                    degrees.append("MD")
            if "Ph.D." in education_text or "PhD" in education_text:
                if "PhD" not in degrees:
                    degrees.append("PhD")

        return degrees

    def extract_title_and_programs(self, markdown: str) -> Dict[str, str]:
        """
        Extract the researcher's title and program affiliations.

        Args:
            markdown (str): The markdown content

        Returns:
            Dict[str, str]: Dictionary with title, primary_program, and research_program
        """
        result = {
            "title": "",
            "primary_program": "",
            "research_program": ""
        }

        # Find the section after the name and before the overview
        name_match = re.search(self.section_patterns['name'], markdown)
        overview_match = re.search(r'##\s+Overview', markdown)

        if name_match and overview_match:
            start_pos = name_match.end()
            end_pos = overview_match.start()
            title_section = markdown[start_pos:end_pos]

            # Look for title
            title_match = re.search(self.section_patterns['title_program'], title_section)
            if title_match:
                # Extract the whole line with the title
                title_line = re.search(r'(.*' + self.section_patterns['title_program'] + '.*)\n', title_section)
                if title_line:
                    result["title"] = title_line.group(1).strip()

            # Look for program affiliations
            program_matches = re.findall(r'\*\*Program:\*\*\s+(.*?)\n', title_section)
            if program_matches:
                primary_program = program_matches[0].strip()
                # Remove " Program" suffix if present
                if primary_program.endswith(' Program'):
                    primary_program = primary_program[:-8].strip()
                # Convert to lowercase
                result["primary_program"] = primary_program.lower()

            research_program_matches = re.findall(r'\*\*Research Program:\*\*\s+(.*?)\n', title_section)
            if research_program_matches:
                research_program = research_program_matches[0].strip()
                # Remove " Program" suffix if present (can be comma-separated list)
                # Split by comma, clean each, and rejoin
                programs = [p.strip() for p in research_program.split(',')]
                cleaned_programs = []
                for prog in programs:
                    if prog.endswith(' Program'):
                        prog = prog[:-8].strip()
                    cleaned_programs.append(prog.lower())  # Convert to lowercase
                result["research_program"] = ', '.join(cleaned_programs)

        return result

    def extract_overview(self, markdown: str) -> str:
        """
        Extract the researcher's overview/biography.

        Args:
            markdown (str): The markdown content

        Returns:
            str: The overview text
        """
        match = re.search(self.section_patterns['overview'], markdown, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    def extract_research_interests(self, markdown: str) -> List[str]:
        """
        Extract the researcher's research interests.

        Args:
            markdown (str): The markdown content

        Returns:
            List[str]: The research interests
        """
        interests = []

        # First try to find a Research Interest section
        match = re.search(self.section_patterns['research_interests'], markdown, re.DOTALL)
        if match:
            interests_text = match.group(1)
            # Return the whole paragraph for now
            return [interests_text.strip()]

        # If no specific section, look for Associations section which often contains interests
        associations = self.extract_associations(markdown)
        if associations:
            return associations

        return interests

    def extract_associations(self, markdown: str) -> List[str]:
        """
        Extract the researcher's associations/interests from the Associations section.

        Args:
            markdown (str): The markdown content

        Returns:
            List[str]: The associations
        """
        associations = []

        # Look for the Associations section
        match = re.search(self.section_patterns['associations'], markdown, re.DOTALL)
        if match:
            associations_text = match.group(1)

            # Extract bullet points if they exist
            bullet_points = re.findall(r'\s*\*\s+(.*?)\n', associations_text)
            if bullet_points:
                associations = [point.strip() for point in bullet_points]
            else:
                # If no bullet points, use the whole text
                associations = [associations_text.strip()]

        return associations

    def extract_education(self, markdown: str) -> List[Dict[str, str]]:
        """
        Extract the researcher's education and training.

        Args:
            markdown (str): The markdown content

        Returns:
            List[Dict[str, str]]: Education entries
        """
        education = []

        match = re.search(self.section_patterns['education'], markdown, re.DOTALL)
        if match:
            education_text = match.group(1)

            # Parse different education types
            education_types = ["Graduate", "Medical School", "Internship", "Residency", "Fellowship", "Board Certification"]

            for edu_type in education_types:
                type_match = re.search(r'\*\*' + edu_type + ':\*\*\n(.*?)(?=\*\*|\Z)', education_text, re.DOTALL)
                if type_match:
                    entries_text = type_match.group(1)
                    entries = re.findall(r'\s*\*\s+(.*?)\n', entries_text)

                    for entry in entries:
                        education_entry = {"type": edu_type}

                        # Try to parse institution and details
                        parts = entry.split(' - ', 1)
                        if len(parts) > 0:
                            education_entry["institution"] = parts[0].strip()

                        if len(parts) > 1:
                            # Further parse details depending on education type
                            details = parts[1].strip()

                            # For graduate and medical school, look for degree
                            if edu_type in ["Graduate", "Medical School"]:
                                degree_match = re.search(r'(M\.D\.|Ph\.D\.|MD|PhD|MS|MPH|MBA)', details)
                                if degree_match:
                                    education_entry["degree"] = degree_match.group(1)

                                    # Check for field of study
                                    field_match = re.search(r'(?:M\.D\.|Ph\.D\.|MD|PhD|MS|MPH|MBA)\s*-?\s*(.*)', details)
                                    if field_match and field_match.group(1).strip():
                                        education_entry["field"] = field_match.group(1).strip()

                            # For internship, residency, fellowship
                            elif edu_type in ["Internship", "Residency", "Fellowship"]:
                                # Check if position is specified (Intern, Resident, etc.)
                                position_match = re.search(r'(Intern|Resident|Fellow|Post-doctoral Fellow)', details)
                                if position_match:
                                    education_entry["position"] = position_match.group(1)
                                    # Specialty would be after position
                                    specialty_match = re.search(r'(?:Intern|Resident|Fellow|Post-doctoral Fellow)\s*-?\s*(.*)', details)
                                    if specialty_match and specialty_match.group(1).strip():
                                        education_entry["specialty"] = specialty_match.group(1).strip()
                                else:
                                    # Assume everything is specialty
                                    education_entry["specialty"] = details

                            # For board certification
                            elif edu_type == "Board Certification":
                                education_entry["certification"] = details

                        education.append(education_entry)

        return education

    def extract_publications(self, markdown: str) -> List[Dict[str, str]]:
        """
        Extract the researcher's publications.

        Args:
            markdown (str): The markdown content

        Returns:
            List[Dict[str, str]]: Publication entries
        """
        publications = []

        match = re.search(self.section_patterns['publications'], markdown, re.DOTALL)
        if match:
            publications_text = match.group(1)

            # Each publication typically starts with a bullet point
            pub_entries = re.findall(r'\s*\*\s+(.*?)(?=\s*\*\s+|\Z)', publications_text, re.DOTALL)

            for entry in pub_entries:
                pub = {"title": ""}

                # Extract title and other details
                # Publications often have format: Authors. Title. Journal. Year.
                entry = entry.strip()

                # Extract PubMed ID if available
                pubmed_match = re.search(r'Pubmedid:\s*\[(.*?)\]', entry)
                if pubmed_match:
                    pub["pubmed_id"] = pubmed_match.group(1)

                # Extract PMC ID if available
                pmc_match = re.search(r'Pmcid:\s*(PMC\d+)', entry)
                if pmc_match:
                    pub["pmc_id"] = pmc_match.group(1)

                # Extract year and publication date information
                year_match = re.search(r'(\d{4})\s+(\w+)\.', entry)
                if year_match:
                    pub["year"] = year_match.group(1)
                    pub["publication_date"] = f"{year_match.group(1)} {year_match.group(2)}"
                else:
                    # Try alternative year format (just the year)
                    alt_year_match = re.search(r'(\d{4})\.', entry)
                    if alt_year_match:
                        pub["year"] = alt_year_match.group(1)

                # We will handle journal extraction in the title/author section
                # This section is no longer needed as we extract the journal alongside authors and title

                # Extract authors, title, and journal (everything before the year)
                if year_match:
                    citation_text = entry[:year_match.start()].strip()

                    # Find all periods that separate major components
                    periods = [m.start() for m in re.finditer(r'\.', citation_text)]

                    if len(periods) >= 2:  # We have at least two periods (Authors. Title. Journal)
                        # First period separates authors from title
                        first_period = periods[0]
                        # Second period separates title from journal
                        second_period = periods[1]

                        # Extract authors (text before first period)
                        pub["authors"] = citation_text[:first_period].strip()

                        # Extract title (text between first and second period)
                        pub["title"] = citation_text[first_period+1:second_period].strip()

                        # Extract journal (text after second period until end or next period)
                        journal_text = ""
                        if len(periods) > 2:
                            journal_text = citation_text[second_period+1:periods[2]].strip()
                        else:
                            journal_text = citation_text[second_period+1:].strip()

                        # Clean up journal to separate actual journal name from volume/issue info
                        # Journal format is usually: "Journal Name" or "Journal Name Volume(Issue)"
                        journal_parts = re.match(r'([^0-9]+)(\s+\d+\(.*\))?', journal_text)
                        if journal_parts:
                            pub["journal"] = journal_parts.group(1).strip()
                            if journal_parts.group(2):
                                pub["journal_details"] = journal_parts.group(2).strip()

                    elif len(periods) == 1:  # Only one period (possibly Authors. Title/Journal)
                        first_period = periods[0]
                        pub["authors"] = citation_text[:first_period].strip()
                        pub["title"] = citation_text[first_period+1:].strip()

                    else:  # No periods found
                        # If we can't parse correctly, use the whole text as title
                        pub["title"] = citation_text
                        pub["authors"] = ""
                else:
                    # If no year found, use the whole entry as title
                    pub["title"] = entry
                    pub["authors"] = ""

                publications.append(pub)

        return publications

    def extract_photo_url(self, markdown: str) -> str:
        """
        Extract the researcher's photo URL if available.

        Args:
            markdown (str): The markdown content

        Returns:
            str: The photo URL
        """
        # Look for image after the name header
        name_match = re.search(self.section_patterns['name'], markdown)
        if name_match:
            # Look for image markdown format after name
            img_match = re.search(r'!\[(.*?)\]\((.*?)\)', markdown[name_match.end():name_match.end()+500])
            if img_match:
                return img_match.group(2)
        return ""

    def extract_contact_info(self, markdown: str) -> Dict[str, str]:
        """
        Extract the researcher's contact information.

        Args:
            markdown (str): The markdown content

        Returns:
            Dict[str, str]: Contact information
        """
        contact = {}

        # Look for contact link
        contact_match = re.search(r'\[\s*Contact\s*\]\s*\((.*?)\)', markdown)
        if contact_match:
            contact["contact_url"] = contact_match.group(1)

        # Look for email (rarely directly provided)
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', markdown)
        if email_match:
            contact["email"] = email_match.group(0)

        return contact

    def extract_grants(self, markdown: str) -> List[Dict[str, str]]:
        """
        Extract the researcher's grants information.

        Args:
            markdown (str): The markdown content

        Returns:
            List[Dict[str, str]]: Grants information
        """
        grants = []

        # Look for the Grants section
        match = re.search(self.section_patterns['grants'], markdown, re.DOTALL)
        if match:
            grants_text = match.group(1)

            # Extract individual grant entries (typically bullet points)
            grant_entries = re.findall(r'\s*\*\s+(.*?)(?=\s*\*\s+|\Z)', grants_text, re.DOTALL)

            for entry in grant_entries:
                # Keep the full entry as description for backwards compatibility
                grant = {"description": entry.strip()}

                # Extract title using the Title: prefix
                title_match = re.search(r'Title:\s*(.*?)(?=\s*Award Number:|$)', entry, re.DOTALL)
                if title_match:
                    grant["title"] = title_match.group(1).strip()

                # Extract award number using the Award Number: prefix
                award_match = re.search(r'Award Number:\s*(.*?)(?=\s*Sponsor:|$)', entry, re.DOTALL)
                if award_match:
                    award_number = award_match.group(1).strip()
                    if award_number != "N/A":  # Skip N/A values
                        grant["award_number"] = award_number

                        # For backward compatibility, also keep the id field if it looks like a standard grant ID
                        standard_id_match = re.search(r'([A-Z]\d+\s+[A-Z]{2}\d+)', award_number)
                        if standard_id_match:
                            grant["id"] = standard_id_match.group(1)

                # Extract sponsor information
                sponsor_match = re.search(r'Sponsor:\s*(.*?)(?=\s*\w+,\s*\w\.|\Z)', entry, re.DOTALL)
                if sponsor_match:
                    grant["sponsor"] = sponsor_match.group(1).strip()

                    # For backward compatibility, also keep the source field
                    funding_sources = ["NIH", "NCI", "NSF", "DOD", "American Cancer Society",
                                       "DOE", "DARPA", "CDC", "Foundation"]
                    for source in funding_sources:
                        if source in grant["sponsor"]:
                            grant["source"] = source
                            break

                # Extract investigator information
                investigators_match = re.search(r'Sponsor:.*?\n(.*?)$', entry, re.DOTALL)
                if investigators_match:
                    investigators_text = investigators_match.group(1).strip()
                    if investigators_text:
                        # Extract all investigators with roles
                        investigators = []
                        for inv_match in re.finditer(r'(\w+,\s*\w\.)\s*\((.*?)\)', investigators_text):
                            investigators.append({
                                "name": inv_match.group(1).strip(),
                                "role": inv_match.group(2).strip()
                            })
                        if investigators:
                            grant["investigators"] = investigators

                # Keep existing extraction for amount
                amount_match = re.search(r'\$\s*([\d,]+)', entry)
                if amount_match:
                    grant["amount"] = amount_match.group(1)

                # Improved period extraction that avoids matching on grant numbers
                # Look for explicit period mentions
                period_match = re.search(r'Period:\s*(\d{4}-\d{4}|\d{4}-\d{2})', entry)
                if period_match:
                    grant["period"] = period_match.group(1)

                grants.append(grant)

        return grants

    def parse_markdown(self, markdown: str, profile_url: str) -> Dict[str, Any]:
        """
        Parse markdown content into a structured researcher profile.

        Args:
            markdown (str): The markdown content
            profile_url (str): The URL of the profile

        Returns:
            Dict[str, Any]: Structured researcher data
        """
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

        # Extract associations (may overlap with interests but keeping separate for completeness)
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

    def parse_markdown_file(self, file_path: str, profile_url: str = "") -> Dict[str, Any]:
        """
        Parse a markdown file into a structured researcher profile.

        Args:
            file_path (str): Path to the markdown file
            profile_url (str, optional): The URL of the profile

        Returns:
            Dict[str, Any]: Structured researcher data
        """
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


def parse_researcher_profile(markdown_path: str, profile_url: str = "") -> Dict[str, Any]:
    """
    Convenience function to parse a researcher profile from a markdown file.

    Args:
        markdown_path (str): Path to the markdown file
        profile_url (str, optional): The URL of the profile

    Returns:
        Dict[str, Any]: Structured researcher data
    """
    parser = ResearcherProfileParser()
    return parser.parse_markdown_file(markdown_path, profile_url)


if __name__ == "__main__":
    # Test with sample file
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        result = parse_researcher_profile(file_path)
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python parse.py <markdown_file_path>")