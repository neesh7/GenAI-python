# PDF Document Analysis with Claude
import base64
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"


def add_user_message(messages, content):
    messages.append({
        "role": "user",
        "content": content.content if isinstance(content, Message) else content,
    })


def add_assistant_message(messages, content):
    messages.append({
        "role": "assistant",
        "content": content.content if isinstance(content, Message) else content,
    })


def chat(messages, system=None, temperature=1.0, stop_sequences=[], tools=None, thinking=False, thinking_budget=1024):
    params = {
        "model": model,
        "max_tokens": 4000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }
    if thinking:
        params["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}
    if tools:
        params["tools"] = tools
    if system:
        params["system"] = system
    return client.messages.create(**params)


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])


def encode_pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def send_pdf_message(messages, pdf_path, prompt):
    pdf_data = encode_pdf_to_base64(pdf_path)
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_data,
                },
            },
            {"type": "text", "text": prompt},
        ],
    })


def analyze_pdf(pdf_path, prompt):
    """Analyze a PDF with a custom prompt."""
    messages = []
    send_pdf_message(messages, pdf_path, prompt)
    response = chat(messages)
    return text_from_message(response)


def summarize_pdf(pdf_path):
    """Summarize a PDF document."""
    prompt = """Provide a comprehensive summary including:
1. Main topic
2. Key sections
3. Key findings
4. Important statistics
5. Recommendations"""
    return analyze_pdf(pdf_path, prompt)


def extract_pdf_info(pdf_path):
    """Extract key information from a PDF."""
    prompt = """Extract and organize:
1. Key concepts
2. Data points
3. Main claims
4. Sources/references
5. Technical details"""
    return analyze_pdf(pdf_path, prompt)


def compare_pdfs(pdf_paths, prompt):
    """Compare multiple PDF documents."""
    messages = []
    content = []
    for pdf_path in pdf_paths:
        pdf_data = encode_pdf_to_base64(pdf_path)
        content.append({
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": pdf_data,
            },
        })
    content.append({"type": "text", "text": prompt})
    messages.append({"role": "user", "content": content})
    response = chat(messages)
    return text_from_message(response)


def pdf_qa_conversation(pdf_path, questions):
    """Multi-turn Q&A conversation about a PDF."""
    messages = []
    send_pdf_message(messages, pdf_path, "Ready to answer questions about this document.")
    chat(messages)  # Acknowledge receipt

    results = []
    for question in questions:
        add_user_message(messages, question)
        response = chat(messages)
        answer = text_from_message(response)
        results.append(f"Q: {question}\nA: {answer}")
        add_assistant_message(messages, response)
    return results


if __name__ == "__main__":
    pdf_file = os.path.join(os.path.dirname(__file__), "earth.pdf")

    if not os.path.exists(pdf_file):
        print(f"PDF not found: {pdf_file}")
        exit(1)

    print("1. Summarizing PDF...")
    print(summarize_pdf(pdf_file))

    print("\n" + "="*70 + "\n")

    print("2. Extracting key information...")
    print(extract_pdf_info(pdf_file))

    print("\n" + "="*70 + "\n")

    print("3. Multi-turn Q&A...")
    questions = [
        "What is the main topic?",
        "What are the key findings?",
        "What actions are recommended?",
    ]
    for result in pdf_qa_conversation(pdf_file, questions):
        print(result)
