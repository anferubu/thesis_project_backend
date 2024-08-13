from fastapi import APIRouter

from api.schemas.chatbot import Chatbot
from api.routers.utils import get_response_from_chatbot



chat = APIRouter()



@chat.post("/chat")
def chatbot(data:Chatbot):
    """Returns the response from an AI assistant."""

    query = data.query
    response = get_response_from_chatbot(query)
    return {"message": response}
