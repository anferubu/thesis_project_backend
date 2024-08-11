from fastapi import APIRouter

from api.schemas.chatbot import ChatPrompt



chat = APIRouter()


@chat.post("/chat")
def chatbot(data:ChatPrompt):
    """Returns the response from an AI assistant."""

    prompt = data.prompt
    # logic here
    response = f"Received your prompt: {prompt}. This is a simulated response."
    return {"message": response}
