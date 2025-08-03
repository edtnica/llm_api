# from flask import Flask, request, jsonify
# import openai
# import os

# app = Flask(__name__)

# # Set your OpenRouter API key (store in environment or paste directly for testing)
# # openai.api_key = os.getenv("OPENROUTER_API_KEY")
# openai.api_key = "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"
# openai.api_base = "https://openrouter.ai/api/v1"

# @app.route("/summarize_reviews", methods=["POST"])
# def summarize_reviews():
#     data = request.get_json()
#     reviews = data.get("reviews", [])

#     if not reviews:
#         return jsonify({"summary": "No reviews provided."}), 400

#     prompt = (
#         "Summarize the following user reviews into a short, accessible description "
#         "focusing on wheelchair accessibility, facilities, and general experience:\n\n"
#         + "\n".join(f"- {r}" for r in reviews)
#     )

#     try:
#         response = openai.ChatCompletion.create(
#             model="deepseek/deepseek-chat-v3-0324:free",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7
#         )
#         summary = response.choices[0].message.content.strip()
#         return jsonify({"summary": summary})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Set up OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    # api_key=os.getenv("OPENROUTER_API_KEY")
    api_key="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"
)

@app.route("/")
def home():
    return "Flask server is working!"

@app.route("/summarize_reviews", methods=["POST"])
def summarize_reviews():
    data = request.get_json()
    reviews = data.get("reviews", [])

    if not reviews:
        return jsonify({"summary": "No reviews provided."}), 400

    # prompt = (
    #     "Summarize the following user reviews into a short, accessible description "
    #     "focusing on wheelchair accessibility, facilities, and general experience:\n\n"
    #     + "\n".join(f"- {r}" for r in reviews)
    # )

    # prompt = (
    #     "You are an impartial summarizer. Do not include personal opinions, questions, or instructions. "
    #     "Summarize the following user reviews in a neutral and informative tone. "
    #     "Structure your summary using three clear sections: 'Accessibility & Experience', 'Facilities', and 'General Impressions'. "
    #     "Avoid conversational phrases like 'Let me know' or 'you might'.\n\n"
    #     + "\n".join(f"- {r}" for r in reviews)
    # )

    prompt = (
        "You are an impartial summarizer. Do not include personal opinions, questions, or instructions. "
        "Summarize the following user reviews in a neutral and informative tone. "
        "Structure your summary using three bolded section headings: **Accessibility & Experience**, **Facilities**, and **General Impressions**. "
        "Use plain text (not HTML). Avoid conversational phrases like 'Let me know' or 'you might'.\n\n"
        + "\n".join(f"- {r}" for r in reviews)
    )



    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",  # or any available model
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": "http://localhost:5000",  # Optional
                "X-Title": "NaviWheel App",
            },
        )

        summary = completion.choices[0].message.content.strip()
        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
