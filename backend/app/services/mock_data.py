from app.schemas import *

mock_account1 = Account(
    id=1,
    name="Main Account",
    balance=1000.0
)

mock_account2 = Account(
    id=2,
    name="TEST Account",
    balance=5000.0
)

mock_accounts = [
    mock_account1,
    mock_account2
]

mock_charity_organizations = [
    CharityOrganization(
        id=1,
        name="Helping Hands",
        description="A non-profit organization focused on providing food and shelter to the homeless.",
        website="https://www.helpinghands.org",
        email="contact@helpinghands.org",
        phone_number="+1234567890",
        address="123 Charity Lane, Kindness City, CA 94016",
        account_id=2
    ),
    CharityOrganization(
        id=2,
        name="Green Earth",
        description="An organization dedicated to environmental conservation and awareness.",
        website="https://www.greenearth.org",
        email="info@greenearth.org",
        phone_number="+0987654321",
        address="456 Eco Street, Nature Town, NY 10001",
        account_id=2
    ),
]


from datetime import datetime

mock_transactions = [
    Transaction(
        id=1,
        sender_account_id=1,
        receiver_account_id=2,
        amount=150.75,
        description="donate donation",
        timestamp=datetime.now(),
        transaction_type="donation"
    ),
    Transaction(
        id=2,
        sender_account_id=1,
        receiver_account_id=2,
        amount=200.00,
        description="Donation to charity",
        timestamp=datetime(2023, 10, 2, 10, 15, 0),
        transaction_type="donation"
    ),
    Transaction(
        id=3,
        sender_account_id=2,
        receiver_account_id=3,
        amount=50.00,
        description="deposit",
        timestamp=datetime(2023, 10, 3, 16, 45, 0),
        transaction_type="deposit"
    )
]
