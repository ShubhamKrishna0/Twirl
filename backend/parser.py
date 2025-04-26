# parser.py

def extract_relevant_part(text: str) -> str:
    """
    Extract content between <threejs_output> and </threejs_output> tags.
    
    Args:
        text (str): The input string containing the Three.js script or other content.
    
    Returns:
        str: The extracted content between the tags, or the full text if tags are not found.
    """
    start_tag = "<threejs_output>"
    end_tag = "</threejs_output>"
    start_idx = text.find(start_tag)
    if start_idx == -1:
        return text  # Return full text if start tag not found
    start_idx += len(start_tag)
    end_idx = text.find(end_tag, start_idx)
    if end_idx == -1:
        return text[start_idx:].strip()  # Return from start tag to end if end tag missing
    return text[start_idx:end_idx].strip()

# Optional: Add more utility functions if needed in the future
def has_threejs_output(text: str) -> bool:
    """
    Check if the text contains <threejs_output> tags.
    
    Args:
        text (str): The input string to check.
    
    Returns:
        bool: True if both start and end tags are present, False otherwise.
    """
    return "<threejs_output>" in text and "</threejs_output>" in text

if __name__ == "__main__":
    # Example usage for testing
    test_text = """
    Some preamble
    <model_planning>Planning stuff</model_planning>
    <threejs_output>
    // Three.js code here
    const scene = new THREE.Scene();
    </threejs_output>
    Some trailing text
    """
    result = extract_relevant_part(test_text)
    print(result)