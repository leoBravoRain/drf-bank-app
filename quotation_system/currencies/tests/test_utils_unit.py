import pytest
from ..utils import convert_amount
from ..models import CurrencyRate

@pytest.mark.unit
def test_convert_amount_with_correct_input_data(mocker):
    # arrange
    
    # define basic params
    amount = 941.86
    from_currency = 'CLP'
    to_currency = 'USD'
    
    # mock currency rate
    currency_rate = 941.86
    
    # mock db call
    mock_get = mocker.patch('quotation_system.currencies.utils.CurrencyRate.objects.get')
    mock_get.return_value.rate = currency_rate
    
    # act
    result = convert_amount(amount, from_currency, to_currency)
    
    # assert
    
    # assert mock was called
    mock_get.assert_called_once()
    mock_get.assert_called_once_with(base_currency__code=from_currency, target_currency__code=to_currency)
    
    # assert currency change
    assert result == amount / currency_rate 
    
    
@pytest.mark.unit
def test_convert_amount_same_currency():
    # arrange
    
    # define basic params
    amount = 10
    from_currency = 'USD'
    to_currency = 'USD'
    
    # act
    result = convert_amount(amount, from_currency, to_currency)
    
    # assert
    assert result == amount 
    
@pytest.mark.unit
def test_convert_amount_no_currency_rate(mocker):
    # arrange
    
    # define basic params
    amount = 10
    from_currency = 'USD'
    to_currency = 'CLP'
    
     # mock db call
    mock_get = mocker.patch(
        'quotation_system.currencies.utils.CurrencyRate.objects.get',
        side_effect=CurrencyRate.DoesNotExist    
    )
    
    # act
    # with pytest.raises(CurrencyRate.DoesNotExist) as e:
    with pytest.raises(ValueError) as e:
        convert_amount(amount, from_currency, to_currency)
    
    # assert
    # asser error message
    assert str(e.value) == "Exchange rate not available"
    
    # assert mock was called with correct params
    mock_get.assert_called_once()
    mock_get.assert_called_once_with(base_currency__code=from_currency, target_currency__code=to_currency)
    
    
    
    
    