from flask import Flask, render_template, request, jsonify
from summary import summarize
import threading

app = Flask(__name__)
summaries = {}

def summarize_async(url, key):
    try:
        summaries[key] = summarize(url)
    except Exception as e:
        summaries[key] = f"❌ Error during summarization: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    summary_text = None
    if request.method == "POST":
        url = request.form.get("url_input")
        if url:
            key = url  # Use URL as key, or generate a unique one
            if key not in summaries:
                thread = threading.Thread(target=summarize_async, args=(url, key))
                thread.start()
                summary_text = "⏳ Summarization in progress. Please refresh in a few seconds."
            else:
                summary_text = summaries[key]
    return render_template("index.html", summary=summary_text)

@app.route("/summary", methods=["POST"])
def get_summary():
    url = request.form.get("url_input")
    key = url
    return jsonify({"summary": summaries.get(key, "⏳ Summarization in progress.")})

if __name__ == "__main__":
    app.run(debug=True)