from sqlmodel import SQLModel
from pydantic import BaseModel
from typing import Optional, List

from pydantic import BaseModel, Field
from typing import Literal, Optional, List


class Chat(SQLModel):
    message: str = "Book me a flight for tomorrow morning from London to Berlin"


class FlightEntities(BaseModel):

    origin_city: Optional[str] = None
    origin_airport: Optional[str] = None

    destination_city: Optional[str] = None
    destination_airport: Optional[str] = None

    departure_date: Optional[str] = None

    time_of_day: Optional[
        Literal["morning", "afternoon", "evening", "night"]
    ] = None


class LLMResponse(BaseModel):

    intent: Literal[
        "search_flights",
        "select_flight",
        "confirm_booking",
        "cancel_booking",
        "general_question"
    ]

    entities: FlightEntities
    missing_fields: List[str] = Field(default_factory=list)
    assistant_message: str


class Conversation(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ConversationHistory(BaseModel):
    history : list[Conversation]= Field(default_factory=list)


class BookingState(BaseModel):

    origin_city: Optional[str] = None
    origin_airport: Optional[str] = None

    destination_city: Optional[str] = None
    destination_airport: Optional[str] = None

    departure_date: Optional[str] = None

    offers: Optional[list] = None

    selected_offer_id: Optional[str] = None

    awaiting_confirmation: bool = False