import requests
from uuid import UUID
from app.models.client import Client
from app.db import get_db

# --- Розкоментуй один раз для створення клієнта ---
# db = next(get_db())
# test_client = Client(
#     id=UUID("11111111-1111-1111-1111-111111111111"),
#     name="Test Client",
#     email="test@example.com",
#     company_name="Test Company"
# )
# db.add(test_client)
# db.commit()

shipments = [
    {
        "recipient_name": "Ivan Ivanov",
        "recipient_address": "Kyiv, Main St, 1",
        "client_id": "11111111-1111-1111-1111-111111111111",
        "items": [
            {
                "name": "Book",
                "brand": "Penguin",
                "weight": 0.5,
                "quantity": 2,
                "value": 10.0,
                "value_currency": "USD",
                "hs_code": "49019900",
                "notes": "Educational"
            },
            {
                "name": "Pen",
                "brand": "Bic",
                "weight": 0.05,
                "quantity": 5,
                "value": 1.0,
                "value_currency": "USD",
                "hs_code": "96081010",
                "notes": "Blue ink"
            }
        ]
    },
    {
        "recipient_name": "Petro Petrov",
        "recipient_address": "Lviv, Green St, 7",
        "client_id": "11111111-1111-1111-1111-111111111111",
        "items": [
            {
                "name": "Laptop",
                "brand": "Lenovo",
                "weight": 2.0,
                "quantity": 1,
                "value": 800.0,
                "value_currency": "USD",
                "hs_code": "8471300000",
                "notes": "Office use"
            }
        ]
    }
]

response = requests.post("http://localhost:8000/shipments/", json=shipments)
print(response.status_code)
print(response.json())
