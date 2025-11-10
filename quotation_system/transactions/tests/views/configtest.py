from unittest.mock import MagicMock

import pytest
from rest_framework.test import APIRequestFactory

from quotation_system.transactions.views import (
    TransactionDetailView,
    TransactionListView,
)


@pytest.fixture
def api_factory():
    """Provides a DRF APIRequestFactory instance."""
    return APIRequestFactory()


@pytest.fixture
def user():
    """Provides a fake user object."""
    user = MagicMock()
    user.id = 1
    return user


@pytest.fixture
def view():
    """Provides a AccountListView instance."""
    return TransactionListView()


@pytest.fixture
def detail_view():
    """Provides a TransactionDetailView instance."""
    return TransactionDetailView()


@pytest.fixture
def mock_atomic(mocker):
    atomic_cm = mocker.MagicMock()
    atomic_cm.__enter__.return_value = None
    atomic_cm.__exit__.return_value = None
    return mocker.patch(
        "quotation_system.transactions.views.transaction.atomic", return_value=atomic_cm
    )
