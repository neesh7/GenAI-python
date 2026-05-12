# Vision Capability: Analyze images with Claude
import base64
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"


# Helper functions
def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
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
    thinking_budget=1024,
):
    params = {
        "model": model,
        "max_tokens": 4000,
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

    message = client.messages.create(**params)
    return message


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])


def encode_image_to_base64(image_path):
    """Read an image file and encode it to base64."""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def get_image_media_type(image_path):
    """Determine media type based on file extension."""
    ext = os.path.splitext(image_path)[1].lower()
    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return media_types.get(ext, "image/jpeg")


def send_image_message(messages, image_path, text_prompt):
    """
    Add an image and text prompt to the message list.

    Args:
        messages: List of message dicts
        image_path: Path to the image file
        text_prompt: Text prompt to accompany the image
    """
    image_data = encode_image_to_base64(image_path)
    media_type = get_image_media_type(image_path)

    user_message = {
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_data,
                },
            },
            {
                "type": "text",
                "text": text_prompt,
            },
        ],
    }
    messages.append(user_message)


def send_image_url_message(messages, image_url, text_prompt):
    """
    Add an image URL and text prompt to the message list.

    Args:
        messages: List of message dicts
        image_url: URL of the image
        text_prompt: Text prompt to accompany the image
    """
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": image_url,
                },
            },
            {
                "type": "text",
                "text": text_prompt,
            },
        ],
    }
    messages.append(user_message)


# Fire Risk Assessment Prompt
fire_risk_prompt = """
Analyze the attached satellite image of a property with these specific steps:

1. Residence identification: Locate the primary residence on the property by looking for:
   - The largest roofed structure
   - Typical residential features (driveway connection, regular geometry)
   - Distinction from other structures (garages, sheds, pools)
   Describe the residence's location relative to property boundaries and other features.

2. Tree overhang analysis: Examine all trees near the primary residence:
   - Identify any trees whose canopy extends directly over any portion of the roof
   - Estimate the percentage of roof covered by overhanging branches (0-25%, 25-50%, 50-75%, 75-100%)
   - Note particularly dense areas of overhang

3. Fire risk assessment: For any overhanging trees, evaluate:
   - Potential wildfire vulnerability (ember catch points, continuous fuel paths to structure)
   - Proximity to chimneys, vents, or other roof openings if visible
   - Areas where branches create a "bridge" between wildland vegetation and the structure

4. Defensible space identification: Assess the property's overall vegetative structure:
   - Identify if trees connect to form a continuous canopy over or near the home
   - Note any obvious fuel ladders (vegetation that can carry fire from ground to tree to roof)

5. Fire risk rating: Based on your analysis, assign a Fire Risk Rating from 1-4:
   - Rating 1 (Low Risk): No tree branches overhanging the roof, good defensible space around the structure
   - Rating 2 (Moderate Risk): Minimal overhang (<25% of roof), some separation between tree canopies
   - Rating 3 (High Risk): Significant overhang (25-50% of roof), connected tree canopies, multiple points of vulnerability
   - Rating 4 (Severe Risk): Extensive overhang (>50% of roof), dense vegetation against structure, numerous ember catch points, limited defensible space

For each item above (1-5), write one sentence summarizing your findings, with your final response being the numeric Fire Risk Rating (1-4) with a brief justification.
"""


# Example: Analyze an image from file
def analyze_fire_risk_from_file(image_path):
    """
    Analyze fire risk from a satellite image file.

    Args:
        image_path: Path to the satellite image file
    """
    messages = []
    send_image_message(messages, image_path, fire_risk_prompt)

    response = chat(messages)
    return text_from_message(response)


# Example: Analyze an image from URL
def analyze_fire_risk_from_url(image_url):
    """
    Analyze fire risk from a satellite image URL.

    Args:
        image_url: URL of the satellite image
    """
    messages = []
    send_image_url_message(messages, image_url, fire_risk_prompt)

    response = chat(messages)
    return text_from_message(response)


# Example: Simple image analysis
def simple_image_analysis(image_path, prompt):
    """
    Perform a simple analysis on an image.

    Args:
        image_path: Path to the image file
        prompt: Analysis prompt
    """
    messages = []
    send_image_message(messages, image_path, prompt)

    response = chat(messages)
    return text_from_message(response)


# Example: Multi-image comparison
def compare_multiple_images(image_paths, prompt):
    """
    Compare multiple images with a single prompt.

    Args:
        image_paths: List of image file paths
        prompt: Comparison prompt
    """
    messages = []

    content = []
    for image_path in image_paths:
        image_data = encode_image_to_base64(image_path)
        media_type = get_image_media_type(image_path)

        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": image_data,
            },
        })

    content.append({
        "type": "text",
        "text": prompt,
    })

    user_message = {
        "role": "user",
        "content": content,
    }
    messages.append(user_message)

    response = chat(messages)
    return text_from_message(response)


if __name__ == "__main__":
    # Base directory for images
    images_dir = os.path.join(
        os.path.dirname(__file__), "images"
    )

    # Example 1: Analyze a single property for fire risk
    print("=" * 60)
    print("EXAMPLE 1: Fire Risk Assessment for Property 1")
    print("=" * 60)
    prop1_path = os.path.join(images_dir, "prop1.png")
    if os.path.exists(prop1_path):
        result = analyze_fire_risk_from_file(prop1_path)
        print(result)
    else:
        print(f"Image not found: {prop1_path}")

    print("\n")

    # Example 2: Simple image description
    print("=" * 60)
    print("EXAMPLE 2: Simple Image Analysis")
    print("=" * 60)
    prop2_path = os.path.join(images_dir, "prop2.png")
    if os.path.exists(prop2_path):
        simple_prompt = "Describe the key features you see in this satellite image. Focus on the vegetation, structures, and overall landscape."
        result = simple_image_analysis(prop2_path, simple_prompt)
        print(result)
    else:
        print(f"Image not found: {prop2_path}")

    print("\n")

    # Example 3: Compare two properties
    print("=" * 60)
    print("EXAMPLE 3: Compare Two Properties")
    print("=" * 60)
    prop3_path = os.path.join(images_dir, "prop3.png")
    prop4_path = os.path.join(images_dir, "prop4.png")
    if os.path.exists(prop3_path) and os.path.exists(prop4_path):
        comparison_prompt = "Compare these two satellite images. Which property appears to have higher fire risk based on vegetation and tree placement? Why?"
        result = compare_multiple_images([prop3_path, prop4_path], comparison_prompt)
        print(result)
    else:
        print(f"One or both images not found")

    print("\n")

    # Example 4: Batch process multiple properties
    print("=" * 60)
    print("EXAMPLE 4: Batch Fire Risk Assessment")
    print("=" * 60)
    property_files = [f"prop{i}.png" for i in range(1, 8)]

    for prop_file in property_files:
        prop_path = os.path.join(images_dir, prop_file)
        if os.path.exists(prop_path):
            print(f"\nAnalyzing {prop_file}...")
            result = analyze_fire_risk_from_file(prop_path)
            print(result)
            print("-" * 60)
        else:
            print(f"Image not found: {prop_path}")
