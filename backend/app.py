from flask import Flask, request, jsonify
from knowledge_base import KNOWLEDGE_BASE

app = Flask(__name__)


def retrieve_context(query: str) -> str:
    query_words = query.lower().split()
    matched_items = []

    for item in KNOWLEDGE_BASE:
        text = f"{item['title']} {item['content']}".lower()
        if any(word in text for word in query_words):
            matched_items.append(item["content"])

    if not matched_items:
        return "No relevant context found."

    return "\n".join(matched_items[:2])


def generate_answer(query: str, context: str) -> str:
    if context == "No relevant context found.":
        return f"I could not find enough context for: {query}"
    return f"Based on retrieved context for '{query}', here is the answer: {context}"


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query must not be empty."}), 400

    context = retrieve_context(query)
    answer = generate_answer(query, context)

    return jsonify({
        "answer": answer,
        "matchedContext": context
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
