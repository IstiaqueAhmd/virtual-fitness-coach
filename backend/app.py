import os
from typing import List, Dict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("API key for Groq is missing. Please set the GROQ_API_KEY in the .env file.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=GROQ_API_KEY)


class FitnessProfile(BaseModel):
    age: int
    gender: str
    weight: float
    height: str
    fitness_goal: str
    equipment: List[str]
    injuries: List[str]
    days_per_week: int
    conversation_id: str


class Conversation:
    def __init__(self):
        self.messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": """You are an expert Fitness Coach. Generate personalized workout plans based on user profiles. Follow these rules:
1. Analyze the user's profile including age, gender, weight, height, fitness goal, equipment, injuries, and workout frequency
2. Create a structured weekly plan with daily workouts
3. For each exercise include: name, sets, reps, rest time
4. Adapt exercises to available equipment and avoid injury risks
5. Include brief form tips and safety notes
6. Use emojis for better readability
7. Format output with clear sections for each day"""
            }
        ]
        self.active: bool = True


conversations: Dict[str, Conversation] = {}


def query_groq_api(conversation: Conversation) -> str:
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=conversation.messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with Groq API: {str(e)}")


def get_or_create_conversation(conversation_id: str) -> Conversation:
    if conversation_id not in conversations:
        conversations[conversation_id] = Conversation()
    return conversations[conversation_id]


@app.post("/generate-plan/")
async def generate_plan(profile: FitnessProfile):
    conversation = get_or_create_conversation(profile.conversation_id)

    if not conversation.active:
        raise HTTPException(
            status_code=400,
            detail="This session has ended. Please start a new session with a new conversation_id."
        )

    try:
        # Build user profile message
        user_profile = f"""User Profile:
Age: {profile.age}
Gender: {profile.gender}
Weight: {profile.weight}
Height: {profile.height}
Fitness Goal: {profile.fitness_goal}
Available Equipment: {', '.join(profile.equipment) or 'None'}
Injuries/Health Conditions: {', '.join(profile.injuries) or 'None'}
Workout Days per Week: {profile.days_per_week}"""

        conversation.messages.append({
            "role": "user",
            "content": user_profile
        })

        response = query_groq_api(conversation)
        conversation.active = False  # End session after generation

        conversation.messages.append({
            "role": "assistant",
            "content": response
        })

        return {
            "workout_plan": response,
            "conversation_id": profile.conversation_id,
            "active": conversation.active
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)