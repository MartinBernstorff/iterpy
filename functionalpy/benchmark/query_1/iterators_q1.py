import datetime as dt
import statistics as stats
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from functionalpy import Seq
from functionalpy.benchmark.query_1.input_data import Q1_DATA
from functionalpy.benchmark.utils import benchmark_method


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
    cancelled: bool
    line_status: LineStatus


@dataclass(frozen=True)
class CategorySummary:
    category_name: str

    sum_quantity: int
    sum_base_price: float
    sum_discount_price: float
    sum_charge: float

    avg_quantity: float
    avg_price: float
    avg_discount: float
    num_orders: int


def summarise_category(
    groupname: str,
    rows: Sequence[Item],
) -> CategorySummary:
    return CategorySummary(
        category_name=groupname,
        sum_quantity=sum(r.quantity for r in rows),
        sum_base_price=sum(r.extended_price for r in rows),
        sum_discount_price=sum(
            calculate_discounted_price(r) for r in rows
        ),
        sum_charge=sum(calculate_charge(r) for r in rows),
        avg_quantity=stats.mean(r.quantity for r in rows),
        avg_price=stats.mean(r.extended_price for r in rows),
        avg_discount=stats.mean(r.discount for r in rows),
        num_orders=len(rows),
    )


def calculate_discounted_price(item: Item) -> float:
    return item.extended_price * (1 - item.discount)


def calculate_charge(item: Item) -> float:
    return item.extended_price * (1 - item.discount) * (1 - item.tax)


def parse_input_data(
    input_data: Sequence[Mapping[str, Any]]
) -> Sequence[Item]:
    parsed_data = (
        Seq(input_data)
        .map(
            lambda row: Item(
                ship_date=row["ship_date"],
                quantity=row["quantity"],
                extended_price=row["extended_price"],
                discount=row["discount"],
                tax=row["tax"],
                returned=row["returned"],
                line_status=LineStatus[row["line_status"].upper()],
                cancelled=row["cancelled"],
            ),
        )
        .to_list()
    )

    return parsed_data


def main_iterator(data: Sequence[Item]) -> Sequence[CategorySummary]:
    mapping = (
        Seq(data)
        .filter(lambda i: i.ship_date <= dt.datetime(2000, 1, 1))
        .groupby(
            lambda i: f"status_{i.cancelled}_returned_{i.returned}"
        )
    )

    summaries = [
        summarise_category(group, rows=values)
        for group, values in mapping.items()
    ]

    return summaries


if __name__ == "__main__":
    benchmark = benchmark_method(
        data_ingest=lambda: parse_input_data(input_data=Q1_DATA),
        query=main_iterator,
        method_title="iterators_q1",
    )
