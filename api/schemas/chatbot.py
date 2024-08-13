from sqlmodel import SQLModel



class Chatbot(SQLModel):
    query: str
