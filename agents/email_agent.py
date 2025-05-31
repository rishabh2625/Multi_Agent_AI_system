from memory.redis_memory import memory_log

class EmailAgent:
    """
    EmailAgent handles parsing of email data, structuring it into a CRM-friendly payload,
    and logging both raw and structured results into Redis memory.
    """

    def process_email(self, email_data: dict, intent: str, urgency: str, doc_id: str, thread_id: str):
        """
        Processes parsed email content:
        - Extracts relevant fields
        - Constructs a CRM payload
        - Logs structured output to memory under the same doc/thread ID
        - Returns the structured response
        """
        try:
            sender = email_data.get("from", "unknown")
            print(f"[EmailAgent] Processing email from: {sender}")

            crm_payload = {
                "contact_email": sender,
                "interaction_type": intent,
                "priority": urgency,
                "summary": self._generate_summary(email_data)
            }

            final_output = {
                "from": sender,
                "to": email_data.get("to", "unknown"),
                "subject": email_data.get("subject", "No Subject"),
                "date": email_data.get("date", "Unknown Date"),
                "body": email_data.get("body", ""),
                "intent": intent,
                "urgency": urgency,
                "crm_payload": crm_payload
            }

            # Append structured data and payload to memory
            memory_log({
                "structured_data": final_output,
                "crm_payload": crm_payload
            }, doc_id=doc_id, thread_id=thread_id)

            return final_output

        except Exception as e:
            print(f"[EmailAgent] Error while processing email: {e}")
            return {"error": str(e)}

    def _generate_summary(self, email_data: dict) -> str:
        """
        Generates a short summary from subject and sender.
        """
        subject = email_data.get("subject", "No Subject")
        sender = email_data.get("from", "Unknown Sender")
        return f"{subject} from {sender}"
