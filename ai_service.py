"""AI service integration for the Virtual Fitness Coach application."""

from typing import List, Dict
from google import genai
from config import GEMINI_API_KEY


class AIService:
    """Handles AI interactions with Gemini."""
    
    def __init__(self):
        self.client = genai.Client()
    
    def create_context_from_history(self, messages: List[Dict]) -> str:
        """Create context string from chat history."""
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
    
    def create_fitness_coach_prompt(self, context: str) -> str:
        """Create a fitness coach prompt with context."""
        return f"""You are a helpful virtual fitness coach. Provide encouraging, informative, and personalized fitness advice.
        
Previous conversation:
{context}

Please respond to the user's latest message in a friendly and supportive manner."""
    
    async def generate_response(self, prompt: str) -> str:
        """Generate AI response using Gemini."""
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
        )
        return response.text
    
    async def generate_fitness_response(self, recent_messages: List[Dict]) -> str:
        """Generate a fitness coach response based on chat history."""
        context = self.create_context_from_history(recent_messages)
        prompt = self.create_fitness_coach_prompt(context)
        return await self.generate_response(prompt)


# Global AI service instance
ai_service = AIService()


def get_ai_service() -> AIService:
    """Get the AI service instance."""
    return ai_service
