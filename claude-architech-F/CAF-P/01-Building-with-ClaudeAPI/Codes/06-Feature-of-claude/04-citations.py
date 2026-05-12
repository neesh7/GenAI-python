# Citations Demo: Show sources for Claude's answers
import base64
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"


def encode_pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def query_with_citations(pdf_path, query):
    """Query a PDF with citations enabled and display results."""
    pdf_data = encode_pdf_to_base64(pdf_path)

    # Message structure with citations enabled
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data,
                    },
                    "title": "earth.pdf",
                    "citations": {"enabled": True},  # Enable citations
                },
                {
                    "type": "text",
                    "text": query,
                },
            ],
        }
    ]

    # Make API call
    response = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=messages,
    )

    return response


def extract_text_and_citations(response):
    """Extract text and citation information from response."""
    text_content = ""
    citations = []

    for block in response.content:
        if block.type == "text":
            text_content += block.text + "\n"
            # Extract citation information if available
            if hasattr(block, "citations") and block.citations is not None:
                citations.extend(block.citations)

    return text_content.strip(), citations


def display_results(query, text_content, citations):
    """Display query results with formatted citations."""
    print("\n" + "=" * 80)
    print("QUERY:")
    print("=" * 80)
    print(query)

    print("\n" + "=" * 80)
    print("RESPONSE:")
    print("=" * 80)
    print(text_content)

    if citations:
        print("\n" + "=" * 80)
        print(f"CITATIONS ({len(citations)} total):")
        print("=" * 80)
        for i, citation in enumerate(citations, 1):
            print(f"\n[Citation {i}]")
            print(f"  Cited Text: {citation.cited_text}")
            if hasattr(citation, "document_title") and citation.document_title:
                print(f"  Document: {citation.document_title}")
            if hasattr(citation, "start_page_number") and citation.start_page_number:
                end_page = citation.end_page_number if hasattr(citation, "end_page_number") else citation.start_page_number
                print(f"  Pages: {citation.start_page_number}-{end_page}")
            if hasattr(citation, "document_index"):
                print(f"  Document Index: {citation.document_index}")
    else:
        print("\n[No citations found in response]")


if __name__ == "__main__":
    pdf_file = os.path.join(os.path.dirname(__file__), "earth.pdf")

    if not os.path.exists(pdf_file):
        print(f"PDF not found: {pdf_file}")
        exit(1)

    # Single query with citations
    query = "What is Earth's atmosphere composed of and how did it form?"

    print("Querying PDF with citations enabled...")
    response = query_with_citations(pdf_file, query)

    text_content, citations = extract_text_and_citations(response)
    display_results(query, text_content, citations)

    # Show raw response structure for reference
    print("\n" + "=" * 80)
    print("RAW RESPONSE STRUCTURE:")
    print("=" * 80)
    print(f"Stop Reason: {response.stop_reason}")
    print(f"Content blocks: {len(response.content)}")
    for i, block in enumerate(response.content):
        print(f"  Block {i}: type={block.type}")
        if hasattr(block, "citations") and block.citations is not None:
            print(f"    Citations: {len(block.citations)}")
        else:
            print(f"    Citations: None")
