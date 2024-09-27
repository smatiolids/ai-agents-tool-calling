import json
import os
#from .astra_conn import AstraDBConnection
from astrapy import DataAPIClient
from astrapy.constants import Environment
from astrapy.authentication import UsernamePasswordTokenProvider


# Build a token
tp = UsernamePasswordTokenProvider("hcd-superuser","PMdS9fnkeH0PumEeANhm")

# Initialize the client and get a "Database" object

file_path = "./sample_data.json"

def load_flight_tickets(clear):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        data = json.load(file)

    if data['flights']:
        client = DataAPIClient(token=tp, environment=Environment.HCD)
        database = client.get_database("http://localhost:8181", token=tp, namespace="default_namespace")
        #astra_db = AstraDBConnection().get_session()
        print("Creating or Getting the collection")
        flight_tickets_collection = database.create_collection("flight_tickets" )
        
        print("Inserting Data")
        # flight_tickets_collection = astra_db.get_collection(os.getenv("ASTRA_COLLECTION"))
        res = flight_tickets_collection.insert_many([{**d, "customerId": 'f08a6894-1863-491d-8116-3945fb915597'} for d in data['flights']])
        return res

    
    return False


if __name__ == "__main__":
    load_flight_tickets(False)
