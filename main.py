import uvicorn

from core.config import app



@app.get("/")
def root():
    return {
        "message": "Welcome to the Motorcycle Club Management App!",
        "description": "This API allows you to manage motorcycle club members, posts, events, and more.",
        "documentation": {
            "swagger_ui": "/docs"
        }
    }



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
