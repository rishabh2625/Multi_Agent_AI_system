import os
import json
import fitz  # PyMuPDF library for reading PDF files
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime

def detect_format(file_path):
    """
    Detects the format of the given file based on its extension.

    Parameters:
        file_path (str): Path to the file.

    Returns:
        str: Detected format - "JSON", "Email", "PDF", or "Unknown".
    """
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".json":
        return "JSON"
    elif ext == ".eml":
        return "Email"
    elif ext == ".pdf":
        return "PDF"
    else:
        return "Unknown"


def parse_json(file_path):
    """
    Parses the contents of a JSON file.

    Parameters:
        file_path (str): Path to the JSON file.

    Returns:
        dict or list: Parsed JSON object or list of objects.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            # Try parsing as a standard JSON object or array
            return json.load(f)
        except json.JSONDecodeError:
            # Fallback: parse line-delimited JSON
            f.seek(0)
            return [json.loads(line) for line in f if line.strip()]


def parse_email(file_path):
    """
    Parses an email (.eml) file and extracts relevant fields.

    Parameters:
        file_path (str): Path to the EML file.

    Returns:
        dict: Parsed email content including sender, receiver, subject, date, and body.
    """
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    # Extract and parse the email's date field
    raw_date = msg["date"]
    parsed_date = parsedate_to_datetime(raw_date) if raw_date else None

    return {
        "from": msg["from"],
        "to": msg["to"],
        "subject": msg["subject"],
        "date": parsed_date.isoformat() if parsed_date else None,
        "body": msg.get_body(preferencelist=('plain', 'html')).get_content()
                if msg.get_body() else msg.get_payload()
    }


def parse_pdf(file_path):
    """
    Extracts text from a PDF file using PyMuPDF (fitz).

    Parameters:
        file_path (str): Path to the PDF file.

    Returns:
        dict: A dictionary containing all the extracted text under the key "text".
    """
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            # Append text from each page
            text += page.get_text()
    return {
        "text": text
    }


def load_file(file_path):
    """
    Loads and parses a file based on its detected format.

    Parameters:
        file_path (str): Path to the file.

    Returns:
        dict: A dictionary with:
            - "format": Detected file format (JSON, Email, PDF),
            - "content": Parsed file content,
            - "source_name": Name of the source file.
    """
    # Detect the file format
    file_format = detect_format(file_path)

    # Extract the file name
    source_name = os.path.basename(file_path)

    # Parse the file content based on its format
    if file_format == "JSON":
        content = parse_json(file_path)
    elif file_format == "Email":
        content = parse_email(file_path)
    elif file_format == "PDF":
        content = parse_pdf(file_path)
    else:
        # Raise an error for unsupported formats
        raise ValueError(f"Unsupported file format for: {file_path}")

    return {
        "format": file_format,
        "content": content,
        "source_name": source_name
    }