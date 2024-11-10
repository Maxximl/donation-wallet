import app.services.mock_orm_models as mock_orm_models
from app.schemas import *


# mock_accounts, mock_transactions, mock_charity_organizations, mock_users

def model_list_to_schemas_list(schema, models_list: dict) -> dict:
    """Костыль для преобразования списка из моковых моделей БД в список схем ответов."""
    schemas = {}
    for key in models_list:
        schemas[key] = schema.from_orm(models_list[key])
    return schemas


mock_accounts = model_list_to_schemas_list(Account, mock_orm_models.mock_accounts)
mock_transactions = list(map(Transaction.from_orm, mock_orm_models.mock_transactions))
mock_charity_organizations = model_list_to_schemas_list(CharityOrganization, mock_orm_models.mock_charity_organizations)
mock_users = model_list_to_schemas_list(User, mock_orm_models.mock_users)
