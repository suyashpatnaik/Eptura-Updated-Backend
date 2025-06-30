import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def handler(request, response):
    try:
        body = json.loads(request.body)
        prompt = body.get("prompt", "")
        lang = body.get("lang", "en")

        if lang == "jp":
            prompt = f"日本語で次の質問に答えてください: {prompt}"

        result = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = result['choices'][0]['message']['content']

        image_url = None
        if "image" in prompt.lower():
            image_response = openai.Image.create(prompt=prompt, n=1, size="512x512")
            image_url = image_response['data'][0]['url']

        return response.status(200).json({
            "response": reply,
            "image_url": image_url
        })
    except Exception as e:
        return response.status(500).json({"error": str(e)})