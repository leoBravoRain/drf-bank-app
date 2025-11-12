import pytest
import requests
from django.contrib.auth.models import User


@pytest.mark.django_db
@pytest.mark.e2e
def test_auth_flow(live_server):

    # user info
    username = "test"
    password = "test123"

    # account info
    account_currency = "USD"

    # trx info
    trx_amount = 1

    # urls
    signup_url = f"{live_server.url}/api/users/signup/"
    token_url = f"{live_server.url}/api/users/login/"
    trx_url = f"{live_server.url}/api/transactions/"
    account_url = f"{live_server.url}/api/accounts/"

    # 0. create user (signup)
    signup_response = requests.post(
        signup_url, json={"username": username, "password": password}
    )

    assert signup_response.status_code == 201

    user = signup_response.json()
    assert user["username"] == username

    # 1. Get token via real HTTP call
    token_response = requests.post(
        token_url, json={"username": username, "password": password}
    )

    assert token_response.status_code == 200
    token = token_response.json()["access"]

    # define auth header
    headers = {"Authorization": f"Bearer {token}"}

    # 2. create an account
    account_response = requests.post(
        account_url,
        json={"currency": account_currency},
        headers=headers,
    )

    assert account_response.status_code == 201

    # get account
    account = account_response.json()

    assert account["balance"] == "0.00"

    # 3. See account created
    accounts_response = requests.get(account_url, headers=headers)

    accounts = accounts_response.json()
    assert len(accounts) == 1
    assert accounts[0]["id"] == account["id"]

    # 3. make a deposit with different currency of the account
    trx_response = requests.post(
        trx_url,
        json={
            "transaction_type": "deposit",
            "amount": trx_amount,
            "account": account["id"],
            "currency": account_currency,
        },
        headers=headers,
    )

    trx = trx_response.json()

    assert trx_response.status_code == 201
    assert trx["previous_balance"] == "0.00"
    assert trx["new_balance"] == f"{trx_amount}.00"

    # 4. get account to check if balance was updated
    accounts_response = requests.get(account_url, headers=headers)
    account = accounts_response.json()[0]

    # assert balance was updated
    assert account["balance"] == f"{trx_amount}.00"
