from app.ai.clients.gemini import GeminiClient
from app.ai.prompts.summary_prompt import RESUME_SUMMARY_PROMPT

class SummaryGenerator:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client

    async def generate_summary(self, resume_text: str) -> str:
        """Generate recruiter-friendly summaries of raw resume content."""
        prompt = RESUME_SUMMARY_PROMPT.format(resume_text=resume_text)
        return await self.gemini_client.call_llm(prompt)
