# utils.py
import json
from groq import Groq
import os
from dotenv import load_dotenv
import re

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_content(topic):
    prompt = f"""
    You are an AI assistant for content creators. Given the topic: "{topic}", provide:
    3 content ideas, each including:
      - title
      - a 500-word script
      - 5 relevant hashtags (list)
      - 3 SEO keywords (list)

    Return the response as a JSON array like:

    [
      {{
        "title": "...",
        "script": "...",
        "hashtags": ["#tag1", "#tag2", ...],
        "seo_keywords": ["keyword1", "keyword2", ...]
      }},
      ...
    ]
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )

    content = response.choices[0].message.content
    print("DEBUG: LLM response\n", content)

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        json_text_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_text_match:
            try:
                return json.loads(json_text_match.group(0))
            except:
                return []
        return []
