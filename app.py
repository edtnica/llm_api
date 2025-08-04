from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# API_KEY = os.getenv("OPENROUTER_API_KEY")
API_KEY = "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"

@app.route("/")
def index():
    return "✅ LLM Review Summarizer is running!"

@app.route("/summarize_reviews", methods=["POST"])
def summarize_reviews():
    data = request.get_json()
    reviews = data.get("reviews", [])

    print("📥 Received reviews:", reviews)

    if not reviews:
        return jsonify({"summary": "No reviews provided."}), 400

    prompt = (
        "You are an impartial summarizer. Do not include personal opinions, questions, or instructions. "
        "Summarize the following user reviews in a neutral and informative tone. "
        "Structure your summary using three bolded section headings: **Accessibility & Experience**, **Facilities**, and **General Impressions**. "
        "Use plain text (not HTML). Avoid conversational phrases like 'Let me know' or 'you might'.\n\n"
        + "\n".join(f"- {r}" for r in reviews)
    )

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://naviwheel.com",  # Optional
            "X-Title": "NaviWheel App"  # Optional
        }

        payload = {
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        print("📤 Raw response status:", response.status_code)
        print("📤 Raw response body:", response.text)

        if response.status_code != 200:
            return jsonify({"error": f"Error code: {response.status_code} - {response.text}"}), 500

        summary = response.json()["choices"][0]["message"]["content"].strip()
        print("✅ Summary generated successfully.")
        return jsonify({"summary": summary})

    except Exception as e:
        print("❌ Exception during summarization:", str(e))
        return jsonify({"error": str(e)}), 500


# Local development only
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
