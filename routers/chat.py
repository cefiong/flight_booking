from typing import Annotated

from fastapi import APIRouter, Depends

from auth.auth import get_current_active_user
from db.config import SessionDep
from models.chat import Chat, LLMResponse
from models.user import User
from ai.llm import client, CONFIG, MODEL
import json


conversation_history = []


router = APIRouter(
    prefix="/booking",
    tags=["Book Flight"]
)

@router.post("/ai")
async def book_flight(
    session: SessionDep,
    #current_user: Annotated[User, Depends(get_current_active_user)],
    chat: Chat
) :

    conversation_history.append({
        "role": "user",
        "content": chat.message
    })


    # Send request with function declarations
    response = client.interactions.create(
        model=MODEL,
        contents=chat.message,
        config=CONFIG,
        input=conversation_history
    )

    llm_data = LLMResponse.model_validate_json(response.text)

    conversation_history.append({
        "role": "assistant",
        "content": llm_data.assistant_message
    })



    return response.text


