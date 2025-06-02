Website Summarizer
This project provides a simple web application and a Jupyter Notebook to summarize the content of a given URL using a local Ollama instance running the Llama 3.2 model.

Features
Web Application (Streamlit): A user-friendly interface to enter a URL and get a summary.
Jupyter Notebook: Allows for interactive development, testing, and detailed exploration of the summarization process.
Content Extraction: Utilizes selenium and BeautifulSoup to extract relevant text content from web pages, filtering out common noisy elements like navigation, footers, and advertisements.
LLM Integration: Sends the extracted web page content to a local Ollama API endpoint for summarization using the specified llama3.2 model.
Prerequisites
Before running this project, ensure you have the following installed:

Python 3.x
Ollama: Running locally with the llama3.2 model pulled. You can download Ollama from ollama.com.
Chrome Browser: selenium requires a Chrome browser installed on your system.
Installation
Clone the repository (or download the files):

Bash

git clone <repository_url>
cd <repository_name>
Install Python dependencies:

Bash

pip install -r requirements.txt
This will install selenium, beautifulsoup4, requests, streamlit, ipython, and jupyter.

Pull the Llama 3.2 model for Ollama:
Ensure your Ollama instance is running and then pull the model:

Bash

ollama pull llama3.2
Usage
1. Running the Streamlit Web Application
To start the web application, run the following command in your terminal:

Bash

streamlit run app.py
This will open the application in your web browser. Enter a URL in the provided input field, and the summarized content will be displayed below.

2. Using the Jupyter Notebook
To explore the summarization process interactively, you can use the provided Jupyter Notebook (summary.ipynb).

Start Jupyter Notebook:

Bash

jupyter notebook
Open summary.ipynb: Navigate to the summary.ipynb file in the Jupyter interface and open it.

Run the cells: Execute the cells sequentially to see how the web page content is extracted, processed, and then sent to Ollama for summarization. The notebook includes a display_summary function for a quick summary of a given URL.

An example usage within the notebook:

Python

if __name__ == "__main__":
    url = "https://www.tutorialspoint.com/machine_learning/index.htm"
    display_summary(url)
This will display a markdown-formatted summary of the provided URL.

Project Structure
app.py: The main Streamlit application file.
summary.py: Contains the core logic for web scraping, text extraction, and communication with the Ollama API.
summary.ipynb: A Jupyter Notebook demonstrating the summarization process interactively.
requirements.txt: Lists all the necessary Python dependencies.
