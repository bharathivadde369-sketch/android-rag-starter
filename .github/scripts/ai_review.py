import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

with open("pr_diff.txt", "r", encoding="utf-8") as file:
    diff = file.read()

diff = diff[:50000]

prompt = f"""
Act as a Principal Android Engineer.

Review this Android Pull Request.

Focus on:
- Scalability
- Performance
- Coroutine misuse
- Flow issues
- Compose recomposition
- MVVM/Clean Architecture
- Security concerns
- ANR risks
- Code readability
- Testing gaps

Give:
1. Blocking Issues
2. Suggestions
3. Nitpicks
4. Final Verdict

PR Diff:
{diff}
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a senior Android reviewer."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2
)

print(response.choices[0].message.content)
