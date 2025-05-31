from utils.file_loader import load_file
from utils.llm_helper import extract_intent_and_urgency
from agents.email_agent import EmailAgent
from agents.json_agent import JSONAgent
from memory.redis_memory import memory_log

class ClassifierAgent:
    def __init__(self):
        self.email_agent = EmailAgent()
        self.json_agent = JSONAgent()

    def classify_and_route(self, file_path):
        """
        Main pipeline to:
        1. Load and parse the file
        2. Extract format, content, and source
        3. Extract intent and urgency using LLM
        4. Log metadata into Redis memory
        5. Route to appropriate agent based on file format
        """

        try:
            # Load and parse the file
            parsed_data = load_file(file_path)
            file_format = parsed_data["format"]
            content = parsed_data["content"]
            source_name = parsed_data["source_name"]

            # Prepare text for classification based on format
            if file_format == "Email":
                text = content.get("body", "")
            elif file_format == "PDF":
                text = content.get("text", "")
            elif file_format == "JSON":
                text = str(content)
            else:
                raise ValueError(f"Unsupported file format: {file_format}")

            # Extract intent and urgency
            metadata = extract_intent_and_urgency(text)
            intent = metadata.get("intent", "Unknown")
            urgency = metadata.get("urgency", "Unknown")

            # Log metadata to Redis
            doc_id, thread_id = memory_log({
                "source": source_name,
                "format": file_format,
                "intent": intent,
                "urgency": urgency,
            })

            # Route to corresponding agent
            if file_format == "Email":
                return self.email_agent.process_email(content, intent, urgency, doc_id, thread_id)

            elif file_format == "JSON":
                return self.json_agent.process_json(content, intent, doc_id, thread_id)

            elif file_format == "PDF":
                print("[PDF Agent Placeholder] PDF handling not implemented yet.")
                return None

            else:
                raise ValueError(f"Unknown file format during routing: {file_format}")

        except Exception as e:
            print("Error in ClassifierAgent.classify_and_route:", e)
            return {"error": str(e)}
