import pytest
from ..configtest import api_factory, user, view

@pytest.mark.unit
def test_get_queryset_returns_transactions_filtered_by_user(api_factory, user, view, mocker):
    
    # arrange
    
    # mock filter() method
    mock_filter = mocker.patch('quotation_system.transactions.views.Transaction.objects.filter')
    
    # create request object
    request = api_factory.get("/")
    request.user = user
    view.request = request
    
    # act
    view.get_queryset()
    
    # assert
    mock_filter.assert_called_once()
    mock_filter.assert_called_once_with(user=user)