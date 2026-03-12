import os
from azure.communication.identity import CommunicationIdentityClient

connection_string = os.getenv("ACS_CONNECTION_STRING")

client = CommunicationIdentityClient.from_connection_string(connection_string)

identity = client.create_user()

print("ACS Identity:", identity.properties["id"])