from fastapi import FastAPI
from pydantic import BaseModel
from agent import flight_agent

app = FastAPI()

class UserQuery(BaseModel):
    query: str  # Natural language query

@app.post("/ask")
async def ask_flight_agent(request: UserQuery):
    print("point 1")
    """Processes user input and calls the correct API."""
    response = flight_agent.invoke({"query": request.query})
    print("point 2")
    print("response in main.py:", response)
    if not response:
        print("Agent returned None or empty response")
        return {"error": "No valid response from agent"}

    flights = response["result"]["data"]
    return flights

