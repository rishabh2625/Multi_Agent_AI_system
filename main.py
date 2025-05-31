import sys
from agents.classifier_agent import ClassifierAgent

def run(file_path: str):
    """
    Initialize the ClassifierAgent and process the given file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        None
    """
    try:
        agent = ClassifierAgent()
        output = agent.classify_and_route(file_path)

        print("\n=== Final Output ===")
        print(output)
        
    except Exception as e:
        print(f"[Error] Failed to process file '{file_path}': {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_file>")
    else:
        run(sys.argv[1])
