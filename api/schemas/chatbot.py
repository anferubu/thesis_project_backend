from sqlmodel import SQLModel



class ChatPrompt(SQLModel):
    prompt: str
