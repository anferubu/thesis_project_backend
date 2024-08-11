import uvicorn

from core.config import app



@app.get("/")
async def root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
