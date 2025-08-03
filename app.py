from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import httpx
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Use environment variable for safety
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

print("🔐 Loaded API key:", os.getenv("OPENROUTER_API_KEY"))

@app.route("/")
def index():
    return "✅ LLM Review Summarizer is running!"

import httpx

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
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://naviwheel.com",
            "X-Title": "NaviWheel App"
        }

        payload = {
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = httpx.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()

        summary = response.json()["choices"][0]["message"]["content"].strip()
        print("✅ Summary generated successfully.")
        return jsonify({"summary": summary})

    except Exception as e:
        print("❌ Error during summarization:", str(e))
        return jsonify({"error": str(e)}), 500



# Only used locally
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
