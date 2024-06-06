from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    # URL to be opened in iframe
    url = "https://server.duinocoin.com/"
    # HTML content with iframe
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Preview</title>
    </head>
    <body>
        <iframe src="{url}" width="100%" height="100%"></iframe>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
