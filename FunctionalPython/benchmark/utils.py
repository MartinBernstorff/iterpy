import timeit
from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from linetimer import CodeTimer

T0 = TypeVar("T0")
T1 = TypeVar("T1")


@dataclass(frozen=True)
class BenchmarkResult(Generic[T0]):
    output: T0
    time_seconds: float


def run_query(query: Callable[..., T0], query_title: str) -> BenchmarkResult[T0]:
    with CodeTimer(name=f"{query_title}", unit="s"):
        t0 = timeit.default_timer()
        result = query()

        secs = timeit.default_timer() - t0

    return BenchmarkResult(output=result, time_seconds=secs)


@dataclass(frozen=True)
class CombinedBenchmark(Generic[T0, T1]):
    ingest: BenchmarkResult[T0]
    query_result: BenchmarkResult[T1]


def benchmark_method(
    data_ingest: Callable[..., T0],
    query: Callable[[T0], T1],
    method_title: str,
) -> CombinedBenchmark[T0, T1]:
    data_ingest_result = run_query(
        lambda: data_ingest(),
        query_title=f"{method_title}: Data ingest for {method_title}",
    )
    parsed_data = data_ingest_result.output

    result = run_query(
        lambda: query(data=parsed_data),  # type: ignore
        query_title=f"{method_title}: Computation",
    )

    return CombinedBenchmark(ingest=data_ingest_result, query_result=result)
