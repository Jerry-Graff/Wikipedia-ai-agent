import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Wikipedia Research Agent",
    description="An ai agent which searches Wikepdia and returns text summaries",
    version="1.0.0"
)


# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Wikipedia Research Agent is running!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
