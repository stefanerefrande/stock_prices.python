import requests
import json
from typing import List
from requests import Response
from pandas import DataFrame

COMPANIES = ["AAPL", "AMZN", "NFLX", "FB", "GOGL"]
API_KEY = "fake_api_key"


def _get_stock_price_api(api_key: str, company: str) -> Response:
    return requests.get(f"https://finnhub.io/api/v1/quote?symbol={company}&token={api_key}")


def get_companies_latest_prices(api_key: str, companies: list[str]) -> List:
    latest_prices = []
    for c, company in enumerate(companies):
        response = _get_stock_price_api(api_key=api_key, company=COMPANIES[c])
        stock_info = json.loads(response.content)
        stock_prices = stock_info["c"]
        latest_prices.append(stock_prices)
    return latest_prices


def get_most_volatile_stock(api_key: str, companies: list[str]) -> List:
    percent_change, current_price, last_close_price = 0, 0, 0
    stock_symbol = ""
    for c, company in enumerate(companies):
        response = _get_stock_price_api(api_key=api_key, company=COMPANIES[c])
        stock_info = json.loads(response.content)
        percentage = abs(stock_info["dp"])
        if percentage > percent_change:
            percent_change = percentage
            stock_symbol = company
            current_price = stock_info["c"]
            last_close_price = stock_info["pc"]
    return [stock_symbol, percent_change, current_price, last_close_price]


def build_csv_file(api_key: API_KEY, companies: COMPANIES):
    stock_symbol = get_most_volatile_stock(api_key, companies)[0]
    percent_change = get_most_volatile_stock(api_key, companies)[1]
    current_price = get_most_volatile_stock(api_key, companies)[2]
    last_close_price = get_most_volatile_stock(api_key, companies)[3]
    stock_data = DataFrame(
        [[stock_symbol, percent_change, current_price, last_close_price]],
        columns=['stock_symbol', 'percentage_change', 'current_price', 'last_close_price']
    )
    return stock_data.to_csv('most_volatile_stock.csv')
