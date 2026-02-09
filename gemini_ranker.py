import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-2.5-flash")


def rank_with_gemini(user_intent, candidates):
    prompt = f"""
You are a relevance ranking engine.

User intent:
"{user_intent}"

Task:
From the candidate chats below, pick the TOP 3 most relevant.
Focus on conceptual relevance, not keyword frequency.

Rules:
- Prefer chats where the topic is the MAIN focus
- Ignore shallow mentions
- Return STRICT JSON ONLY
- Exactly 3 results

JSON format:
[
  {{ "id": "...", "reason": "..." }},
  {{ "id": "...", "reason": "..." }},
  {{ "id": "...", "reason": "..." }}
]

Candidates:
"""

    for i, c in enumerate(candidates, 1):
        prompt += f"""
Chat {i}
ID: {c['id']}
Title: {c['title']}
Content:
{c['text'][:1200]}
"""

    response = model.generate_content(prompt)
    return response.text
