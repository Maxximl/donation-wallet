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
        username="string",
        password="string",
        email="jane.smith@example.com"
    ),
}

mock_accounts = {
    1: Account(
        id=1,
        balance=1000.50,
        owner_id=1
    ),
    2: Account(
        id=2,
        balance=5000.50,
        owner_id=1
    ),
    3: Account(
        id=3,
        balance=2500.75,
        owner_id=2
    )
}

mock_charity_organizations = {
    1: CharityOrganization(
        id=1,
        name="Приют для бездомных",
        description="Благотворительная организация, предоставляющая еду и жилье бедным котятам.",
        website="https://pomogayushchie-ruki.ru",
        email="info@pomogayushchie-ruki.ru",
        phone_number="+7 (123) 456-78-90",
        address="ул. Благотворительная, д. 123, г. Доброта",
        account_id=1,  # Предполагаем, что у аккаунта с id=1 есть эта организация
        owner_id=1  # Предполагаем, что у пользователя с id=1 есть эта организация
    ),
    2: CharityOrganization(
        id=2,
        name="Зеленая Планета",
        description="Организация, посвященная охране окружающей среды.",
        website="https://zelenaya-planeta.ru",
        email="contact@zelenaya-planeta.ru",
        phone_number="+7 (987) 654-32-10",
        address="ул. Эко, д. 456, г. Природный",
        account_id=1,  # Предполагаем, что у аккаунта с id=2 есть эта организация
        owner_id=2  # Предполагаем, что у пользователя с id=2 есть эта организация
    )
}

mock_transactions = [
    Transaction(
        id=1,
        sender_account_id=2,
        receiver_account_id=1,
        amount=100.50,
        description="Купите плюшек собачкам",
        timestamp=datetime.datetime(2023, 10, 1, 14, 30),
        transaction_type="donation"
    ),
    Transaction(
        id=2,
        sender_account_id=1,
        receiver_account_id=3,
        amount=5000.00,
        description="Купили корм",
        timestamp=datetime.datetime(2023, 11, 2, 10, 15),
        transaction_type="deposit"
    ),
    Transaction(
        id=3,
        sender_account_id=1,
        receiver_account_id=3,
        amount=1200.00,
        description="Купили продукты",
        timestamp=datetime.datetime(2023, 11, 2, 10, 15),
        transaction_type="deposit"
    ),
    Transaction(
        id=4,
        sender_account_id=1,
        receiver_account_id=3,
        amount=5000.00,
        description="Новое оборудование",
        timestamp=datetime.datetime(2023, 11, 2, 10, 15),
        transaction_type="deposit"
    ),
]
