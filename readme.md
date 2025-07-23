# Website Summarizer

Website Summarizer is a Flask web application that generates concise summaries of web pages using an LLM (via Ollama API). Users can input a URL, and the app will fetch, clean, and summarize the page content.

## Features

- Simple web interface for submitting URLs
- Uses Selenium and BeautifulSoup to extract and clean page text
- Sends content to an LLM (configured for Ollama) for summarization
- Displays the summary on the page

## Requirements

See [requirements.txt](requirements.txt) for dependencies:
- Flask
- selenium
- beautifulsoup4
- requests
- ipython
- jupyter

## Setup

1. Install Python 3.10+ and [ChromeDriver](https://chromedriver.chromium.org/downloads).
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Ensure Ollama is running locally and the model name in [`summary.py`](summary.py) matches your setup.

## Usage

1. Start the Flask app:
    ```sh
    python app.py
    ```
2. Open [http://localhost:5000](http://localhost:5000) in your browser.
3. Enter a URL and click "Summarize" to view the summary.

## File Structure

- [`app.py`](app.py): Flask web server
- [`summary.py`](summary.py): Summarization logic
- [`templates/index.html`](templates/index.html): Web UI template
- [`requirements.txt`](requirements.txt): Python dependencies

## Notes

- Requires Chrome browser and ChromeDriver for Selenium.
- The summarization uses the Ollama API; ensure it is running and accessible.