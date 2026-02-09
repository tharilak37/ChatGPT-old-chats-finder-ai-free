from index import load_chats, filter_candidates
from gemini_ranker import rank_with_gemini
from config import MAX_CANDIDATES

def main():
    print("=== ChatGPT Chat Finder ===\n")

    user_intent = input("Describe what you are trying to find:\n> ")

    tags = input("\nEnter tags (comma separated):\n> ")
    tags = [t.strip().lower() for t in tags.split(",") if t.strip()]

    conversations = load_chats("data/conversations.json")
    print(f"Loaded {len(conversations)} conversations")
    candidates = filter_candidates(conversations, tags)

    if not candidates:
        print("\n❌ No matches found.")
        return

    candidates = candidates[:MAX_CANDIDATES]

    print(f"\n🔍 {len(candidates)} candidates found. Sending to Gemini...\n")

    result = rank_with_gemini(user_intent, candidates)
    print("=== TOP RESULTS ===")
    print(result)

if __name__ == "__main__":
    main()
