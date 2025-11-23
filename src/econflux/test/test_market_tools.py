import pytest

from econflux.tools import get_stock_price


@pytest.mark.integration
def test_get_stock_price_basic():
    data = get_stock_price("AAPL")
    assert data["ticker"] == "AAPL"
    assert data["price"] is not None
