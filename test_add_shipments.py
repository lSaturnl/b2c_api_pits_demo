import requests

shipments = [
    {
        "recipient_name": "Ivan Ivanov",
        "recipient_address": "Kyiv, Main St, 1",
        "client_id": "11111111-1111-1111-1111-111111111111",
        "dispatch_id": "22222222-2222-2222-2222-222222222222",
        "items": [
            {"description": "Book", "weight": 0.5, "quantity": 2},
            {"description": "Pen", "weight": 0.05, "quantity": 5}
        ]
    },
    {
        "recipient_name": "Petro Petrov",
        "recipient_address": "Lviv, Green St, 7",
        "client_id": "11111111-1111-1111-1111-111111111111",
        "dispatch_id": "22222222-2222-2222-2222-222222222222",
        "items": [
            {"description": "Laptop", "weight": 2.0, "quantity": 1}
        ]
    }
]

response = requests.post("http://localhost:8000/shipments/", json=shipments)
print(response.status_code)
print(response.json())
