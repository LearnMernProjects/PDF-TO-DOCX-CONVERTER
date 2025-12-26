def normalize_lines(text: str):

   
    normalized_lines = []

   
    for raw_line in text.split("\n"):

  
        line = raw_line.strip()


        if not line:
            continue


        line = " ".join(line.split())

   
        normalized_lines.append(line)

    return normalized_lines


def looks_like_sentence(line: str) -> bool:
    """
    Checks whether a line looks like a normal sentence.

    Sentences usually:
    - End with a period
    - Contain commas
    - Are not fully uppercase
    """

    # If line ends with a full stop, it is likely a sentence
    if line.endswith("."):
        return True

    # If line contains commas, it is usually descriptive text
    if "," in line:
        return True

    return False
def is_heading(line: str) -> bool:
    """
    Determines whether a line is a heading using structural heuristics.

    A heading typically:
    - Is short
    - Has mostly uppercase letters
    - Does not look like a sentence
    """

    # Very long lines are unlikely to be headings
    if len(line) > 50:
        return False

    # Extract only alphabetic characters from the line
    letters = [char for char in line if char.isalpha()]

    # If there are no letters, it cannot be a heading
    if not letters:
        return False

    # Calculate ratio of uppercase letters
    uppercase_count = sum(1 for char in letters if char.isupper())
    uppercase_ratio = uppercase_count / len(letters)

    # Headings usually have majority uppercase letters
    if uppercase_ratio < 0.7:
        return False

    # Headings are not full sentences
    if looks_like_sentence(line):
        return False

    return True

def detect_title(lines: list[str]) -> str:
    """
    Detects the document title.

    Strategy:
    - Title appears near the top
    - Title structurally looks like a heading
    - First strong heading is treated as title
    """

    # Only inspect the first few lines to avoid false positives
    for line in lines[:5]:
        if is_heading(line):
            return line

    # If no title is detected, return empty string
    return ""
def group_content_under_headings(text: str):
    """
    Groups normalized text lines under detected headings.

    Input:
    - Raw extracted text (string)

    Output:
    {
        "title": "DOCUMENT TITLE",
        "sections": {
            "HEADING 1": [line1, line2, ...],
            "HEADING 2": [line1, line2, ...],
            ...
        }
    }
    """

    # STEP 1: Normalize raw text into clean lines (STEP 2.1)
    lines = normalize_lines(text)

    # STEP 2: Detect document title (STEP 2.2)
    title = detect_title(lines)

    # Dictionary to store sections and their content
    sections = {}

    # Keeps track of which section we are currently inside
    current_heading = None

    # Iterate through each line in order
    for line in lines:

        # Skip the title line so it is not treated as a section
        if line == title:
            continue

        # Check if the current line is a heading
        if is_heading(line):

            # When a new heading is found, create a new section
            current_heading = line

            # Initialize an empty list to store content for this heading
            sections[current_heading] = []

            # Move to next line (content will be added later)
            continue

        # If the line is not a heading, it is content
        # Content must belong to the most recent heading
        if current_heading:
            sections[current_heading].append(line)

        # If no heading has been detected yet,
        # we safely ignore the line (metadata like Name, Email, etc.)
        # This avoids wrongly grouping header info into sections

    # Return the structured document
    return {
        "title": title,
        "sections": sections
    }
