import json
from utils.llm_helper import extract_structured_json
from memory.redis_memory import memory_log

# Target schema for extracting structured information from raw JSON (can be modifed according to the need)
TARGET_SCHEMA = {
    "document_type": "invoice",
    "document_id": "string",
    "date": "ISO8601",
    "sender": "string",
    "recipient": "string",
    "line_items": [
        {
            "description": "string",
            "quantity": "number",
            "unit_price": "number",
            "total": "number"
        }
    ],
    "total_amount": "number",
}

class JSONAgent:
    """
    JSONAgent processes raw JSON documents to extract structured data using LLM assistance.
    It then logs the normalized data and missing fields into the Redis memory store.
    """

    def process_json(self, parsed_json: dict, intent: str, doc_id: str, thread_id: str):
        """
        Processes a parsed JSON document by:
        - Extracting structured fields using above target schema via LLM
        - Logging the structured data and missing fields to memory (if any)
        - Returning structured result a
        """
        try:
            print(f"[JSONAgent] Processing JSON for doc_id: {doc_id}")

            # LLM-call structure extraction
            result = extract_structured_json(parsed_json, TARGET_SCHEMA)

            # Sanity check for expected structure
            if isinstance(result, dict):
                missing_fields = result.get("missing_fields", [])
                normalized_data = {k: v for k, v in result.items() if k != "missing_fields"}
            else:
                print(f"[JSONAgent] Warning: Unexpected format in LLM result.")
                missing_fields = ["Invalid result format"]
                normalized_data = {}

            # Serialize structured data for logging
            try:
                parsed_data_str = json.dumps(normalized_data)
            except Exception as e:
                print(f"[JSONAgent] Warning: Failed to serialize normalized data: {e}")
                parsed_data_str = "{}"

            document_type = normalized_data.get("document_type", "unknown")

            # Log structured data into Redis memory
            memory_log({
                "type": "JSON",
                "intent": intent,
                "document_type": document_type,
                "parsed_data": parsed_data_str,
                "missing_fields": json.dumps(missing_fields)
            }, doc_id=doc_id, thread_id=thread_id)

            return {
                "normalized_data": normalized_data,
                "missing_fields": missing_fields
            }

        except Exception as e:
            print(f"[JSONAgent] Error while processing JSON: {e}")
            return {"error": str(e)}
