import os

# Toggle caching for heavy API calls. Set environment variable ENABLE_CACHE to 'false' to disable.
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
