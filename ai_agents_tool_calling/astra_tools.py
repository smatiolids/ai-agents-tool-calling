import os
from typing import Optional
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool, StructuredTool
from .astra_conn import AstraDBConnection

astra_db = AstraDBConnection().get_session()
flight_tickets_collection = astra_db.get_collection(
    os.getenv("ASTRA_COLLECTION"))

# TOOL Definition =  Scheduled Flights


class ScheduledFlightsInput(BaseModel):
    customer_id: str = Field(
        description="The UUID that represents the customer")
    arrivalAirport: Optional[str] = Field(
        description="Arrival Airport code")
    departureAirport: Optional[str] = Field(
        description="Departure Airport code")



def _get_scheduled_flights(customer_id: str, arrivalAirport: str = None, departureAirport: str = None) -> [str]:
    filter = {"customerId": customer_id}

    if arrivalAirport != None:
        filter["arrivalAirport"] = arrivalAirport

    if departureAirport != None:
        filter["departureAirport"] = departureAirport

    print(f"Scheduled flights condition: {filter}")

    flights = flight_tickets_collection.find(filter=filter, projection={
        "departureAirport": 1, "arrivalAirport": 1, "departureDateTime": 1})

    res = []
    for doc in flights:
        res.append(doc)
        
    return res

get_scheduled_flights = StructuredTool.from_function(
    func=_get_scheduled_flights,
    name="GetScheduledFlights",
    description="Returns information about scheduled flights for a customer",
    args_schema=ScheduledFlightsInput,
)

class ScheduledFlightDetailInput(BaseModel):
    ticket_id: str = Field(
        description="The UUID for a specific flight ticket")

def _get_flight_detail(ticket_id: str) -> [str]:
    print(f"Flight detail: {ticket_id}")
    filter = {"_id": ticket_id}
    flight = flight_tickets_collection.find_one(filter=filter)
    return flight

get_flight_detail = StructuredTool.from_function(
    func=_get_flight_detail,
    name="GetFlightDetail",
    description="Returns information about a flight",
    args_schema=ScheduledFlightDetailInput,
)

