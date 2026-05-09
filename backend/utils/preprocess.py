import re

# -----------------------------
# 🧹 CLEAN TEXT FUNCTION
# -----------------------------
def clean_text(text: str) -> str:
    """
    Cleans input text by:
    - converting to lowercase
    - removing special characters, numbers, emojis
    - removing extra spaces
    """

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z ]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text