"""Course detail extraction module using Firecrawl API."""
import os
import time
import json
import threading
from typing import List, Optional, Generator, Tuple, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv

try:
    from firecrawl.firecrawl import FirecrawlApp as FirecrawlClient
except ImportError:
    from firecrawl import Firecrawl as FirecrawlClient


# -----------------------------
# Constants
# -----------------------------
EXTRACTION_TIMEOUT = 60  # seconds
REQUEST_DELAY = 3  # seconds between requests
OUTPUT_FILE = "courses_full.json"


# -----------------------------
# Data Models
# -----------------------------

class CourseSchema(BaseModel):
    """Schema for course data."""
    course_name: str = Field(..., description="Title of the course / programme")
    level: Optional[str] = Field(None, description="Undergraduate, Postgraduate, Diploma, etc.")
    fees: Optional[str] = Field(None, description="Fees or cost info")
    intake_date: Optional[str] = Field(None, description="Next intake or start date")
    requirements: Optional[str] = Field(None, description="Entry requirements or prerequisites")
    description: Optional[str] = Field(None, description="Course description / overview")
    duration: Optional[str] = Field(None, description="Course duration")
    source_url: Optional[str] = Field(None, description="URL of the course page")


# -----------------------------
# Extraction Functions
# -----------------------------

def _get_extraction_schema() -> Dict[str, Any]:
    """Get the schema for course extraction."""
    return {
        "type": "object",
        "properties": {
            "course_name": {"type": "string"},
            "level": {"type": "string"},
            "fees": {"type": "string"},
            "intake_date": {"type": "string"},
            "requirements": {"type": "string"},
            "description": {"type": "string"},
            "duration": {"type": "string"}
        },
        "required": ["course_name"]
    }


def _get_extraction_prompt() -> str:
    """Get the prompt for course extraction."""
    return (
        "Extract full details of this course: course name, level, fees (UK and International if available),"
        "intake / year of entry, entry requirements, full description, duration."
        "Return a structured object with these fields."
    )


def extract_course_details(
    fc: FirecrawlClient,
    course_urls: List[str]
) -> Generator[Tuple[Optional[str], Optional[Dict[str, Any]]], None, None]:
    """
    Generator that yields progress logs and course data one at a time.
    
    Args:
        fc: Firecrawl client instance
        course_urls: List of course URLs to extract
        
    Yields:
        Tuple of (log_message, course_dict):
        - (log_message, None) -> for status updates
        - (None, course_dict) -> for extracted courses
    """
    for i, url in enumerate(course_urls, 1):
        yield f"[{i}/{len(course_urls)}] Extracting from {url}", None
        try:
            print(f"\n\nStarting extraction for: {url}", end="\n\n")
            
            # Add timeout to prevent hanging
            result = None
            error_occurred = None
            
            def extract_worker():
                nonlocal result, error_occurred
                try:
                    result = fc.extract(
                        urls=[url],
                        prompt=_get_extraction_prompt(),
                        schema=_get_extraction_schema(),
                        enable_web_search=False
                    )
                except Exception as e:
                    error_occurred = e
            
            # Start extraction in a thread
            thread = threading.Thread(target=extract_worker)
            thread.daemon = True
            thread.start()
            
            # Wait for timeout
            thread.join(timeout=EXTRACTION_TIMEOUT)
            
            if thread.is_alive():
                print(f"Extraction timed out for: {url}")
                yield f"⏰ Timeout extracting {url} ({EXTRACTION_TIMEOUT}s limit)", None
                continue
            
            if error_occurred:
                print(f"Error extracting {url}: \nraised error--> {error_occurred}")
                yield f"❌ Error extracting {url}: {error_occurred}", None
                continue
                
            if not result:
                print(f"No result for: {url}")
                yield f"⚠️ No result for {url}", None
                continue
                
            print(f"Extraction completed for: {url}")
                
        except Exception as e:
            print(f"Error extracting {url}: {e}")
            yield f"❌ Error extracting {url}: {e}", None
            continue

        if not result or result.data is None:
            yield f"⚠️ No data for {url}", None
            continue

        raw = result.data
        items = raw if isinstance(raw, list) else [raw]
        for d in items:
            if isinstance(d, dict):
                d["source_url"] = url
                yield None, d
        time.sleep(REQUEST_DELAY)  # Delay between requests


def extract_all_courses(course_urls: List[str], output_file: str = OUTPUT_FILE) -> List[Dict[str, Any]]:
    """
    Extract all courses and return a list of unique courses.
    
    Args:
        course_urls: List of course URLs to extract
        output_file: Output JSON file path
        
    Returns:
        List of extracted course dictionaries
        
    Raises:
        EnvironmentError: If FIRECRAWL_API_KEY is not set
    """
    load_dotenv()
    API_KEY = os.getenv("FIRECRAWL_API_KEY")
    if not API_KEY:
        raise EnvironmentError("FIRECRAWL_API_KEY not set in .env file")

    fc = FirecrawlClient(api_key=API_KEY)

    results = []
    seen = set()
    for log, course in extract_course_details(fc, course_urls):
        if course:
            key = course.get("course_name", "").lower().strip()
            if key and key not in seen:
                seen.add(key)
                results.append(course)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return results


if __name__ == "__main__":
    # Example usage
    course_urls = [
        "https://www.liverpool.ac.uk/study/online/"
    ]
    extract_all_courses(course_urls)
