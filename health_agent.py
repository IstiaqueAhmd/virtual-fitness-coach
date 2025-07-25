"""Health agent for specialized fitness and health logic."""

from typing import List, Dict, Optional
from ai_service import AIService


class HealthAgent:
    """Specialized agent for health and fitness interactions."""
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
    
    def analyze_user_message(self, message: str) -> Dict[str, bool]:
        """Analyze user message for health-related intent."""
        message_lower = message.lower()
        
        analysis = {
            "is_workout_request": any(keyword in message_lower for keyword in 
                                    ["workout", "exercise", "training", "routine", "fitness"]),
            "is_nutrition_question": any(keyword in message_lower for keyword in 
                                       ["diet", "nutrition", "food", "calories", "meal", "eat"]),
            "is_health_concern": any(keyword in message_lower for keyword in 
                                   ["pain", "injury", "hurt", "doctor", "medical"]),
            "is_motivation_needed": any(keyword in message_lower for keyword in 
                                      ["tired", "unmotivated", "give up", "difficult", "hard"])
        }
        
        return analysis
    
    def create_specialized_prompt(self, message: str, context: str, analysis: Dict[str, bool]) -> str:
        """Create a specialized prompt based on message analysis."""
        base_prompt = f"""You are a helpful virtual fitness coach. Provide encouraging, informative, and personalized fitness advice.

Previous conversation:
{context}

User's latest message: {message}

"""
        
        if analysis["is_workout_request"]:
            base_prompt += "Focus on providing specific workout recommendations with proper form instructions and safety tips."
        elif analysis["is_nutrition_question"]:
            base_prompt += "Provide nutritional guidance while emphasizing the importance of consulting healthcare professionals for specific dietary needs."
        elif analysis["is_health_concern"]:
            base_prompt += "Address the concern with care and recommend consulting a healthcare professional for any medical issues."
        elif analysis["is_motivation_needed"]:
            base_prompt += "Focus on providing encouragement and motivation while offering practical tips to overcome challenges."
        
        base_prompt += "\n\nPlease respond in a friendly and supportive manner."
        
        return base_prompt
    
    async def generate_health_response(self, message: str, recent_messages: List[Dict]) -> str:
        """Generate a health-focused response."""
        analysis = self.analyze_user_message(message)
        context = self.ai_service.create_context_from_history(recent_messages)
        prompt = self.create_specialized_prompt(message, context, analysis)
        
        return await self.ai_service.generate_response(prompt)
