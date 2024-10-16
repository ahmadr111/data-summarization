import requests
from flask import Flask,render_template,url_for
from flask import request as req


app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def Index():
    return render_template("index.html")


@app.route("/Summarize", methods=["GET", "POST"])
def Summarize():
    if req.method == "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer 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"}

        try:
            data = req.form["data"]
            maxL = int(req.form["maxL"])
            minL = maxL // 4
        except KeyError as e:
            return "Error: Missing form field", 400
        except ValueError as e:
            return "Error: Invalid form data", 400
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        try:
            output = query({
                "inputs": data,
                "parameters": {"min_length": minL, "max_length": maxL},
            })[0]
            return render_template("index.html", result=output["summary_text"])
        except requests.exceptions.RequestException as e:
            return "Error: API request failed", 500
        except Exception as e:
            return "Error: Data processing failed - " + str(e), 500
    else:
        return render_template("index.html")
    
if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode
