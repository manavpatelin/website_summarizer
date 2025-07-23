from flask import Flask, render_template, request
from summary import summarize # Import your summarization function

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary_text = None
    if request.method == "POST":
        url = request.form.get("url_input")
        if url:
            try:
                summary_text = summarize(url)
            except Exception as e:
                summary_text = f"❌ Error during summarization: {str(e)}"
    return render_template("index.html", summary=summary_text)

if __name__ == "__main__":
    app.run(debug=True)