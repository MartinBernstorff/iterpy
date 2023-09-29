import datetime as dt
import statistics
from dataclasses import dataclass
from enum import Enum

from FunctionalPython.sequence import Group, Seq


class LineStatus(Enum):
    SHIPPED = 0
    PENDING = 1
    CANCELLED = 2
    BACKORDERED = 3


@dataclass(frozen=True)
class ItemResults:
    ship_date: dt.datetime
    quantity: int
    extended_price: float
    discount: float
    tax: float
    returned: bool
    line_status: LineStatus


@dataclass(frozen=True)
class CategoryResults:
    group_name: str
    sum_quantity: int
    sum_base_price: float
    sum_discount_price: float
    sum_charge: float

    avg_quantity: float
    avg_price: float
    avg_discount: float
    num_orders: int


def get_aggregate_data(input_data: Group[ItemResults]) -> CategoryResults:
    group_id = input_data.group_id
    rows = input_data.group_contents

    return CategoryResults(
        group_name=group_id,
        sum_quantity=sum(row.quantity for row in rows),
        sum_base_price=sum(row.extended_price for row in rows),
        sum_discount_price=sum(row.extended_price * (1 - row.discount) for row in rows),
        sum_charge=sum(row.extended_price * row.discount * row.tax for row in rows),
        avg_quantity=statistics.mean(row.quantity for row in rows),
        avg_price=statistics.mean(row.extended_price for row in rows),
        avg_discount=statistics.mean(row.discount for row in rows),
        num_orders=len(rows),
    )


if __name__ == "__main__":
    input_data = [
        ItemResults(
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

    sequence = Seq(input_data).group_by(lambda row: row.line_status.name)

    pass
