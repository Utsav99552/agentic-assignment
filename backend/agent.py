from openai import OpenAI
import os

# FIX: Do NOT create the client at module level.
# If CEREBRAS_API_KEY is missing, OpenAI() raises immediately and crashes
# uvicorn before the app even starts. Create the client lazily inside the
# function so the server boots fine; the error only surfaces when a request
# is actually made (and is caught by the try/except below).
_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("CEREBRAS_API_KEY")
        if not api_key:
            raise ValueError(
                "CEREBRAS_API_KEY environment variable is not set. "
                "Run: export CEREBRAS_API_KEY=your_key_here"
            )
        _client = OpenAI(
            api_key=api_key,
            base_url="https://api.cerebras.ai/v1"
        )
    return _client


def ask_agent(content, query):

    prompt = f"""
You are an Agentic AI Assistant.

Content:
{content}

User Query:
{query}

Rules:

1. If the query asks for a summary:
   Return:
   - One Line Summary
   - 3 Bullet Points
   - 5 Sentence Summary

2. If the query asks for sentiment:
   Return:
   - Sentiment
   - Confidence
   - Justification

3. If the query asks for code analysis:
   Return:
   - Explanation
   - Bugs
   - Time Complexity

4. If the query asks for technical skills:
   Extract all technical skills in bullet points.

5. If the query asks to compare documents:
   Compare them in a structured table format.

6. If the query asks for strengths:
   Identify key strengths.

7. If the query asks for weaknesses:
   Identify areas of improvement.

8. If the query asks to explain a resume:
   Explain:
   - Education
   - Skills
   - Projects
   - Experience
   - Achievements

9. If multiple documents are uploaded and the query is ambiguous:
   Ask which document should be analyzed.

10. Always provide clear, structured, and professional answers.

11. Never return HTML tags.
Use proper markdown formatting only.

12. When comparing resumes:
   - Comparison Table
   - Strengths
   - Weaknesses
   - Recommendation
"""

    try:
        response = _get_client().chat.completions.create(
            model="gpt-oss-120b",   # Current Cerebras production model (as of 2025)
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"