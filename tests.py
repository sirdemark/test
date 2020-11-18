import fastapi
from starlette.testclient import TestClient

from discounts import Discount
from main import app
from states import STATES

client = TestClient(app)


def test_calculate():
    state = "TX"
    price_per_good = 20
    number_of_goods = 32

    data = {
        "state": state, "price_per_good": price_per_good, "number_of_goods": number_of_goods
    }

    full_price = price_per_good * number_of_goods
    discounted_price = full_price - Discount().get_discount(full_price)/100
    taxed_price = round(discounted_price + STATES[state] * discounted_price/100, 2)
    response = client.post(url="/calculate/", json=data)
    assert response.status_code == 200, response.json()
    assert response.json() == {
        "state": state, "price_per_good": price_per_good, "number_of_goods": number_of_goods,
        "result": taxed_price
    }, response.json()


def test_state_not_in_list():
    state = "42"
    price_per_good = 20
    number_of_goods = 32
    data = {
        "state": state, "price_per_good": price_per_good, "number_of_goods": number_of_goods
    }
    response = client.post(url="/calculate/", json=data)
    assert response.status_code == fastapi.status.HTTP_400_BAD_REQUEST, response.json()


def test_bad_price_per_good():
    state = "TX"
    price_per_good = -20
    number_of_goods = 32
    data = {
        "state": state, "price_per_good": price_per_good, "number_of_goods": number_of_goods
    }
    response = client.post(url="/calculate/", json=data)
    assert response.status_code == fastapi.status.HTTP_400_BAD_REQUEST, response.json()


def test_bad_number_of_goods():
    state = "42"
    price_per_good = 20
    number_of_goods = 0
    data = {
        "state": state, "price_per_good": price_per_good, "number_of_goods": number_of_goods
    }
    response = client.post(url="/calculate/", json=data)
    assert response.status_code == fastapi.status.HTTP_400_BAD_REQUEST, response.json()


def test_index():
    response = client.get(url="/")
    assert response.status_code == 200, response.json()
