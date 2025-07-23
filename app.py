from flask import Flask, render_template, request
from summary import summarize

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    if request.method == "POST":
        url = request.form.get("url_input")
        if url:
            summary = summarize(url)
        else:
            summary = "⚠️ Please provide a URL."
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run()