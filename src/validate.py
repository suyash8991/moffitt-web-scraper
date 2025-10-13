"""
Schema validation for researcher profiles.
"""
import json
import os
import hashlib
from datetime import datetime
import jsonschema


def load_schema(schema_path):
    """
    Load the JSON schema from the given path.

    Args:
        schema_path (str): Path to the schema file

    Returns:
        dict: The loaded schema
    """
    with open(schema_path, 'r') as f:
        return json.load(f)


def generate_content_hash(content):
    """
    Generate a hash of the content for change detection.

    Args:
        content (str): The content to hash

    Returns:
        str: The hash of the content
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def validate_researcher(data, schema=None):
    """
    Validate a researcher profile against the schema.

    Args:
        data (dict): The researcher profile data
        schema (dict, optional): The schema to validate against.
                                If None, the default schema is loaded.

    Returns:
        tuple: (is_valid, errors) where is_valid is a boolean and errors is a list
    """
    if schema is None:
        schema_path = os.path.join('schemas', 'researcher.json')
        schema = load_schema(schema_path)

    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, []
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)


def prepare_researcher_data(raw_data, profile_url):
    """
    Prepare researcher data for validation by adding required fields.

    Args:
        raw_data (dict): The raw researcher data
        profile_url (str): The profile URL

    Returns:
        dict: The prepared researcher data
    """
    # Generate a unique ID from the name or URL
    if 'name' in raw_data and raw_data['name']:
        researcher_id = raw_data['name'].lower().replace(' ', '-')
    else:
        # Extract from URL as fallback
        path_parts = profile_url.rstrip('/').split('/')
        researcher_id = path_parts[-1] if path_parts else 'unknown'

    # Generate content hash from raw data
    content_str = json.dumps(raw_data, sort_keys=True)
    content_hash = generate_content_hash(content_str)

    # Add required fields
    prepared_data = {
        **raw_data,
        'researcher_id': researcher_id,
        'profile_url': profile_url,
        'content_hash': content_hash,
        'last_updated': datetime.utcnow().isoformat()
    }

    return prepared_data