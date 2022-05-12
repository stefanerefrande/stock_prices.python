import pytest

from stock_prices import (
    get_companies_latest_prices,
    get_most_volatile_stock,
    build_csv_file,
)
import mock


class TestStock:

    @pytest.fixture
    def mock_get_most_volatile_stock(self):
        with mock.patch(
                "stock_prices.get_most_volatile_stock"
        ) as mock_get_most_volatile_stock:
            yield mock_get_most_volatile_stock

    @pytest.fixture
    def mock_api_key(self):
        return "fake_api_key"

    @pytest.fixture
    def mock_companies(self):
        return ["EXCOF", "AAPL", "GOGL"]

    def test_should_get_companies_latest_prices(
            self,
            mock_api_key,
            mock_companies,
    ):
        prices = get_companies_latest_prices(
            api_key=mock_api_key,
            companies=mock_companies
        )
        assert isinstance(prices, list)
        assert len(prices) == len(mock_companies)

    def test_should_get_most_volatile_stock(
            self,
            mock_api_key,
            mock_companies,
    ):
        most_volatile_stock_info = get_most_volatile_stock(
            api_key=mock_api_key,
            companies=mock_companies
        )
        assert isinstance(most_volatile_stock_info, list)
        assert len(most_volatile_stock_info) == 4
        assert isinstance(most_volatile_stock_info[0], str)
        assert isinstance(most_volatile_stock_info[1], float)

    def test_should_build_csv_file(
            self,
            mock_api_key,
            mock_companies,
            mock_get_most_volatile_stock
    ):
        build_csv_file(
            api_key=mock_api_key,
            companies=mock_companies
        )
        mock_get_most_volatile_stock.assert_called()
