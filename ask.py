from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate(text, lang):
    if lang == "jp":
        return f"日本語で次の質問に答えてください: {text}"
    return text  # Default: English

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = translate(data.get("prompt", ""), data.get("lang", "en"))

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response['choices'][0]['message']['content']

    # Optional image generation if needed
    image_url = None
    if "image" in prompt.lower():
        image_response = openai.Image.create(prompt=prompt, n=1, size="512x512")
        image_url = image_response['data'][0]['url']

    return jsonify({"response": text, "image_url": image_url})

if __name__ == '__main__':
    app.run(debug=True)