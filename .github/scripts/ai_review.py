import os
import sys
import requests
from openai import OpenAI

# ── Config ─────────────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN   = os.getenv("GITHUB_TOKEN")
REPO           = os.getenv("REPO")        # e.g. "org/android-rag-starter"
PR_NUMBER      = os.getenv("PR_NUMBER")   # e.g. "42"

MAX_DIFF_CHARS = 48_000  # leave room for prompt overhead within context window

# ── Validate env vars ──────────────────────────────────────────────────────────
missing = [v for v in ["OPENAI_API_KEY", "GITHUB_TOKEN", "REPO", "PR_NUMBER"]
           if not os.getenv(v)]
if missing:
    print(f"❌ Missing environment variables: {', '.join(missing)}")
    sys.exit(1)

# ── Read diff ──────────────────────────────────────────────────────────────────
try:
    with open("pr_diff.txt", "r", encoding="utf-8") as f:
        diff = f.read()
except FileNotFoundError:
    print("❌ pr_diff.txt not found.")
    sys.exit(1)

if not diff.strip():
    print("⚠️ Diff is empty — skipping review.")
    sys.exit(0)

# Truncate cleanly at a line boundary
if len(diff) > MAX_DIFF_CHARS:
    truncated = diff[:MAX_DIFF_CHARS].rsplit("\n", 1)[0]
    diff = truncated + "\n\n⚠️ [Diff truncated for token limit]"

# ── Build prompt ───────────────────────────────────────────────────────────────
prompt = f"""
Act as a Principal Android Engineer reviewing a Pull Request.

Focus on:
- Scalability & Performance
- Coroutine misuse (e.g. GlobalScope, blocking calls on Main thread)
- Flow issues (e.g. shareIn scope, cold vs hot streams)
- Jetpack Compose recomposition problems
- MVVM / Clean Architecture violations
- Security concerns (e.g. hardcoded keys, insecure storage)
- ANR risks (main thread blocking)
- Code readability & naming
- Testing gaps

Respond in this exact format:

## 🚨 Blocking Issues
(Must fix before merge — list each with file:line if visible)

## 💡 Suggestions
(Should fix — improvements that matter but aren't blockers)

## 🔍 Nitpicks
(Optional polish — style, naming, minor readability)

## ✅ Final Verdict
(One of: APPROVE / REQUEST CHANGES / NEEDS DISCUSSION — with 1-2 sentence summary)

PR Diff:
{diff}
"""

# ── Call OpenAI ────────────────────────────────────────────────────────────────
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior Android engineer. Be concise, specific, and actionable. "
                    "Reference file names and line numbers from the diff where possible."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=2000
    )
    review_text = response.choices[0].message.content
except Exception as e:
    print(f"❌ OpenAI API error: {e}")
    sys.exit(1)

print("✅ Review generated:\n")
print(review_text)

# ── Post comment to PR ─────────────────────────────────────────────────────────
comment_body = f"""## 🤖 AI Android Code Review

{review_text}

---
*Powered by GPT-4.1-mini · Review all suggestions carefully before acting on them.*
"""

url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

try:
    res = requests.post(url, json={"body": comment_body}, headers=headers)
    res.raise_for_status()
    print(f"✅ Review posted to PR #{PR_NUMBER}")
except requests.HTTPError:
    print(f"❌ GitHub API error: {res.status_code} — {res.text}")
    sys.exit(1)
