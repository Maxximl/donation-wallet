import datetime

from app.db.models import *

mock_users = {
    1: User(
        id=1,
        username="john_doe",
        password="hashed_password_123",
        email="john.doe@example.com"
    ),
    2: User(
        id=2,
        username="jane_smith",
        password="hashed_password_456",
        email="jane.smith@example.com"
    ),
    3: User(
        id=2,
        username="string",
        password="string",
        email="string@example.com"
    )
}

mock_accounts = {
    1: Account(
        id=1,
        balance=1000.50,
        owner_id=1
    ),
    2: Account(
        id=2,
        balance=1000.50,
        owner_id=1
    ),
    3: Account(
        id=3,
        balance=250.75,
        owner_id=2
    )
}

mock_charity_organizations = {
    1: CharityOrganization(
        id=1,
        name="Helping Hands",
        description="A charity organization focused on providing food and shelter.",
        website="https://helpinghands.org",
        email="info@helpinghands.org",
        phone_number="123-456-7890",
        address="123 Charity St, Kindness City",
        account_id=1,  # Предполагаем, что у аккаунта с id=1 есть эта организация
        owner_id=1  # Предполагаем, что у пользователя с id=1 есть эта организация
    ),
    2: CharityOrganization(
        id=2,
        name="Green Earth",
        description="An organization dedicated to environmental conservation.",
        website="https://greenearth.org",
        email="contact@greenearth.org",
        phone_number="987-654-3210",
        address="456 Eco Rd, Nature Town",
        account_id=3,  # Предполагаем, что у аккаунта с id=2 есть эта организация
        owner_id=2  # Предполагаем, что у пользователя с id=2 есть эта организация
    )
}

mock_transactions = {
    1: Transaction(
        id=1,
        sender_account_id=2,
        receiver_account_id=1,
        amount=100.50,
        description="Donation to Green Earth",
        timestamp=datetime.datetime(2023, 10, 1, 14, 30),
        transaction_type="donation"
    ),
    2: Transaction(
        id=2,
        sender_account_id=2,
        receiver_account_id=3,
        amount=50.00,
        description="Типа потратили",
        timestamp=datetime.datetime(2023, 11, 2, 10, 15),
        transaction_type="deposit"
    )
}
