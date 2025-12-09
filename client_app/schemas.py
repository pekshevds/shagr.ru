from pydantic import BaseModel, Field


class SendEmailSchemaOutgoing(BaseModel):
    client_name: str = Field()
    email: str = Field()
    pin: str = Field()


class OrganizationSchemaOutgoing(BaseModel):
    name: str = Field(default="")
    address: str = Field(default="")


class ClientSchemaIncoming(BaseModel):
    email: str = Field()


class ClientSchemaOutgoing(BaseModel):
    name: str = Field()
    organization: OrganizationSchemaOutgoing | None = Field(default=None)


class PinSchema(BaseModel):
    pin: str = Field()


class ClientCredentialSchema(BaseModel):
    email: str = Field()
    pin: str = Field()


class TokenSchema(BaseModel):
    token: str = Field()
