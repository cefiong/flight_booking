from models.chat import ConversationHistory
from models.chat import BookingState

conversation_store = {}
state_store = {}


def get_history(user_id: str):

    if user_id not in conversation_store:
        conversation_store[user_id] = ConversationHistory()

    return conversation_store[user_id]


def get_state(user_id: str):

    if user_id not in state_store:
        state_store[user_id] = BookingState()

    return state_store[user_id]