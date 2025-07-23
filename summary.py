import time
import requests
import os
from dotenv import load_dotenv # Import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Required constants for Google Gemini API
# Get API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 
# Gemini API endpoint for generateContent
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
# Using gemini-2.0-flash as the model
GEMINI_MODEL = "gemini-2.0-flash" 
HEADERS = {
    "Content-Type": "application/json",
}

# Example helper class and function
class Website:
    def __init__(self, title, text):
        self.title = title
        self.text = text

# System prompt for the LLM to guide its behavior
SYSTEM_PROMPT = (
    "You are an assistant that analyzes the contents of a website "
    "and provides a concise, accurate, and beautifully formatted summary. "
    "Use clear markdown with headings and bullet points. "
    "Do NOT use bold formatting (e.g., do not use '**') anywhere in the output. "
    "Ignore navigation-related text. Focus on the main content, key topics, and any important announcements."
)

def messages_for(website):
    # Construct the user prompt with website title and text
    user_prompt = (
        f"You are looking at a website titled '{website.title}'.\n"
        "The contents of this website are as follows; please provide a short summary of this website in markdown. "
        "If it includes news or announcements, then summarize these too.\n\n"
        + website.text
    )
    # Gemini API uses 'parts' for content
    return [
        {"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}, # System prompt as a user part for Gemini
        {"role": "user", "parts": [{"text": user_prompt}]}
    ]

def summarize(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    # Added arguments to improve stability in headless environments
    chrome_options.add_argument("--remote-debugging-port=9222") # Specify a fixed debugging port
    chrome_options.add_argument("--disable-setuid-sandbox") # Disable setuid sandbox
    chrome_options.add_argument("--single-process") # Run in a single process
    chrome_options.add_argument("--disable-features=NetworkService") # Disable network service
    chrome_options.add_argument("--disable-features=VizDisplayCompositor") # Disable VizDisplayCompositor


    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(2) # Consider replacing with explicit waits for better performance

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    for tag in soup(["img", "style", "script", "nav", "footer", "header", "button", "input", "svg", "a"]):
        tag.decompose()
    for unwanted in soup.select(".navbar, .menu, .sidebar, .ad-banner"):
        unwanted.decompose()

    title = soup.title.string if soup.title else "No Title"
    text = soup.get_text(separator="\n", strip=True)

    website = Website(title, text)
    
    # Gemini API payload structure
    payload = {
        "contents": messages_for(website),
        "generationConfig": {
            "temperature": 0.7, # Example generation config, adjust as needed
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 800,
        }
    }

    try:
        # Append API key to the URL for Gemini
        api_url_with_key = f"{GEMINI_API_URL}?key={GOOGLE_API_KEY}"
        response = requests.post(api_url_with_key, json=payload, headers=HEADERS)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()

        # Extract content from Gemini's generateContent response format
        if result and "candidates" in result and len(result["candidates"]) > 0 and \
           "content" in result["candidates"][0] and "parts" in result["candidates"][0]["content"] and \
           len(result["candidates"][0]["content"]["parts"]) > 0 and "text" in result["candidates"][0]["content"]["parts"][0]:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"⚠️ Unexpected API response structure from Google Gemini:\n{result}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error communicating with Google Gemini API: {str(e)}"
    except Exception as e:
        return f"❌ An unexpected error occurred during summarization: {str(e)}"

