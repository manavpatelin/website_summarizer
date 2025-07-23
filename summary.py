import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options # Import Options 
from bs4 import BeautifulSoup

# Required constants
MODEL = "llama3.2"
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}

# Example helper class and function
class Website:
    def __init__(self, title, text):
        self.title = title
        self.text = text

def messages_for(website):
    return [{"role": "user", "content": f"Summarize this:\n\n{website.text}"}]

def summarize(url):
    chrome_options = Options() # Create an instance of Chrome options 
    # Run in headless mode (no visible browser UI) - highly recommended for server-side applications 
    chrome_options.add_argument("--headless")
    # Required for some environments (e.g., Docker, Linux servers) 
    chrome_options.add_argument("--no-sandbox")
    # Overcomes limited resource problems in environments like Docker containers 
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options) # Pass the configured options to the Chrome driver 
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit() # Ensure the driver quits to free up resources

    for tag in soup(["img", "style", "script", "nav", "footer", "header", "button", "input", "svg", "a"]):
        tag.decompose()
    for unwanted in soup.select(".navbar, .menu, .sidebar, .ad-banner"):
        unwanted.decompose()

    title = soup.title.string if soup.title else "No Title"
    text = soup.get_text(separator="\n", strip=True)

    website = Website(title, text)
    payload = {
        "model": MODEL,
        "messages": messages_for(website),
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
        result = response.json()
        if "message" in result and "content" in result["message"]:
            return result["message"]["content"]
        else:
            return f"⚠️ Unexpected API response:\n{result}"
    except Exception as e:
        return f"❌ Error during summarization:\n{str(e)}"