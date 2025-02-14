from fastapi import FastAPI
from agent import flight_agent
from pydantic import BaseModel

app = FastAPI()

class FlightQuery(BaseModel):
    query: str

@app.post("/ask")
async def ask_flight_agent(request: FlightQuery):
    """Handles user queries and invokes the AI agent."""
    response = flight_agent.invoke({"query": request.query})
    return response
