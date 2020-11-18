from pydantic import validator, ValidationError, typing
from pydantic.main import BaseModel

from discounts import Discount
from states import STATES


class Calculator(BaseModel):
    price_per_good: typing.Union[float, int]
    number_of_goods: int
    state: str

    @validator('state', always=True)
    def check_state(cls, state, values):
        if not (state is not None and state in STATES.keys()):
            raise ValueError(f"Код штата {state} не известен.")

        return state

    @validator('price_per_good', always=True)
    def check_price_per_good(cls, price_per_good, values):
        if price_per_good <= 0:
            raise ValueError(f"Цена за товар меньше или равна нулю.")

        return price_per_good

    @validator('number_of_goods', always=True)
    def check_number_of_goods(cls, number_of_goods, values):
        if number_of_goods <= 0:
            raise ValueError(f"Количество продуктов меньше или равно нулю.")

        return number_of_goods

    def _count_tax(self, price: float) -> float:
        return price + STATES[self.state] * price/100

    def _count_discount(self, price: float) -> float:
        return price - Discount().get_discount(price) * price/100

    def execute(self):
        full_price = self.price_per_good * self.number_of_goods
        discounted_price = self._count_discount(full_price)
        return round(self._count_tax(discounted_price), 2)


class CalculatorResponse(BaseModel):
    price_per_good: typing.Union[float, int]
    number_of_goods: int
    state: str
    result: float
