"""Test script to extract courses from Abertay URL."""
import json
import os
from dotenv import load_dotenv
from course_extractor import extract_all_courses

# Load environment variables
load_dotenv()

# Test URL
TEST_URL = "https://www.abertay.ac.uk/course-search/?keywords=course"

if __name__ == "__main__":
    print(f"Testing extraction with URL: {TEST_URL}")
    print("=" * 80)
    
    # Check API key
    API_KEY = os.getenv("FIRECRAWL_API_KEY")
    if not API_KEY:
        print("❌ ERROR: FIRECRAWL_API_KEY not set in .env file")
        exit(1)
    
    print(f"✅ API Key found: {API_KEY[:10]}...")
    print("\nStarting extraction...\n")
    
    try:
        # Extract courses
        results = extract_all_courses([TEST_URL], output_file="test_extraction_results.json")
        
        print("\n" + "=" * 80)
        print(f"✅ Extraction completed!")
        print(f"📊 Found {len(results)} course(s)")
        print("=" * 80)
        
        # Display results
        if results:
            print("\n📚 Extracted Courses:\n")
            for i, course in enumerate(results, 1):
                print(f"\n--- Course {i} ---")
                print(json.dumps(course, indent=2, ensure_ascii=False))
        else:
            print("\n⚠️  No courses extracted")
        
        print(f"\n💾 Results saved to: test_extraction_results.json")
        
    except Exception as e:
        print(f"\n❌ Error during extraction: {e}")
        import traceback
        traceback.print_exc()

