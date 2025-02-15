import google.generativeai as genai
import langgraph.graph as lg
import json
from api_calls import search_flight_api

import os

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"
# Load API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

def parse_user_query(input_data):
    """Uses Gemini to extract intent and details from user query."""
    query = input_data["query"]
    
    # Prompt Gemini to extract intent
    
    prompt = f"""
    You are an AI that extracts structured data from user queries.

    User Query: "{query}"

    Extract intent and required details as JSON, following this format:
    {{
        "intent": "search_flights",  
        "origin": "DEL",
        "destination": "BOM",
        "departure_date": "2025-02-20"
    }}

    If the intent is unclear, respond with:
    {{
        "intent": "unknown"
    }}
    ONLY return valid JSON. No extra text.
    """

    
    response = model.generate_content(prompt)
    
    try:
        extracted_data = json.loads(response.text)  # Convert string to dictionary
    except Exception:
        extracted_data = {"intent": "unknown"}
    print(extracted_data)
    return extracted_data

def search_flights(input_data):
    """Calls the flight search API if intent is search_flights."""
    if input_data["intent"] == "search_flights":
        response = search_flight_api(
            input_data["origin"],
            input_data["destination"],
            input_data["departure_date"]
        )
        # print("response:", response)
        if(response):
            print("Amadeus returned data")
        result = {"type": "search", "result": response}
        if(result):
            print("Returning from search_flights")  # Confirm returning data
        return result  
    

# Define LangGraph flow
graph = lg.Graph()
graph.add_node("parse_user_query", parse_user_query)
graph.add_node("search_flights", search_flights)


# Connect nodes
graph.add_edge("parse_user_query", "search_flights")

# Set entry point
graph.set_entry_point("parse_user_query")

graph.set_finish_point("search_flights")  # Ensure final result is returned


# Compile agent
flight_agent = graph.compile()
