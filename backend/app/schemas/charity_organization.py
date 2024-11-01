from pydantic import Field, EmailStr, BaseModel


class CharityOrganization(BaseModel):
    id: int
    name: str
    description: str
    website: str
    email: EmailStr = Field(..., unique=True)
    phone_number: str
    address: str
    account_id: int
