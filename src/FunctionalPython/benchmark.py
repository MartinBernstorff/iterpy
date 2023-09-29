import datetime as dt
import statistics as stats
from dataclasses import dataclass
from enum import Enum

from FunctionalPython.sequence import Group, Seq


class LineStatus(Enum):
    SHIPPED = 0
    PENDING = 1
    CANCELLED = 2
    BACKORDERED = 3


@dataclass(frozen=True)
class Item:
    ship_date: dt.datetime
    quantity: int
    extended_price: float
    discount: float
    tax: float
    returned: bool
    line_status: LineStatus


@dataclass(frozen=True)
class CategorySummary:
    group_name: str
    sum_quantity: int
    sum_base_price: float
    sum_discount_price: float
    sum_charge: float

    avg_quantity: float
    avg_price: float
    avg_discount: float
    num_orders: int


def summarise_category(input_data: Group[Item]) -> CategorySummary:
    group_id = input_data.group_id
    rows = input_data.group_contents.to_list()

    return CategorySummary(
        group_name=group_id,
        sum_quantity=sum(r.quantity for r in rows),
        sum_base_price=sum(r.extended_price for r in rows),
        sum_discount_price=sum(calculate_discounted_price(r) for r in rows),
        sum_charge=sum(calculate_charge(r) for r in rows),
        avg_quantity=stats.mean(r.quantity for r in rows),
        avg_price=stats.mean(r.extended_price for r in rows),
        avg_discount=stats.mean(r.discount for r in rows),
        num_orders=input_data.group_contents.count(),
    )


def calculate_discounted_price(item: Item) -> float:
    return item.extended_price * (1 - item.discount)


def calculate_charge(r: Item) -> float:
    return r.extended_price * r.discount * r.tax


if __name__ == "__main__":
    input_data = [
        Item(
            ship_date=dt.datetime(1995 + i, 9, 2),
            quantity=i,
            extended_price=0.1 * i,
            discount=1 - (0.1 * i),
            tax=(1 - (0.1 * i)),
            line_status=LineStatus.SHIPPED if i < 5 else LineStatus.PENDING,
            returned=not i < 9,
        )
        for i in range(10)
    ]

    sequence = (
        Seq(input_data)
        .group_by(lambda row: f"status_{row.line_status.name}_returned_{row.returned}")
        .map(summarise_category)
        .to_list()
    )

    pass
