from flask import Flask, request, jsonify
import base64
import json
import openai

openai.api_key = "your-openai-key"

app = Flask(__name__)

# Load scraped data
with open("discourse_data.json", "r") as f:
    discourse_data = json.load(f)

@app.route("/api/", methods=["POST"])
def answer_question():
    data = request.json
    question = data.get("question", "")
    image_b64 = data.get("image")

    prompt = f"""You are a helpful TA for Tools in Data Science.
Use the following Discourse posts and course notes to answer the student's question:\n\n"""

    for thread in discourse_data[:5]:  # Limit for speed
        prompt += f"### {thread['title']}\n"
        for post in thread['posts']:
            prompt += f"{post}\n"
    prompt += f"\nStudent Question: {question}\nAnswer:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    answer = response["choices"][0]["message"]["content"]

    return jsonify({
        "answer": answer,
        "links": []  # You can enhance with actual matching URLs if needed
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
