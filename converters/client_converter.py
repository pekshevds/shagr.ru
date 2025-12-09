from client_app.models import Client
from client_app.schemas import (
    ClientSchemaOutgoing,
    OrganizationSchemaOutgoing,
)


def client_to_outgoing_schema(client: Client) -> ClientSchemaOutgoing:
    organization = OrganizationSchemaOutgoing()
    organization.name = client.organization.name if client.organization else ""
    organization.address = client.organization.address if client.organization else ""
    model = ClientSchemaOutgoing(name=client.name, organization=organization)
    return model
