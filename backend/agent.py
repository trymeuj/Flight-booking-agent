from langgraph.graph import StateGraph

class FlightState:
    query: str = None
    flight_id: str = None
    ticket_id: str = None

workflow = StateGraph(FlightState)

def search_flights(inputs):
    """Search for flights using external APIs"""
    from api_calls import search_flight_api  # Import API function
    return search_flight_api(inputs["query"])

def get_flight_details(inputs):
    """Get flight details"""
    from api_calls import get_flight_details_api
    return get_flight_details_api(inputs["flight_id"])

def cancel_flight(inputs):
    """Cancel a flight ticket"""
    from api_calls import cancel_flight_api
    return cancel_flight_api(inputs["ticket_id"])

# Define nodes
workflow.add_node("search_flights", search_flights)
workflow.add_node("get_flight_details", get_flight_details)
workflow.add_node("cancel_flight", cancel_flight)

# Set edges (flow)
workflow.set_entry_point("search_flights")
workflow.add_edge("search_flights", "get_flight_details")
workflow.add_edge("get_flight_details", "cancel_flight")

# Compile the graph
flight_agent = workflow.compile()
