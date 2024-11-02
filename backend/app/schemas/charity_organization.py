from pydantic import Field, EmailStr, BaseModel


class CharityOrganization(BaseModel):
    id: int
    name: str
    description: str
    website: str
    email: EmailStr
    phone_number: str
    address: str
    account_id: int
    owner_id: int

    class Config:
        orm_mode = True
        from_attributes = True
