import datetime as dt
import itertools
import statistics as stats
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from FunctionalPython.benchmark.query_1.input_data import Q1_DATA
from FunctionalPython.benchmark.utils import benchmark_method
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


def summarise_category(input_data: Group[Item]) -> CategorySummary:
    group_id = input_data.group_id
    rows = input_data.group_contents.to_list()

    return CategorySummary(
        category_name=group_id,
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


def calculate_charge(item: Item) -> float:
    return item.extended_price * (1 - item.discount) * (1 - item.tax)


def parse_input_data(input_data: Sequence[Mapping[str, Any]]) -> Sequence[Item]:
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
            ),
        )
        .to_list()
    )

    return parsed_data


def main_native(data: Sequence[Item]) -> Sequence[CategorySummary]:
    filtered = filter(lambda x: x.ship_date <= dt.datetime(2000, 1, 1), data)
    grouped = (
        Group(group_id=key, group_contents=value)
        for key, value in itertools.groupby(
            filtered,
            key=lambda row: f"status_{row.cancelled}_returned_{row.returned}",
        )
    )
    summarised = map(summarise_category, grouped)

    return list(summarised)


def main_inlined(data: Sequence[Item]) -> Sequence[CategorySummary]:
    return list(
        map(
            summarise_category,
            (
                Group(group_id=key, group_contents=value)
                for key, value in itertools.groupby(
                    filter(lambda x: x.ship_date <= dt.datetime(2000, 1, 1), data),
                    key=lambda row: f"status_{row.cancelled}_returned_{row.returned}",
                )
            ),
        )
    )


def main_iterator(data: Sequence[Item]) -> Sequence[CategorySummary]:
    sequence = (
        Seq(data)
        .filter(lambda i: i.ship_date <= dt.datetime(2000, 1, 1))
        .group_by(lambda i: f"status_{i.cancelled}_returned_{i.returned}")
        .map(summarise_category)
        .to_list()
    )

    return sequence


if __name__ == "__main__":
    benchmark = benchmark_method(
        data_ingest=lambda: parse_input_data(input_data=Q1_DATA),
        query=main_iterator,
        method_title="iterators_q1",
    )
