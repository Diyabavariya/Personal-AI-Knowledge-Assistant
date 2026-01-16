import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def llm_answer(question, context):
    prompt = f"""
You are an academic assistant.

Rules:
- Answer clearly and concisely
- No repetition
- For definitions: 2–3 lines
- For comparisons: use bullet points
- Keep it exam-oriented

Context:
{context}

Question:
{question}

Answer:
"""
    response = client.chat.completions.create(
       model="llama-3.1-8b-instant",
       messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()
