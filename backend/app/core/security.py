import re

# Blacklist of destructive or non-read-only SQL keywords
FORBIDDEN_KEYWORDS = [
    "DROP",
    "TRUNCATE",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "CREATE",
    "GRANT",
    "REVOKE",
    "COMMENT",
    "EXECUTE",
]

def validate_sql_query(query: str) -> None:
    """
    Validates a SQL query for safety.
    
    Ensures the query:
    1. Starts with a read-only keyword (SELECT or WITH).
    2. Does not contain any forbidden keywords (e.g., DROP, DELETE).
    
    Raises:
        ValueError: If the query is considered unsafe.
    """
    clean_query = query.strip().upper()
    
    # Check if query is empty
    if not clean_query:
        raise ValueError("SQL query cannot be empty.")

    # Rule 1: Must start with SELECT or WITH
    if not (clean_query.startswith("SELECT") or clean_query.startswith("WITH")):
        raise ValueError("Only SELECT or WITH (CTE) queries are allowed for safety reasons.")

    # Rule 2: Check for forbidden keywords using regex for word boundaries
    for keyword in FORBIDDEN_KEYWORDS:
        # \b ensures we match the whole word (e.g., 'DROP' but not 'DROPLET')
        pattern = rf"\b{keyword}\b"
        if re.search(pattern, clean_query):
            raise ValueError(f"Forbidden keyword '{keyword}' detected in query.")
