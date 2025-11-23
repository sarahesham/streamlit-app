# """Unified course link extraction module for multiple universities."""
# import os
# import sys
# import asyncio
# import re
# import csv
# from datetime import datetime
# from typing import List, Tuple, Optional, Dict, Any
# from urllib.parse import urlparse, parse_qs, unquote, urljoin, urlencode, urlsplit, urlunsplit

# # Fix for Windows Python 3.13+ asyncio subprocess issues with Playwright
# # WindowsProactorEventLoopPolicy supports subprocess operations (required by Playwright)
# # WindowsSelectorEventLoopPolicy does NOT support subprocess operations
# if sys.platform.startswith('win'):
#     if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
#         asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
#     elif hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
#         # Fallback if Proactor is not available (older Python versions)
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# from playwright.async_api import async_playwright, Page, TimeoutError as PWTimeoutError
# from university_config import get_config_for_url, get_university_display_name, UNIVERSITY_CONFIGS


# # -----------------------------
# # Constants
# # -----------------------------
# OUTPUT_MAIN_FOLDER = "output_links_files"
# MAX_PAGES = 100  # Maximum pages to prevent infinite loops
# PAGE_LOAD_TIMEOUT = 60000
# PAGINATION_DELAY = 1000


# # -----------------------------
# # Utility Functions
# # -----------------------------

# def _ensure_output_dirs(folder_name: str) -> str:
#     """
#     Ensure output directories exist.
    
#     Args:
#         folder_name: Name of the subfolder to create
        
#     Returns:
#         Path to the created subfolder
#     """
#     main_folder = OUTPUT_MAIN_FOLDER
#     os.makedirs(main_folder, exist_ok=True)
#     subfolder = os.path.join(main_folder, folder_name)
#     os.makedirs(subfolder, exist_ok=True)
#     return subfolder


# def save_list_to_file(filename: str, items: List[str], folder_name: str) -> str:
#     """
#     Save a list of items to a file (legacy function for backward compatibility).
    
#     Args:
#         filename: Name of the file to save
#         items: List of strings to save
#         folder_name: Name of the subfolder
        
#     Returns:
#         Full path to the saved file
#     """
#     subfolder = _ensure_output_dirs(folder_name)
#     full_path = os.path.join(subfolder, filename)
#     with open(full_path, "w", encoding="utf-8") as f:
#         for item in items:
#             f.write(str(item) + "\n")
#     return full_path


# def save_urls_to_csv(
#     urls: List[str],
#     university_name: str,
#     university_id: Optional[int] = None,
#     discovered_via: str = "unified-extractor",
#     folder_name: Optional[str] = None,
#     filename: Optional[str] = None
# ) -> str:
#     """
#     Save URLs to CSV file matching the export structure.
    
#     Args:
#         urls: List of course URLs to save
#         university_name: Name of the university
#         university_id: Optional university ID (defaults to 1 if not provided)
#         discovered_via: How the URLs were discovered (default: "unified-extractor")
#         folder_name: Optional folder name (defaults to university_name)
#         filename: Optional filename (defaults to "{university_name}_courses.csv")
        
#     Returns:
#         Full path to the saved CSV file
#     """
#     if university_id is None:
#         university_id = 1  # Default ID
    
#     if folder_name is None:
#         folder_name = university_name.lower().replace(" ", "_")
    
#     if filename is None:
#         filename = f"{folder_name}_courses.csv"
    
#     subfolder = _ensure_output_dirs(folder_name)
#     full_path = os.path.join(subfolder, filename)
    
#     # Get current timestamp
#     extracted_at = datetime.now().isoformat()
    
#     # Prepare CSV data
#     csv_data = []
#     for idx, url in enumerate(urls):
#         csv_data.append({
#             "": idx,  # Index column
#             "url": url,
#             "university_id": university_id,
#             "university_name": university_name,
#             "discovered_via": discovered_via,
#             "link_group_type": "",  # Empty as per CSV structure
#             "confidence_score": "",  # Empty as per CSV structure
#             "status": "pending",
#             "extracted_at": extracted_at,
#             "error_message": ""
#         })
    
#     # Write CSV file
#     if csv_data:
#         fieldnames = ["", "url", "university_id", "university_name", "discovered_via", 
#                      "link_group_type", "confidence_score", "status", "extracted_at", "error_message"]
#         with open(full_path, "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=fieldnames)
#             writer.writeheader()
#             writer.writerows(csv_data)
#         print(f"[✔] Saved {len(urls)} URLs to CSV: {full_path}")
#     else:
#         # Create empty CSV with headers
#         fieldnames = ["", "url", "university_id", "university_name", "discovered_via", 
#                      "link_group_type", "confidence_score", "status", "extracted_at", "error_message"]
#         with open(full_path, "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=fieldnames)
#             writer.writeheader()
#         print(f"[✔] Created empty CSV: {full_path}")
    
#     return full_path


# def filter_links_by_keywords(
#     links: List[str],
#     keywords: List[str],
#     filename: str,
#     folder_name: str,
#     match_mode: str = "contains",
#     university_name: Optional[str] = None,
#     university_id: Optional[int] = None,
#     save_as_csv: bool = True
# ) -> List[str]:
#     """
#     Filter links by keywords and save to CSV file.
    
#     Args:
#         links: List of URLs to filter
#         keywords: List of keywords to match against
#         filename: Output filename (will be converted to .csv if save_as_csv=True)
#         folder_name: Name of the subfolder
#         match_mode: "contains" or "segment"
#         university_name: University name for CSV (defaults to folder_name)
#         university_id: University ID for CSV (defaults to 1)
#         save_as_csv: Whether to save as CSV (True) or text file (False)
        
#     Returns:
#         List of filtered URLs
#     """
#     if not keywords:
#         if save_as_csv:
#             # Save empty CSV
#             csv_filename = filename.replace(".txt", ".csv") if filename.endswith(".txt") else filename
#             if not csv_filename.endswith(".csv"):
#                 csv_filename += ".csv"
#             save_urls_to_csv(
#                 [],
#                 university_name or folder_name,
#                 university_id,
#                 "unified-extractor",
#                 folder_name,
#                 csv_filename
#             )
#         else:
#             save_list_to_file(filename, [], folder_name)
#         return []

#     filtered = []
#     keyword_list = [kw.lower().strip() for kw in keywords if kw]

#     for url in links:
#         if not isinstance(url, str):
#             continue
#         try:
#             path = urlparse(url).path.lower()
#         except Exception:
#             path = url.lower()

#         match = False
#         for kw in keyword_list:
#             if not kw:
#                 continue
#             if match_mode == "segment":
#                 segments = [s for s in path.strip("/").split("/") if s]
#                 if kw.strip("/") in segments:
#                     match = True
#                     break
#             else:  # 'contains'
#                 if kw in path:
#                     match = True
#                     break
#         if match:
#             filtered.append(url)

#     if save_as_csv:
#         # Save filtered results as CSV
#         csv_filename = filename.replace(".txt", ".csv") if filename.endswith(".txt") else filename
#         if not csv_filename.endswith(".csv"):
#             csv_filename += ".csv"
#         save_urls_to_csv(
#             filtered,
#             university_name or folder_name,
#             university_id,
#             "unified-extractor",
#             folder_name,
#             csv_filename
#         )
#     else:
#         save_list_to_file(filename, filtered, folder_name)
    
#     return filtered


# # -----------------------------
# # Unified Scraper Functions
# # -----------------------------

# async def _extract_course_links(
#     page: Page,
#     config: Dict[str, Any],
#     base_url: str
# ) -> List[str]:
#     """
#     Extract course links from current page using config selector.
    
#     Args:
#         page: Playwright page object
#         config: University configuration
#         base_url: Base URL for resolving relative links
        
#     Returns:
#         List of course URLs
#     """
#     course_urls = []
#     selector = config.get("course_selector")
#     if not selector:
#         return course_urls
    
#     try:
#         # Wait for selector if specified
#         wait_selector = config.get("wait_selector", selector)
#         if wait_selector:
#             try:
#                 await page.wait_for_selector(wait_selector, timeout=20000)
#             except PWTimeoutError:
#                 pass  # Continue anyway
        
#         # Extract links based on selector
#         elements = await page.query_selector_all(selector)
        
#         url_resolution = config.get("url_resolution")
#         special_logic = config.get("special_logic")
        
#         for el in elements:
#             try:
#                 if special_logic == "generate_slug_from_title":
#                     # York College: Generate URL from title
#                     title = await el.inner_text()
#                     if title:
#                         slug = re.sub(r'[^a-z0-9\s]', '', title.lower())
#                         slug = re.sub(r'\s+', '-', slug)
#                         slug = re.sub(r'-+', '-', slug).strip('-')
#                         if slug and len(slug) >= 3:
#                             parsed = urlparse(base_url)
#                             course_url = f"{parsed.scheme}://{parsed.netloc}/academics/programs/{slug}"
#                             course_urls.append(course_url)
#                 elif selector == "div.listing-item__header.test a[data-live-url]":
#                     # Otago: Extract from data-live-url attribute
#                     href = await el.get_attribute("data-live-url")
#                     if href:
#                         course_urls.append(href.strip())
#                 else:
#                     # Standard: Extract href attribute
#                     href = await el.get_attribute("href")
#                     if not href:
#                         continue
                    
#                     # Resolve URL using resolution function if provided
#                     if url_resolution:
#                         resolved = url_resolution(href, base_url)
#                         if resolved:
#                             course_urls.append(resolved)
#                     else:
#                         # Standard URL join
#                         full_url = urljoin(base_url, href)
#                         course_urls.append(full_url)
#             except Exception:
#                 continue  # Skip malformed URLs
                
#     except Exception as e:
#         print(f"Error extracting course links: {e}")
    
#     return course_urls


# async def _handle_next_button_pagination(
#     page: Page,
#     config: Dict[str, Any],
#     current_url: str,
#     visited_urls: List[str]
# ) -> Optional[str]:
#     """
#     Handle pagination using next button.
    
#     Returns:
#         Next URL if available, None otherwise
#     """
#     selector = config.get("pagination_selector")
#     if not selector:
#         return None
    
#     try:
#         # Check if next button exists and is enabled
#         next_button = await page.query_selector(selector)
#         if not next_button:
#             return None
        
#         # Check if disabled (various ways)
#         is_disabled = await next_button.is_disabled() if hasattr(next_button, 'is_disabled') else False
#         class_attr = await next_button.get_attribute("class") or ""
#         aria_disabled = await next_button.get_attribute("aria-disabled")
        
#         if is_disabled or "disabled" in class_attr.lower() or aria_disabled == "true":
#             return None
        
#         # Get next URL
#         next_href = await next_button.get_attribute("href")
#         if not next_href or next_href in ["", "#", "javascript:void(0)"]:
#             # Try clicking and getting new URL
#             try:
#                 await next_button.click()
#                 await page.wait_for_timeout(config.get("pagination_delay", PAGINATION_DELAY))
#                 new_url = page.url
#                 if new_url != current_url and new_url not in visited_urls:
#                     return new_url
#             except Exception:
#                 pass
#             return None
        
#         # Resolve next URL
#         next_url = urljoin(current_url, next_href)
#         if next_url == current_url or next_url in visited_urls:
#             return None
        
#         return next_url
        
#     except Exception:
#         return None


# async def _handle_page_numbers_pagination(
#     page: Page,
#     config: Dict[str, Any],
#     base_url: str
# ) -> List[str]:
#     """
#     Handle pagination by extracting total page count and generating URLs.
    
#     Returns:
#         List of pagination URLs
#     """
#     pagination_urls = []
#     selector = config.get("pagination_selector")
#     param = config.get("pagination_param", "page")
    
#     try:
#         if selector:
#             await page.wait_for_selector(selector, timeout=30000)
            
#             # Extract total pages
#             total_pages = 1
#             try:
#                 # Try extracting from text (e.g., "Page 1 of 22")
#                 text = await page.locator(selector).inner_text()
#                 pattern = config.get("pagination_extract_pattern", r"of\D*(\d+)")
#                 match = re.search(pattern, text.replace("\xa0", " ").replace("Page", ""))
#                 if match:
#                     total_pages = int(match.group(1))
#                 else:
#                     # Fallback: count options in select
#                     option_count = await page.locator(f"select[aria-label*='page'] option").count()
#                     if option_count > 0:
#                         total_pages = option_count
#             except Exception:
#                 total_pages = 1
            
#             # Generate pagination URLs
#             parsed = urlparse(base_url)
#             base_path = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
#             query_params = parse_qs(parsed.query, keep_blank_values=True)
            
#             for i in range(1, total_pages + 1):
#                 if i == 1:
#                     pagination_urls.append(base_url)
#                 else:
#                     query_params[param] = [str(i - 1)] if "shu.ac.uk" in base_url else [str(i)]
#                     query_string = urlencode(query_params, doseq=True)
#                     pagination_urls.append(f"{base_path}?{query_string}")
#         else:
#             pagination_urls.append(base_url)
            
#     except Exception as e:
#         print(f"Error extracting page numbers: {e}")
#         pagination_urls.append(base_url)
    
#     return pagination_urls


# async def _handle_url_params_pagination(
#     page: Page,
#     config: Dict[str, Any],
#     base_url: str
# ) -> List[str]:
#     """
#     Handle pagination by modifying URL parameters.
    
#     Returns:
#         List of pagination URLs
#     """
#     pagination_urls = []
#     param = config.get("pagination_param", "page")
#     increment = config.get("pagination_increment", 1)
#     start_value = config.get("pagination_start", 1)
    
#     # For Canterbury, we need to detect when to stop
#     if "canterbury.ac.nz" in base_url:
#         # Canterbury uses start_rank parameter
#         current_rank = start_value
#         max_pages = 50  # Safety limit
        
#         for page_num in range(1, max_pages + 1):
#             if page_num == 1:
#                 pagination_urls.append(base_url)
#             else:
#                 url = f"{base_url}&start_rank={current_rank}"
#                 pagination_urls.append(url)
#                 current_rank += increment
#     else:
#         # Standard URL param pagination
#         parsed = urlparse(base_url)
#         base_path = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
#         query_params = parse_qs(parsed.query, keep_blank_values=True)
        
#         for i in range(1, MAX_PAGES + 1):
#             if i == 1:
#                 pagination_urls.append(base_url)
#             else:
#                 query_params[param] = [str(i - 1)]
#                 query_string = urlencode(query_params, doseq=True)
#                 pagination_urls.append(f"{base_path}?{query_string}")
    
#     return pagination_urls


# async def _handle_accordion_pagination(
#     page: Page,
#     config: Dict[str, Any]
# ) -> bool:
#     """
#     Handle accordion-style pagination by expanding sections.
    
#     Returns:
#         True if accordion was handled
#     """
#     selector = config.get("pagination_selector")
#     if not selector:
#         return False
    
#     try:
#         accordion_buttons = await page.query_selector_all(selector)
#         for btn in accordion_buttons:
#             try:
#                 aria_expanded = await btn.get_attribute("aria-expanded")
#                 if aria_expanded != "true":
#                     await btn.click()
#                     await page.wait_for_timeout(1000)  # Wait for accordion to expand
#             except Exception:
#                 continue
#         return True
#     except Exception:
#         return False


# async def scrape_university_courses(university_url: str) -> Tuple[int, List[str]]:
#     """
#     Unified function to scrape course URLs from any configured university.
    
#     Args:
#         university_url: URL of the university course page
        
#     Returns:
#         Tuple of (total_count, unique_urls)
        
#     Raises:
#         ValueError: If university is not configured
#     """
#     # Get configuration for this university
#     config = get_config_for_url(university_url)
#     if not config:
#         raise ValueError(f"University URL '{university_url}' is not configured. "
#                         f"Available universities: {', '.join(UNIVERSITY_CONFIGS.keys())}")
    
#     folder_name = config.get("folder_name", "unknown")
#     pagination_type = config.get("pagination_type", "single_page")
    
#     # Windows Python 3.13+ fix: Ensure ProactorEventLoopPolicy is set before Playwright creates subprocess
#     if sys.platform.startswith('win'):
#         if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
#             policy = asyncio.WindowsProactorEventLoopPolicy()
#             asyncio.set_event_loop_policy(policy)
    
#     all_urls = []
#     pagination_urls = []
    
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(
#             headless=True,
#             args=[
#                 "--no-sandbox",
#                 "--disable-setuid-sandbox",
#                 "--disable-dev-shm-usage",
#                 "--disable-gpu",
#                 "--disable-extensions"
#             ]
#         )
#         try:
#             context = await browser.new_context(
#                 viewport={"width": 1920, "height": 1080},
#                 user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
#             )
#             page = await context.new_page()
#             page.set_default_timeout(PAGE_LOAD_TIMEOUT)
            
#             # Parse base URL
#             parsed = urlparse(university_url)
#             base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            
#             # Handle different pagination types
#             if pagination_type == "single_page":
#                 # Single page - no pagination
#                 await page.goto(university_url, wait_until="domcontentloaded")
#                 pagination_urls.append(university_url)
#                 course_urls = await _extract_course_links(page, config, base_url)
#                 all_urls.extend(course_urls)
                
#             elif pagination_type == "accordion":
#                 # Accordion - expand all sections
#                 await page.goto(university_url, wait_until="domcontentloaded")
#                 pagination_urls.append(university_url)
#                 await _handle_accordion_pagination(page, config)
#                 course_urls = await _extract_course_links(page, config, base_url)
#                 all_urls.extend(course_urls)
                
#             elif pagination_type == "page_numbers":
#                 # Extract total pages and generate URLs
#                 await page.goto(university_url, wait_until="domcontentloaded")
#                 pagination_urls = await _handle_page_numbers_pagination(page, config, university_url)
                
#                 # Scrape each page
#                 for pag_url in pagination_urls:
#                     try:
#                         await page.goto(pag_url, wait_until="domcontentloaded")
#                         course_urls = await _extract_course_links(page, config, base_url)
#                         all_urls.extend(course_urls)
#                         await asyncio.sleep(0.5)  # Small delay between pages
#                     except Exception as e:
#                         print(f"Error scraping page {pag_url}: {e}")
#                         continue
                        
#             elif pagination_type == "url_params":
#                 # Generate URLs with different parameters
#                 pagination_urls = await _handle_url_params_pagination(page, config, university_url)
                
#                 # Scrape each page
#                 for pag_url in pagination_urls:
#                     try:
#                         await page.goto(pag_url, wait_until="domcontentloaded")
                        
#                         # Handle cookies/overlays if needed
#                         if "canterbury.ac.nz" in pag_url:
#                             try:
#                                 accept_btn = await page.get_by_role("button", name=re.compile(r"Accept|Agree", re.I)).first
#                                 if await accept_btn.is_visible(timeout=5000):
#                                     await accept_btn.click()
#                                     await page.wait_for_timeout(1000)
#                             except:
#                                 pass
                        
#                         course_urls = await _extract_course_links(page, config, base_url)
#                         all_urls.extend(course_urls)
#                         # For Canterbury, stop if no results found
#                         if "canterbury.ac.nz" in pag_url and not course_urls:
#                             break
#                         await asyncio.sleep(1)  # Delay for Canterbury
#                     except Exception as e:
#                         print(f"Error scraping page {pag_url}: {e}")
#                         continue
                        
#             elif pagination_type == "next_button":
#                 # Click next button repeatedly
#                 current_url = university_url
#                 visited_urls = []
#                 page_count = 0
                
#                 while page_count < MAX_PAGES:
#                     try:
#                         await page.goto(current_url, wait_until="domcontentloaded")
#                         pagination_urls.append(current_url)
#                         visited_urls.append(current_url)
                        
#                         course_urls = await _extract_course_links(page, config, base_url)
#                         all_urls.extend(course_urls)
                        
#                         # Try to get next URL
#                         next_url = await _handle_next_button_pagination(page, config, current_url, visited_urls)
#                         if not next_url:
#                             break
                        
#                         current_url = next_url
#                         page_count += 1
#                         await asyncio.sleep(0.8)  # Delay between pages
                        
#                     except Exception as e:
#                         print(f"Error in pagination loop: {e}")
#                         break
#             else:
#                 # Unknown pagination type - treat as single page
#                 await page.goto(university_url, wait_until="domcontentloaded")
#                 pagination_urls.append(university_url)
#                 course_urls = await _extract_course_links(page, config, base_url)
#                 all_urls.extend(course_urls)
                
#         finally:
#             await browser.close()
    
#     # Deduplicate (preserve order)
#     unique_urls = list(dict.fromkeys(all_urls))
    
#     # Get university display name
#     university_display_name = get_university_display_name(university_url)
    
#     # Save outputs as CSV
#     save_urls_to_csv(
#         urls=unique_urls,
#         university_name=university_display_name,
#         university_id=1,  # Default ID, can be customized per university
#         discovered_via="unified-extractor",
#         folder_name=folder_name,
#         filename=f"{folder_name}_courses.csv"
#     )
    
#     # # Also save pagination URLs as CSV (for reference)
#     # save_urls_to_csv(
#     #     urls=pagination_urls,
#     #     university_name=university_display_name,
#     #     university_id=1,
#     #     discovered_via="unified-extractor",
#     #     folder_name=folder_name,
#     #     filename=f"{folder_name}_pagination.csv"
#     # )
    
#     # # Filter if keywords provided
#     # filter_keywords = config.get("filter_keywords", [])
#     # match_mode = config.get("match_mode", "contains")
#     # if filter_keywords:
#     #     filtered_urls = filter_links_by_keywords(
#     #         links=unique_urls,
#     #         keywords=filter_keywords,
#     #         filename=f"{folder_name}_filtered_courses.csv",
#     #         folder_name=folder_name,
#     #         match_mode=match_mode,
#     #         university_name=university_display_name,
#     #         university_id=1,
#     #         save_as_csv=True
#     #     )
#     # else:
#     #     # Save empty filtered CSV
#     #     save_urls_to_csv(
#     #         urls=[],
#     #         university_name=university_display_name,
#     #         university_id=1,
#     #         discovered_via="unified-extractor",
#     #         folder_name=folder_name,
#     #         filename=f"{folder_name}_filtered_courses.csv"
#     #     )
    
#     return len(unique_urls), unique_urls


# # Backward compatibility: Keep old function name for Abertay
# async def scrape_abertay_courses_async() -> Tuple[int, List[str]]:
#     """Scrape Abertay courses (async version for backward compatibility)."""
#     url = "https://www.abertay.ac.uk/course-search/?keywords=course"
#     return await scrape_university_courses(url)


# def scrape_university_courses_sync(university_url: str) -> Tuple[int, List[str]]:
#     """
#     Synchronous wrapper for scrape_university_courses (for use in Streamlit).
    
#     Args:
#         university_url: URL of the university course page
        
#     Returns:
#         Tuple of (total_count, unique_urls)
#     """
#     return asyncio.run(scrape_university_courses(university_url))


# def scrape_abertay_courses() -> Tuple[int, List[str]]:
#     """
#     Scrape all course URLs from Abertay course search (sync wrapper for backward compatibility).
    
#     Returns:
#         Tuple of (total_count, unique_urls)
#     """
#     url = "https://www.abertay.ac.uk/course-search/?keywords=course"
#     return scrape_university_courses_sync(url)
#################################### V2 ##############################
"""Unified course link extraction module for multiple universities."""
import os
import sys
import asyncio
import re
import csv
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any
from urllib.parse import urlparse, parse_qs, unquote, urljoin, urlencode, urlsplit, urlunsplit

# Fix for Windows Python 3.13+ asyncio subprocess issues with Playwright
# WindowsProactorEventLoopPolicy supports subprocess operations (required by Playwright)
# WindowsSelectorEventLoopPolicy does NOT support subprocess operations
if sys.platform.startswith('win'):
    if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    elif hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
        # Fallback if Proactor is not available (older Python versions)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from playwright.async_api import async_playwright, Page, TimeoutError as PWTimeoutError
from university_config import get_config_for_url, get_university_display_name, UNIVERSITY_CONFIGS


# -----------------------------
# Constants
# -----------------------------
OUTPUT_MAIN_FOLDER = "output_links_files"
MAX_PAGES = 100  # Maximum pages to prevent infinite loops
PAGE_LOAD_TIMEOUT = 60000
PAGINATION_DELAY = 1000


# -----------------------------
# Utility Functions
# -----------------------------

def _ensure_output_dirs(folder_name: str) -> str:
    """
    Ensure output directories exist.
    
    Args:
        folder_name: Name of the subfolder to create
        
    Returns:
        Path to the created subfolder
    """
    main_folder = OUTPUT_MAIN_FOLDER
    os.makedirs(main_folder, exist_ok=True)
    subfolder = os.path.join(main_folder, folder_name)
    os.makedirs(subfolder, exist_ok=True)
    return subfolder


def save_list_to_file(filename: str, items: List[str], folder_name: str) -> str:
    """
    Save a list of items to a file (legacy function for backward compatibility).
    
    Args:
        filename: Name of the file to save
        items: List of strings to save
        folder_name: Name of the subfolder
        
    Returns:
        Full path to the saved file
    """
    subfolder = _ensure_output_dirs(folder_name)
    full_path = os.path.join(subfolder, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(str(item) + "\n")
    return full_path


def save_urls_to_csv(
    urls: List[str],
    university_name: str,
    university_id: Optional[int] = None,
    discovered_via: str = "unified-extractor",
    folder_name: Optional[str] = None,
    filename: Optional[str] = None
) -> str:
    """
    Save URLs to CSV file matching the export structure.
    
    Args:
        urls: List of course URLs to save
        university_name: Name of the university
        university_id: Optional university ID (defaults to 1 if not provided)
        discovered_via: How the URLs were discovered (default: "unified-extractor")
        folder_name: Optional folder name (defaults to university_name)
        filename: Optional filename (defaults to "{university_name}_courses.csv")
        
    Returns:
        Full path to the saved CSV file
    """
    if university_id is None:
        university_id = 1  # Default ID
    
    if folder_name is None:
        folder_name = university_name.lower().replace(" ", "_")
    
    if filename is None:
        filename = f"{folder_name}_courses.csv"
    
    subfolder = _ensure_output_dirs(folder_name)
    full_path = os.path.join(subfolder, filename)
    
    # Get current timestamp
    extracted_at = datetime.now().isoformat()
    
    # Prepare CSV data
    csv_data = []
    for idx, url in enumerate(urls):
        csv_data.append({
            "": idx,  # Index column
            "url": url,
            "university_id": university_id,
            "university_name": university_name,
            "discovered_via": discovered_via,
            "link_group_type": "",  # Empty as per CSV structure
            "confidence_score": "",  # Empty as per CSV structure
            "status": "pending",
            "extracted_at": extracted_at,
            "error_message": ""
        })
    
    # Write CSV file
    if csv_data:
        fieldnames = ["", "url", "university_id", "university_name", "discovered_via", 
                     "link_group_type", "confidence_score", "status", "extracted_at", "error_message"]
        with open(full_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        print(f"[✔] Saved {len(urls)} URLs to CSV: {full_path}")
    else:
        # Create empty CSV with headers
        fieldnames = ["", "url", "university_id", "university_name", "discovered_via", 
                     "link_group_type", "confidence_score", "status", "extracted_at", "error_message"]
        with open(full_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        print(f"[✔] Created empty CSV: {full_path}")
    
    return full_path


def filter_links_by_keywords(
    links: List[str],
    keywords: List[str],
    filename: str,
    folder_name: str,
    match_mode: str = "contains",
    university_name: Optional[str] = None,
    university_id: Optional[int] = None,
    save_as_csv: bool = True
) -> List[str]:
    """
    Filter links by keywords and save to CSV file.
    
    Args:
        links: List of URLs to filter
        keywords: List of keywords to match against
        filename: Output filename (will be converted to .csv if save_as_csv=True)
        folder_name: Name of the subfolder
        match_mode: "contains" or "segment"
        university_name: University name for CSV (defaults to folder_name)
        university_id: University ID for CSV (defaults to 1)
        save_as_csv: Whether to save as CSV (True) or text file (False)
        
    Returns:
        List of filtered URLs
    """
    if not keywords:
        if save_as_csv:
            # Save empty CSV
            csv_filename = filename.replace(".txt", ".csv") if filename.endswith(".txt") else filename
            if not csv_filename.endswith(".csv"):
                csv_filename += ".csv"
            save_urls_to_csv(
                [],
                university_name or folder_name,
                university_id,
                "unified-extractor",
                folder_name,
                csv_filename
            )
        else:
            save_list_to_file(filename, [], folder_name)
        return []

    filtered = []
    keyword_list = [kw.lower().strip() for kw in keywords if kw]

    for url in links:
        if not isinstance(url, str):
            continue
        try:
            path = urlparse(url).path.lower()
        except Exception:
            path = url.lower()

        match = False
        for kw in keyword_list:
            if not kw:
                continue
            if match_mode == "segment":
                segments = [s for s in path.strip("/").split("/") if s]
                if kw.strip("/") in segments:
                    match = True
                    break
            else:  # 'contains'
                if kw in path:
                    match = True
                    break
        if match:
            filtered.append(url)

    if save_as_csv:
        # Save filtered results as CSV
        csv_filename = filename.replace(".txt", ".csv") if filename.endswith(".txt") else filename
        if not csv_filename.endswith(".csv"):
            csv_filename += ".csv"
        save_urls_to_csv(
            filtered,
            university_name or folder_name,
            university_id,
            "unified-extractor",
            folder_name,
            csv_filename
        )
    else:
        save_list_to_file(filename, filtered, folder_name)
    
    return filtered


# -----------------------------
# Unified Scraper Functions
# -----------------------------

async def _extract_course_links(
    page: Page,
    config: Dict[str, Any],
    base_url: str
) -> List[str]:
    """
    Extract course links from current page using config selector.
    
    Args:
        page: Playwright page object
        config: University configuration
        base_url: Base URL for resolving relative links
        
    Returns:
        List of course URLs
    """
    course_urls = []
    selector = config.get("course_selector")
    if not selector:
        return course_urls
    
    try:
        # Wait for selector if specified
        wait_selector = config.get("wait_selector", selector)
        if wait_selector:
            try:
                await page.wait_for_selector(wait_selector, timeout=20000)
            except PWTimeoutError:
                pass  # Continue anyway
        
        # Extract links based on selector
        elements = await page.query_selector_all(selector)
        
        url_resolution = config.get("url_resolution")
        special_logic = config.get("special_logic")
        
        for el in elements:
            try:
                if special_logic == "generate_slug_from_title":
                    # York College: Generate URL from title
                    title = await el.inner_text()
                    if title:
                        slug = re.sub(r'[^a-z0-9\s]', '', title.lower())
                        slug = re.sub(r'\s+', '-', slug)
                        slug = re.sub(r'-+', '-', slug).strip('-')
                        if slug and len(slug) >= 3:
                            parsed = urlparse(base_url)
                            course_url = f"{parsed.scheme}://{parsed.netloc}/academics/programs/{slug}"
                            course_urls.append(course_url)
                elif selector == "div.listing-item__header.test a[data-live-url]":
                    # Otago: Extract from data-live-url attribute
                    href = await el.get_attribute("data-live-url")
                    if href:
                        course_urls.append(href.strip())
                else:
                    # Standard: Extract href attribute
                    href = await el.get_attribute("href")
                    if not href:
                        continue
                    
                    # Resolve URL using resolution function if provided
                    if url_resolution:
                        resolved = url_resolution(href, base_url)
                        if resolved:
                            course_urls.append(resolved)
                    else:
                        # Standard URL join
                        full_url = urljoin(base_url, href)
                        course_urls.append(full_url)
            except Exception:
                continue  # Skip malformed URLs
                
    except Exception as e:
        print(f"Error extracting course links: {e}")
    
    return course_urls


async def _handle_next_button_pagination(
    page: Page,
    config: Dict[str, Any],
    current_url: str,
    visited_urls: List[str]
) -> Optional[str]:
    """
    Handle pagination using next button.
    
    Returns:
        Next URL if available, None otherwise
    """
    selector = config.get("pagination_selector")
    if not selector:
        return None
    
    try:
        # Check if next button exists and is enabled
        next_button = await page.query_selector(selector)
        if not next_button:
            return None
        
        # Check if disabled (various ways)
        is_disabled = await next_button.is_disabled() if hasattr(next_button, 'is_disabled') else False
        class_attr = await next_button.get_attribute("class") or ""
        aria_disabled = await next_button.get_attribute("aria-disabled")
        
        if is_disabled or "disabled" in class_attr.lower() or aria_disabled == "true":
            return None
        
        # Get next URL
        next_href = await next_button.get_attribute("href")
        if not next_href or next_href in ["", "#", "javascript:void(0)"]:
            # Try clicking and getting new URL
            try:
                await next_button.click()
                await page.wait_for_timeout(config.get("pagination_delay", PAGINATION_DELAY))
                new_url = page.url
                if new_url != current_url and new_url not in visited_urls:
                    return new_url
            except Exception:
                pass
            return None
        
        # Resolve next URL
        next_url = urljoin(current_url, next_href)
        if next_url == current_url or next_url in visited_urls:
            return None
        
        return next_url
        
    except Exception:
        return None


async def _handle_page_numbers_pagination(
    page: Page,
    config: Dict[str, Any],
    base_url: str
) -> List[str]:
    """
    Handle pagination by extracting total page count and generating URLs.
    
    Returns:
        List of pagination URLs
    """
    pagination_urls = []
    selector = config.get("pagination_selector")
    param = config.get("pagination_param", "page")
    
    try:
        if selector:
            await page.wait_for_selector(selector, timeout=30000)
            
            # Extract total pages
            total_pages = 1
            try:
                # Try extracting from text (e.g., "Page 1 of 22")
                text = await page.locator(selector).inner_text()
                pattern = config.get("pagination_extract_pattern", r"of\D*(\d+)")
                match = re.search(pattern, text.replace("\xa0", " ").replace("Page", ""))
                if match:
                    total_pages = int(match.group(1))
                else:
                    # Fallback: count options in select
                    option_count = await page.locator(f"select[aria-label*='page'] option").count()
                    if option_count > 0:
                        total_pages = option_count
            except Exception:
                total_pages = 1
            
            # Generate pagination URLs
            parsed = urlparse(base_url)
            base_path = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            query_params = parse_qs(parsed.query, keep_blank_values=True)
            
            for i in range(1, total_pages + 1):
                if i == 1:
                    pagination_urls.append(base_url)
                else:
                    query_params[param] = [str(i - 1)] if "shu.ac.uk" in base_url else [str(i)]
                    query_string = urlencode(query_params, doseq=True)
                    pagination_urls.append(f"{base_path}?{query_string}")
        else:
            pagination_urls.append(base_url)
            
    except Exception as e:
        print(f"Error extracting page numbers: {e}")
        pagination_urls.append(base_url)
    
    return pagination_urls


async def _handle_url_params_pagination(
    page: Page,
    config: Dict[str, Any],
    base_url: str
) -> List[str]:
    """
    Handle pagination by modifying URL parameters.
    
    Returns:
        List of pagination URLs
    """
    pagination_urls = []
    param = config.get("pagination_param", "page")
    increment = config.get("pagination_increment", 1)
    start_value = config.get("pagination_start", 1)
    
    # For Canterbury, we need to detect when to stop
    if "canterbury.ac.nz" in base_url:
        # Canterbury uses start_rank parameter
        current_rank = start_value
        max_pages = 50  # Safety limit
        
        for page_num in range(1, max_pages + 1):
            if page_num == 1:
                pagination_urls.append(base_url)
            else:
                url = f"{base_url}&start_rank={current_rank}"
                pagination_urls.append(url)
                current_rank += increment
    else:
        # Standard URL param pagination
        parsed = urlparse(base_url)
        base_path = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        
        for i in range(1, MAX_PAGES + 1):
            if i == 1:
                pagination_urls.append(base_url)
            else:
                query_params[param] = [str(i - 1)]
                query_string = urlencode(query_params, doseq=True)
                pagination_urls.append(f"{base_path}?{query_string}")
    
    return pagination_urls


async def _handle_accordion_pagination(
    page: Page,
    config: Dict[str, Any]
) -> bool:
    """
    Handle accordion-style pagination by expanding sections.
    
    Returns:
        True if accordion was handled
    """
    selector = config.get("pagination_selector")
    if not selector:
        return False
    
    try:
        accordion_buttons = await page.query_selector_all(selector)
        for btn in accordion_buttons:
            try:
                aria_expanded = await btn.get_attribute("aria-expanded")
                if aria_expanded != "true":
                    await btn.click()
                    await page.wait_for_timeout(1000)  # Wait for accordion to expand
            except Exception:
                continue
        return True
    except Exception:
        return False


async def scrape_university_courses(university_url: str) -> Tuple[int, List[str]]:
    """
    Unified function to scrape course URLs from any configured university.
    
    Args:
        university_url: URL of the university course page
        
    Returns:
        Tuple of (total_count, unique_urls)
        
    Raises:
        ValueError: If university is not configured
    """
    # Get configuration for this university
    config = get_config_for_url(university_url)
    if not config:
        raise ValueError(f"University URL '{university_url}' is not configured. "
                        f"Available universities: {', '.join(UNIVERSITY_CONFIGS.keys())}")
    
    folder_name = config.get("folder_name", "unknown")
    pagination_type = config.get("pagination_type", "single_page")
    
    # Windows Python 3.13+ fix: Ensure ProactorEventLoopPolicy is set before Playwright creates subprocess
    if sys.platform.startswith('win'):
        if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
            policy = asyncio.WindowsProactorEventLoopPolicy()
            asyncio.set_event_loop_policy(policy)
    
    all_urls = []
    pagination_urls = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-extensions"
            ]
        )
        try:
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            page.set_default_timeout(PAGE_LOAD_TIMEOUT)
            
            # Parse base URL
            parsed = urlparse(university_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            
            # Handle different pagination types
            if pagination_type == "single_page":
                # Single page - no pagination
                await page.goto(university_url, wait_until="domcontentloaded")
                pagination_urls.append(university_url)
                course_urls = await _extract_course_links(page, config, base_url)
                all_urls.extend(course_urls)
                
            elif pagination_type == "accordion":
                # Accordion - expand all sections
                await page.goto(university_url, wait_until="domcontentloaded")
                pagination_urls.append(university_url)
                await _handle_accordion_pagination(page, config)
                course_urls = await _extract_course_links(page, config, base_url)
                all_urls.extend(course_urls)
                
            elif pagination_type == "page_numbers":
                # Extract total pages and generate URLs
                await page.goto(university_url, wait_until="domcontentloaded")
                pagination_urls = await _handle_page_numbers_pagination(page, config, university_url)
                
                # Scrape each page
                for pag_url in pagination_urls:
                    try:
                        await page.goto(pag_url, wait_until="domcontentloaded")
                        course_urls = await _extract_course_links(page, config, base_url)
                        all_urls.extend(course_urls)
                        await asyncio.sleep(0.5)  # Small delay between pages
                    except Exception as e:
                        print(f"Error scraping page {pag_url}: {e}")
                        continue
                        
            elif pagination_type == "url_params":
                # Generate URLs with different parameters
                pagination_urls = await _handle_url_params_pagination(page, config, university_url)
                
                # Scrape each page
                for pag_url in pagination_urls:
                    try:
                        await page.goto(pag_url, wait_until="domcontentloaded")
                        
                        # Handle cookies/overlays if needed
                        if "canterbury.ac.nz" in pag_url:
                            try:
                                accept_btn = await page.get_by_role("button", name=re.compile(r"Accept|Agree", re.I)).first
                                if await accept_btn.is_visible(timeout=5000):
                                    await accept_btn.click()
                                    await page.wait_for_timeout(1000)
                            except:
                                pass
                        
                        course_urls = await _extract_course_links(page, config, base_url)
                        all_urls.extend(course_urls)
                        # For Canterbury, stop if no results found
                        if "canterbury.ac.nz" in pag_url and not course_urls:
                            break
                        await asyncio.sleep(1)  # Delay for Canterbury
                    except Exception as e:
                        print(f"Error scraping page {pag_url}: {e}")
                        continue
                        
            elif pagination_type == "next_button":
                # Click next button repeatedly
                current_url = university_url
                visited_urls = []
                page_count = 0
                
                while page_count < MAX_PAGES:
                    try:
                        await page.goto(current_url, wait_until="domcontentloaded")
                        pagination_urls.append(current_url)
                        visited_urls.append(current_url)
                        
                        course_urls = await _extract_course_links(page, config, base_url)
                        all_urls.extend(course_urls)
                        
                        # Try to get next URL
                        next_url = await _handle_next_button_pagination(page, config, current_url, visited_urls)
                        if not next_url:
                            break
                        
                        current_url = next_url
                        page_count += 1
                        await asyncio.sleep(0.8)  # Delay between pages
                        
                    except Exception as e:
                        print(f"Error in pagination loop: {e}")
                        break
            else:
                # Unknown pagination type - treat as single page
                await page.goto(university_url, wait_until="domcontentloaded")
                pagination_urls.append(university_url)
                course_urls = await _extract_course_links(page, config, base_url)
                all_urls.extend(course_urls)
                
        finally:
            await browser.close()
    
    # Deduplicate (preserve order)
    unique_urls = list(dict.fromkeys(all_urls))
    
    # Get university display name
    university_display_name = get_university_display_name(university_url)
    
    # Save outputs as CSV
    full_path = save_urls_to_csv(
        urls=unique_urls,
        university_name=university_display_name,
        university_id=1,  # Default ID, can be customized per university
        discovered_via="unified-extractor",
        folder_name=folder_name,
        filename=f"{folder_name}_courses.csv"
    )
    
    # # Also save pagination URLs as CSV (for reference)
    # save_urls_to_csv(
    #     urls=pagination_urls,
    #     university_name=university_display_name,
    #     university_id=1,
    #     discovered_via="unified-extractor",
    #     folder_name=folder_name,
    #     filename=f"{folder_name}_pagination.csv"
    # )
    
    # # Filter if keywords provided
    # filter_keywords = config.get("filter_keywords", [])
    # match_mode = config.get("match_mode", "contains")
    # if filter_keywords:
    #     filtered_urls = filter_links_by_keywords(
    #         links=unique_urls,
    #         keywords=filter_keywords,
    #         filename=f"{folder_name}_filtered_courses.csv",
    #         folder_name=folder_name,
    #         match_mode=match_mode,
    #         university_name=university_display_name,
    #         university_id=1,
    #         save_as_csv=True
    #     )
    # else:
    #     # Save empty filtered CSV
    #     save_urls_to_csv(
    #         urls=[],
    #         university_name=university_display_name,
    #         university_id=1,
    #         discovered_via="unified-extractor",
    #         folder_name=folder_name,
    #         filename=f"{folder_name}_filtered_courses.csv"
    #     )
    
    return len(unique_urls), unique_urls, full_path


# Backward compatibility: Keep old function name for Abertay
async def scrape_abertay_courses_async() -> Tuple[int, List[str]]:
    """Scrape Abertay courses (async version for backward compatibility)."""
    url = "https://www.abertay.ac.uk/course-search/?keywords=course"
    return await scrape_university_courses(url)


def scrape_university_courses_sync(university_url: str) -> Tuple[int, List[str]]:
    """
    Synchronous wrapper for scrape_university_courses (for use in Streamlit).
    
    Args:
        university_url: URL of the university course page
        
    Returns:
        Tuple of (total_count, unique_urls)
    """
    return asyncio.run(scrape_university_courses(university_url))


def scrape_abertay_courses() -> Tuple[int, List[str]]:
    """
    Scrape all course URLs from Abertay course search (sync wrapper for backward compatibility).
    
    Returns:
        Tuple of (total_count, unique_urls)
    """
    url = "https://www.abertay.ac.uk/course-search/?keywords=course"
    return scrape_university_courses_sync(url)
