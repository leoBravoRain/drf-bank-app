import pytest
import requests
from django.contrib.auth.models import User


@pytest.mark.django_db
@pytest.mark.e2e
def test_auth_flow(live_server):
    username = "test"
    password = "test123"

    # create test user
    user = User.objects.create_user(username=username, password=password)

    token_url = f"{live_server.url}/api/users/login/"
    # tx_url = f"{live_server.url}/api/transactions/"

    # 1️⃣ Get token via real HTTP call
    token_response = requests.post(
        token_url, json={"username": username, "password": password}
    )

    print(token_response.json())

    assert token_response.status_code == 200
    # token = token_response.json()["access"]

    # # 2️⃣ Use token to perform a real request
    # headers = {"Authorization": f"Bearer {token}"}
    # tx_response = requests.post(
    #     tx_url,
    #     json={"transaction_type": "deposit", "amount": 100, "currency": "USD", "account": 1},
    #     headers=headers,
    # )
    # assert tx_response.status_code == 201
