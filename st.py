"""Streamlit application for course extraction."""
import asyncio
import sys
import time
import json
import os
from typing import Dict, Any, List
from urllib.parse import urlparse

# Fix for Windows Python 3.13+ asyncio subprocess issues
# This must be set before any asyncio operations or imports that use asyncio
# WindowsProactorEventLoopPolicy supports subprocess operations (required by Playwright)
# WindowsSelectorEventLoopPolicy does NOT support subprocess operations
if sys.platform.startswith('win'):
    if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    elif hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
        # Fallback if Proactor is not available (older Python versions)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
import nest_asyncio
# Apply nest_asyncio patch early for Windows compatibility with nested event loops
nest_asyncio.apply()

from dotenv import load_dotenv
from course_extractor import extract_course_details
from extractor import scrape_university_courses_sync

try:
    from firecrawl.firecrawl import FirecrawlApp as FirecrawlClient
except ImportError:
    from firecrawl import Firecrawl as FirecrawlClient

# -----------------------------
# Streamlit Setup
# -----------------------------
st.set_page_config(
    page_title="BoldStep.AI Course Extractor", 
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .course-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
    }
    
    .course-title {
        color: #2c3e50;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .course-detail {
        background: rgba(255,255,255,0.8);
        padding: 8px 12px;
        border-radius: 8px;
        margin: 5px 0;
        font-size: 0.9rem;
    }
    
    .course-detail strong {
        color: #34495e;
    }
    
    .url-input-container, .uni-input-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #ddd;
    }
    
    .extraction-status {
        background: #e8f4fd;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 10px 0;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
    }
    
    .stat-item {
        text-align: center;
        color: white;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# BoldStep.AI Logo
# -----------------------------
def create_logo():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                <div style="display: flex; gap: 5px;">
                    <div style="width: 20px; height: 20px; background: white; transform: rotate(45deg); 
                                box-shadow: 2px 2px 4px rgba(0,0,0,0.3);"></div>
                    <div style="width: 20px; height: 20px; background: white; transform: rotate(45deg); 
                                box-shadow: 2px 2px 4px rgba(0,0,0,0.3); margin-top: 8px;"></div>
                </div>
                <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: bold; 
                           text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    BoldStep<span style="color: #ffd700; font-size: 2rem;">.AI</span>
                </h1>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def validate_url(url: str) -> bool:
    """
    Validate if URL is properly formatted.
    
    Args:
        url: URL string to validate
        
    Returns:
        True if URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def create_course_card(course: Dict[str, Any], index: int) -> None:
    """
    Create a beautiful, detailed course card display.
    
    Args:
        course: Course dictionary with course details
        index: Index of the course in the list
    """
    course_json = json.dumps(course, indent=2, ensure_ascii=False)

    st.markdown(f"""
    <div class="course-card">
        <div class="course-title">🎓 {course.get('course_name', 'Unknown Course')}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        if course.get('level'):
            st.markdown(f"**🎯 Level:** {course['level']}")
        if course.get('duration'):
            st.markdown(f"**⏰ Duration:** {course['duration']}")
        if course.get('fees'):
            st.markdown(f"**💰 Fees:** {course['fees']}")
        if course.get('intake_date'):
            st.markdown(f"**📅 Intake Date:** {course['intake_date']}")
        if course.get('requirements'):
            st.markdown(f"**📋 Requirements:** {course['requirements']}")
        if course.get('source_url'):
            st.markdown(f"**🔗 Source:** [View Original Page]({course['source_url']})")

        if course.get('description'):
            with st.expander("📖 Course Description", expanded=False):
                st.markdown(course['description'])

    with col2:
        if course.get('source_url'):
            st.link_button("🔗 View Original", course['source_url'], use_container_width=True)

        st.download_button(
            label="📥 Download JSON",
            data=course_json,
            file_name=f"course_{index+1}.json",
            mime="application/json",
            use_container_width=True,
            key=f"download_course_{index}_{int(time.time() * 1000)}"
        )

    with st.expander(f"🛠️ Raw Data - {course.get('course_name', 'Course')}"):
        st.json(course)

# Initialize session state
if 'courses_data' not in st.session_state:
    st.session_state.courses_data = []

create_logo()

st.markdown("---")

# -----------------------------
# Main App
# -----------------------------
st.title("🎓 Course Extractor")
st.markdown("Extract detailed course information from university websites")

# Load API key
load_dotenv()
API_KEY = os.getenv("FIRECRAWL_API_KEY")
if not API_KEY:
    st.error("❌ FIRECRAWL_API_KEY not set in .env file")
    st.stop()

fc = FirecrawlClient(api_key=API_KEY)

# 👇 NEW SECTION: University Website Input for Full Pipeline
st.markdown("""
<div class="uni-input-container">
    <h3 style="color: white; margin-bottom: 10px;">🌐 University Website (Bulk Extraction)</h3>
    <p style="color: rgba(255,255,255,0.8); margin-bottom: 0;">
        Enter the main university website (e.g., <code>https://wrexham.ac.uk/international-students/courses/</code>). 
        We'll discover and extract <strong>all available courses</strong using the full pipeline.
    </p>
</div>
""", unsafe_allow_html=True)

university_url = st.text_input(
    "University Home/Study URL:",
    placeholder="https://wrexham.ac.uk/international-students/courses/",
    help="University courses directory (e.g., /courses)"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔍 Extract course links", type="secondary", use_container_width=True):
        if not university_url.strip():
            st.error("❌ Please enter a university URL")
        else:
            with st.spinner("⏳ Running full pipeline extraction… This may take a few minutes."):
                try:
                    st.info("⏳ Running extraction. Please wait...")
                    count, pipeline_results, saved_path = scrape_university_courses_sync(university_url.strip())
                    st.success(f"Extracted {count} courses 🎉")
                    if pipeline_results:
                        st.info(f"✅ Found {len(pipeline_results)} unique course URLs")
                        # csv_data = "\n".join(pipeline_results).encode("utf-8")

                        # st.download_button(
                        #     "Download CSV",
                        #     csv_data,
                        #     "course_links.csv",
                        #     "text/csv"
                        # )
                        # Read the file after saving it
                        with open(saved_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download CSV File",
                                data=f.read(),
                                file_name=os.path.basename(saved_path),
                                mime="text/csv"
                            )
                except Exception as e:
                    st.error(f"💥 Error in extraction: {str(e)}")
                    st.exception(e)

st.markdown("---")

# -----------------------------
# Main Link Input Section - Simplified
# -----------------------------
st.markdown("""
<div class="url-input-container">
    <h3 style="color: white; margin-bottom: 10px;">🔗 Enter Course Link</h3>
    <p style="color: rgba(255,255,255,0.8); margin-bottom: 0;">
        Enter a course URL to extract detailed information. You can add multiple URLs (one per line) for batch extraction.
    </p>
</div>
""", unsafe_allow_html=True)

# Single URL input (prominent)
single_url = st.text_input(
    "🔗 Course URL:",
    placeholder="https://www.abertay.ac.uk/course-search/?keywords=course",
    help="Enter a single course page URL to extract details",
    key="single_url_input"
)

# Multi-line URL input (for batch)
with st.expander("📝 Or enter multiple URLs (one per line)", expanded=False):
    multi_url_input = st.text_area(
        "Course URLs (one per line):",
        height=150,
        placeholder="https://www.university.edu/courses/computer-science\nhttps://www.university.edu/courses/business-studies\n...",
        help="Enter multiple university course page URLs, one per line",
        key="multi_url_input"
    )

# Use single URL if provided, otherwise use multi-line input
if single_url.strip():
    url_input = single_url
elif multi_url_input.strip():
    url_input = multi_url_input
else:
    url_input = ""

# Sample URLs button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📝 Load Sample URLs", use_container_width=True):
        sample_urls = """https://www.liverpool.ac.uk/courses/accounting-and-finance-bsc-hons  
https://www.leedsbeckett.ac.uk/courses/applied-sports-studies-tennis-bsc  
https://www.leedsbeckett.ac.uk/courses/accounting-finance-ba  
https://www.brighton.ac.uk/courses/study/secondary-biology-pgce.aspx  
https://www.hw.ac.uk/study/postgraduate/actuarial-management-with-data-science"""
        st.session_state.sample_urls = sample_urls
        st.rerun()

if 'sample_urls' in st.session_state:
    url_input = st.session_state.sample_urls
    del st.session_state.sample_urls

# Extract Button (for individual URLs)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Extract Course Details", type="primary", use_container_width=True):
        if not url_input.strip():
            st.error("❌ Please enter URLs first")
            st.stop()
        
        urls = [url.strip() for url in url_input.strip().split('\n') if url.strip()]
        
        valid_urls = []
        invalid_urls = []
        
        for url in urls:
            if validate_url(url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        if invalid_urls:
            st.warning(f"⚠️ Found {len(invalid_urls)} invalid URLs:")
            for invalid_url in invalid_urls:
                st.write(f"❌ {invalid_url}")
        
        if not valid_urls:
            st.error("❌ No valid URLs found")
            st.stop()
        
        st.success(f"✅ Found {len(valid_urls)} valid URLs")
        
        progress_container = st.container()
        results_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        results = []
        seen = set()
        
        with results_container:
            st.markdown("---")
            st.subheader("🔄 Live Results")
            results_placeholder = st.empty()
        
        processed_count = 0
        for log, course in extract_course_details(fc, valid_urls):
            if course:
                processed_count += 1
                progress = processed_count / len(valid_urls)
                progress_bar.progress(progress)
                
                key = course.get("course_name", "").lower().strip()
                if key and key not in seen:
                    seen.add(key)
                    results.append(course)
                    
                    with results_placeholder.container():
                        st.write(f"**✅ {len(results)} course(s) extracted so far:**")
                        for idx, result_course in enumerate(reversed(results)):
                            create_course_card(result_course, len(results) - 1 - idx)
            
            if log:
                status_text.markdown(f"""
                <div class="extraction-status">
                    <strong>Processing ({processed_count}/{len(valid_urls)}):</strong> {log}
                </div>
                """, unsafe_allow_html=True)
        
        status_text.success(f"🎉 Extraction completed! Found {len(results)} unique courses.")
        
        if results:
            st.session_state.courses_data.extend(results)
            st.rerun()

# -----------------------------
# Clear Results Button
# -----------------------------
if st.session_state.courses_data:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🗑️ Clear Previous Results", use_container_width=True):
            st.session_state.courses_data = []
            st.rerun()

# -----------------------------
# Results Display (unchanged)
# -----------------------------
if st.session_state.courses_data:
    results = st.session_state.courses_data
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-item">
            <span class="stat-number">{len(results)}</span>
            <span class="stat-label">Courses Extracted</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">{len(set(course.get('university', 'Unknown') for course in results))}</span>
            <span class="stat-label">Universities</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">{len(set(course.get('degree_type', 'Unknown') for course in results))}</span>
            <span class="stat-label">Degree Types</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        all_courses_json = json.dumps(results, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Download All Results",
            data=all_courses_json,
            file_name="extracted_courses.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.courses_data = []
            st.rerun()
    
    with col3:
        if st.button("💾 Save to File", use_container_width=True):
            with open("courses_extracted.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            st.success("✅ Saved to courses_extracted.json")
    
    st.markdown("---")
    
    st.subheader("📚 Extracted Courses")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        universities = sorted(set(course.get('university', 'Unknown') for course in results))
        selected_uni = st.selectbox("🏛️ Filter by University", ['All'] + universities)
    
    with col2:
        degree_types = sorted(set(course.get('degree_type', 'Unknown') for course in results))
        selected_degree = st.selectbox("🎯 Filter by Degree Type", ['All'] + degree_types)
    
    with col3:
        sort_by = st.selectbox("🔄 Sort by", ['Course Name', 'University', 'Degree Type'])
    
    filtered_results = results
    if selected_uni != 'All':
        filtered_results = [c for c in filtered_results if c.get('university') == selected_uni]
    if selected_degree != 'All':
        filtered_results = [c for c in filtered_results if c.get('degree_type') == selected_degree]
    
    if sort_by == 'Course Name':
        filtered_results = sorted(filtered_results, key=lambda x: x.get('course_name', ''))
    elif sort_by == 'University':
        filtered_results = sorted(filtered_results, key=lambda x: x.get('university', ''))
    elif sort_by == 'Degree Type':
        filtered_results = sorted(filtered_results, key=lambda x: x.get('degree_type', ''))
    
    st.write(f"Showing {len(filtered_results)} of {len(results)} courses")
    
    for i, course in enumerate(filtered_results):
        create_course_card(course, i)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p><strong>🚀 Powered by BoldStep.AI</strong></p>
    <p>Advanced Course Data Extraction Tool | Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
