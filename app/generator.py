import os
from groq import Groq
from dotenv import load_dotenv
from .prompts import get_prompt
from .vector_store import VectorStore

load_dotenv()

class ContentGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.vector_store = VectorStore()

    def generate(self, topic: str, report_type: str = "site_report", location: str = "Project Site", date: str = "Today"):
        # 1. Search for similar past reports for context
        similar_docs = self.vector_store.search_similar(topic)
        context = "\n\n".join(similar_docs) if similar_docs else ""

        # 2. Build the prompt
        prompt = get_prompt(report_type, topic=topic, location=location, date=date)
        if context:
            prompt = f"Reference examples from past reports:\n{context}\n\n---\n\n{prompt}"

        # 3. Call Groq API
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Free & powerful model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048
        )

        result = response.choices[0].message.content

        # 4. Save to vector DB for future reference
        doc_id = f"{report_type}_{topic[:30].replace(' ', '_')}"
        self.vector_store.add_document(doc_id, result, {"type": report_type, "topic": topic})

        return result