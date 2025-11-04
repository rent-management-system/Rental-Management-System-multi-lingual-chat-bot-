import google.generativeai as genai
import os

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def get_status(self) -> Dict[str, Any]:
        """Get the status of the AI service."""
        # This is a placeholder. In a real application, you would check the health of the AI service.
        return {"status": "healthy"}

    async def generate_response(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response from Gemini: {e}")
            return ""
