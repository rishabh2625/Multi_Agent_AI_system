# Multi-Agent Email & JSON Intelligence System

This is a multi-agent system that accepts email (.eml) files or JSON files, extracts structured and useful information from them using LLMs, and logs everything into a Redis-based memory system.

## Features

- **Classifier Agent**: Routes incoming documents (emails or JSON) to the correct processing agent
- **Email Agent**: Extracts metadata and summaries from emails
- **JSON Agent**: Uses an LLM to normalize unstructured JSON into a predefined schema (e.g., invoice format)
- **Redis Memory**: All results are stored and organized by document and thread in Redis

## Installation & Setup

### 1. Clone the repository
```bash
git clone <url>

```
OR
If using VSCode use command pallate (By CTRL + SHIFT + P ) then type git -> select git:clone -> paste the url of repo -> select forlder and ENTER.

### 2. Install dependencies
Make sure you're in a virtual environment, then run:
```bash
pip install -r requirements.txt
```

### 3. Set up Redis server
- **Recommended**: Use WSL (Windows Subsystem for Linux) if on Windows
- Alternatively, you can install Redis using [official Redis installation docs](https://redis.io/docs/getting-started/installation/)
- Run the server and in the config add the port, host and database
- Then add your `OPENAI_API_KEY` in the `config.py`

## Running the System

### 1. Test with a JSON file
```bash
python main.py sample_inputs/tes_json.json
```

### 2. Test with an email file
```bash
python main.py sample_inputs/test_email.eml
```

The system will:
- Print extracted structured output in the terminal
- Log documents and threads in Redis (with `doc:<id>` and `thread:<id>` format)

## Debug & Monitoring

You can inspect stored documents via:
- **RedisInsight GUI** (recommended)

## Requirements

Check `requirements.txt` — includes:
- `redis` — Redis client for Python
- `PyMuPDF (fitz)` — for PDF/EML parsing
- `openai` — for LLM-based JSON extraction

## Project Structure

```
project/
├── agents/
│   ├── classifier_agent.py
│   ├── email_agent.py
│   └── json_agent.py
├── memory/
│   └── redis_memory.py
├── utils/
│   ├── file_loader.py
│   └── llm_helper.py
|
├── sample_inputs/
│   ├── tes_json.json
│   └── test_email.eml
├── output_samples/
│   ├── screenshots
|   |   └──(screenshots of output)
|   └── Demo.mp4
├── config.py
├── main.py
├── README.md
└── requirements.txt

```

## Output Samples

The folder `output_samples/` contains screenshots,demo video and sample outputs of:
- Terminal logs showing extracted information
- RedisInsight views of stored documents and threads

This folder helps in verifying the system's functionality visually.

## Notes

- Make sure Redis server is running before executing `main.py`
- `main.py` automatically detects the input file type (email or JSON) and routes accordingly
- The system can be extended with new agents  (e.g., PDFAgent) by plugging into the same interface.
- The classifier agent can be extended to take one ,ore input thread_id to add conversation of a particular thread
  for easy access with some modification and simple logic

