from typing import Annotated
from google.genai import types
from fastapi import APIRouter, Depends

from auth.auth import get_current_active_user
from db.config import SessionDep
from models.user import User
from ai.llm import CLIENT, CONFIG, MODEL
import json


conversation_history = []


router = APIRouter(
    prefix="/booking",
    tags=["Book Flight"]
)

@router.post("/ai")
async def book_flight(
    message: str,
    session: SessionDep,
    #current_user: Annotated[User, Depends(get_current_active_user)],

) :
    # Add user message
    conversation_history.append(
        types.Content(
            role="user",
            parts=[types.Part(text=message)]
        )
    )

    # Make the request
    response = CLIENT.models.generate_content(
        model=MODEL,
        contents=conversation_history,
        config=CONFIG,
    )

    # Add model response to history
    conversation_history.append(response.candidates[0].content)

    return {
        "model": response.text
    }
