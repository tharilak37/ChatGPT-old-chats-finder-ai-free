import json
import re
from datetime import datetime

def load_chats(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # New ChatGPT export format (list)
    if isinstance(data, list):
        return data

    # Old format fallback
    if isinstance(data, dict) and "conversations" in data:
        return data["conversations"]

    raise ValueError("Unknown conversations.json format")


def extract_text(conv):
    texts = []

    for node in conv["mapping"].values():
        msg = node.get("message")
        if not msg:
            continue

        role = msg["author"]["role"]
        parts = msg["content"].get("parts", [])

        if role in ("user", "assistant"):
            for p in parts:
                if isinstance(p, str):
                    texts.append(p)

    return " ".join(texts)


def keyword_match(text, keywords):
    text = text.lower()
    return sum(1 for k in keywords if k in text)

def filter_candidates(conversations, tags, min_hits=1):
    candidates = []

    for conv in conversations:
        text = extract_text(conv)
        if not text:
            continue

        hits = keyword_match(text, tags)
        if hits >= min_hits:
            candidates.append({
                "id": conv["id"],
                "title": conv.get("title", "Untitled"),
                "text": text,
                "hits": hits
            })

    # prioritize by keyword hits
    candidates.sort(key=lambda x: x["hits"], reverse=True)
    return candidates
