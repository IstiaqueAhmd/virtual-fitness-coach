"""AI service for generating fitness coach responses."""

from google import genai
from typing import List, Dict
from config import GEMINI_API_KEY


class FitnessCoachAI:
    """Handles AI responses for the virtual fitness coach."""
    
    def __init__(self):
        self.client = genai.Client()
    
    def _build_context(self, messages: List[Dict]) -> str:
        """Build context string from chat history."""
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
    
    def _build_prompt(self, context: str) -> str:
        """Build the full prompt for the AI model."""
        return f"""You are a helpful virtual fitness coach. Provide encouraging, informative, and personalized fitness advice.
        
Previous conversation:
{context}

Please respond to the user's latest message in a friendly and supportive manner."""
    
    async def generate_response(self, user_message: str, chat_history: List[Dict]) -> str:
        """Generate an AI response based on user message and chat history."""
        try:
            context = self._build_context(chat_history)
            prompt = self._build_prompt(context)
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",  
                contents=prompt,
            )
            
            return response.text
        except Exception as e:
            raise Exception(f"Error generating AI response: {str(e)}")


# Global AI service instance
ai_service = FitnessCoachAI()
