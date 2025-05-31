from openai import OpenAI
import json
from config import OPENAI_API_KEY

# Initialize OpenAI client with API key from config
client = OpenAI(api_key=OPENAI_API_KEY)


def extract_intent_and_urgency(text):
    """
    Uses LLM to classify the given message into business intent and urgency levels.

    Parameters:
        text (str): The raw message text or str (from json) input .

    Returns:
        dict: A dictionary with keys:
              - "intent" → one of ["RFQ", "Invoice", "Complaint", "Regulation", "General", "Other"]
              - "urgency" → one of ["High", "Medium", "Low"]
              If parsing fails, both are set to "Unknown".
    """
    messages = [
        {"role": "system", "content": "You are an intelligent assistant for business communication processing."},
        {"role": "user", "content": f"""
Classify the following message by:
1. Intent → one of ["RFQ", "Invoice", "Complaint", "Regulation", "General", "Other"]
2. Urgency → one of ["High", "Medium", "Low"]

Text:
\"\"\"{text}\"\"\"

Respond in the following JSON format:
{{
  "intent": "Invoice",
  "urgency": "High"
}}
"""}
    ]

    try:
        # Call the GPT-4o model to classify the message
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0  
        )

        content = response.choices[0].message.content.strip()

        # Debug log: print raw model output
        print("Raw LLM response:", repr(content))

        # Handle JSON
        if content.startswith("```json"):
            content = content.removeprefix("```json").removesuffix("```").strip()
        elif content.startswith("```"):
            content = content.removeprefix("```").removesuffix("```").strip()

        return json.loads(content)

    except Exception as e:
        # Log error and return default fallback
        print("Error in extract_intent_and_urgency:", e)
        return {"intent": "Unknown", "urgency": "Unknown"}


def extract_structured_json(raw_json: dict, target_schema: dict) -> dict:
    """
    Uses LLM to convert a raw JSON dictionary into a structured format defined by the target schema.

    Parameters:
        raw_json (dict): The input data to be normalized.
        target_schema (dict): The desired structure and field names.

    Returns:
        dict: A dictionary containing:
              - "data": JSON data mapped to target schema
              - "missing_fields": A list of fields not found in the raw JSON
                or ["LLM parsing error"] if transformation fails.
    """
    messages = [
        {"role": "system", "content": "You are a business document parser."},
        {"role": "user", "content": f"""
Your job is to convert the input JSON below into the target schema format.
If any fields cannot be matched, add a "missing_fields" list in the response.

TARGET SCHEMA:
{json.dumps(target_schema, indent=2)}

INPUT JSON:
{json.dumps(raw_json, indent=2)}

Return ONLY a valid JSON object with the normalized data and (if needed) a "missing_fields" array.
"""}
    ]

    try:
        # Call GPT-4o model to normalize the JSON
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # Debug log: print raw model output
        print("the extracted content from the api for JSON WALA SCHEMA TOOL ...................................")
        print(content)
        print("....................................................................")

        # Handle possible markdown-wrapped JSON
        if content.startswith("```json"):
            content = content.removeprefix("```json").removesuffix("```").strip()
        elif content.startswith("```"):
            content = content.removeprefix("```").removesuffix("```").strip()

        return json.loads(content)

    except Exception as e:
        # Log error and return fallback result with error flag
        print("Error in extract_structured_json:", e)
        return {
            "data": {},
            "missing_fields": ["LLM parsing error"]
        }