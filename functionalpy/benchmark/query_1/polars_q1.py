import datetime as dt

import polars as pl

from functionalpy.benchmark.query_1.input_data import Q1_DATA
from functionalpy.benchmark.utils import benchmark_method


def main(data: pl.LazyFrame) -> pl.DataFrame:
    result = (
        data.filter(pl.col("ship_date") <= dt.datetime(2000, 1, 1))
        .group_by(["returned", "line_status"])
        .agg(
            [
                pl.sum("quantity").alias("sum_qty"),
                pl.sum("extended_price").alias("sum_base_price"),
                (pl.col("extended_price") * (1 - pl.col("discount")))
                .sum()
                .alias("sum_disc_price"),
                (
                    pl.col("extended_price")
                    * (1.0 - pl.col("discount"))
                    * (1.0 + pl.col("tax"))
                )
                .sum()
                .alias("sum_charge"),
                pl.mean("quantity").alias("avg_qty"),
                pl.mean("extended_price").alias("avg_price"),
                pl.mean("discount").alias("avg_disc"),
                pl.count().alias("count_order"),
            ],
        )
    )

    collected = result.collect()

    return collected


if __name__ == "__main__":
    data = Q1_DATA
    benchmark = benchmark_method(
        data_ingest=lambda: pl.DataFrame(data).lazy(),
        query=main,
        method_title="polars_q1",
    )
