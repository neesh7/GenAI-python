# Code Execution & Files API: Data Analysis with Claude
import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message

load_dotenv()

# Initialize client with code execution and files API beta features
client = Anthropic(
    default_headers={
        "anthropic-beta": "code-execution-2025-08-25, files-api-2025-04-14"
    }
)
model = "claude-sonnet-4-5-20250929"


# Helper functions
def add_user_message(messages, message):
    """Add a user message to the conversation."""
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    """Add an assistant message to the conversation."""
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


def chat(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=[],
    tools=None,
    thinking=False,
    thinking_budget=2000,
):
    """Send a message to Claude with optional tools."""
    params = {
        "model": model,
        "max_tokens": 10000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if thinking:
        params["thinking"] = {
            "type": "enabled",
            "budget_tokens": thinking_budget,
        }

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    return client.messages.create(**params)


def text_from_message(message):
    """Extract text content from a message."""
    return "\n".join([block.text for block in message.content if block.type == "text"])


# Files API functions
def upload(file_path):
    """Upload a file to Claude's Files API."""
    path = Path(file_path)
    extension = path.suffix.lower()

    mime_type_map = {
        ".pdf": "application/pdf",
        ".txt": "text/plain",
        ".md": "text/plain",
        ".py": "text/plain",
        ".js": "text/plain",
        ".html": "text/html",
        ".css": "text/plain",
        ".csv": "text/csv",
        ".json": "application/json",
        ".xml": "application/xml",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls": "application/vnd.ms-excel",
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }

    mime_type = mime_type_map.get(extension)

    if not mime_type:
        raise ValueError(f"Unknown mimetype for extension: {extension}")

    filename = path.name

    with open(file_path, "rb") as file:
        return client.beta.files.upload(file=(filename, file, mime_type))


def list_files():
    """List all uploaded files."""
    return client.beta.files.list()


def delete_file(file_id):
    """Delete a file from Files API."""
    return client.beta.files.delete(file_id)


def download_file(file_id, filename=None):
    """Download a file from Files API."""
    file_content = client.beta.files.download(file_id)

    if not filename:
        file_metadata = get_metadata(file_id)
        file_content.write_to_file(file_metadata.filename)
    else:
        file_content.write_to_file(filename)


def get_metadata(file_id):
    """Get metadata for an uploaded file."""
    return client.beta.files.retrieve_metadata(file_id)


# Code Execution Example
def analyze_data_with_code_execution(file_path):
    """
    Upload a CSV file and have Claude analyze it using code execution.

    Args:
        file_path: Path to the CSV file to analyze

    Returns:
        Claude's analysis response
    """
    # Upload the file
    print(f"Uploading {file_path}...")
    file_metadata = upload(file_path)
    print(f"✓ File uploaded with ID: {file_metadata.id}")

    # Create the analysis request
    messages = []
    add_user_message(
        messages,
        [
            {
                "type": "text",
                "text": """
Run a detailed analysis to determine major drivers of churn.
Your final output should include at least one detailed plot summarizing your findings.

Critical note: Every time you execute code, you're starting with a completely clean slate.
No variables or library imports from previous executions exist. You need to redeclare/reimport all variables/libraries.
                """,
            },
            {
                "type": "container_upload",
                "file_id": file_metadata.id
            },
        ],
    )

    # Send request with code execution tool
    print("Analyzing data with code execution...")
    response = chat(
        messages,
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
    )

    print("✓ Analysis complete")
    return response


def list_and_display_files():
    """List all uploaded files and display their metadata."""
    print("\nListing all uploaded files...")
    files = list_files()

    if not files.data:
        print("No files uploaded yet.")
        return

    for file in files.data:
        print(f"  - {file.filename} (ID: {file.id})")
        print(f"    Size: {file.size_bytes} bytes")
        print(f"    Created: {file.created_at}")


def cleanup_files():
    """Delete all uploaded files."""
    print("\nCleaning up files...")
    files = list_files()

    for file in files.data:
        delete_file(file.id)
        print(f"  ✓ Deleted {file.filename}")


if __name__ == "__main__":
    import sys

    # Example usage
    print("=" * 70)
    print("Claude Code Execution & Files API Demo")
    print("=" * 70)

    # Check if a file path is provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

        if os.path.exists(file_path):
            # Analyze the uploaded file
            response = analyze_data_with_code_execution(file_path)

            # Display response
            print("\n" + "=" * 70)
            print("ANALYSIS RESULTS:")
            print("=" * 70)
            print(text_from_message(response))

            # List files
            list_and_display_files()

            # Optional: Download generated files
            print("\n" + "=" * 70)
            print("GENERATED FILES:")
            print("=" * 70)
            for block in response.content:
                if hasattr(block, "file_id"):
                    print(f"Generated file: {block.file_id}")
                    # download_file(block.file_id, f"output_{block.file_id}.csv")
        else:
            print(f"Error: File not found: {file_path}")
    else:
        print("\nUsage: python 06-code-execution-and-files-api.py <path_to_csv_file>")
        print("\nExample:")
        print("  python 06-code-execution-and-files-api.py data.csv")
        print("\nFunctionality:")
        print("  1. Upload CSV file to Claude's Files API")
        print("  2. Request Claude to analyze it using code execution")
        print("  3. Claude generates plots and insights")
        print("  4. Download generated files (plots, analysis)")

        # Show available files
        list_and_display_files()
