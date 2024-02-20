from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import pytest

from iterpy.iter import Iter

if TYPE_CHECKING:
    import types
    from collections.abc import Callable, Mapping, Sequence


@dataclass(frozen=True)
class AnnotatedArgument:
    name: str
    annotation: types.GenericAlias | type | None


def _get_callable_annotated_args(method: Callable[[Any], Any]) -> Sequence[AnnotatedArgument]:
    annotated_args = getattr(method, "__annotations__", None)
    annotated_arguments = [
        AnnotatedArgument(name=arg_name, annotation=annotation)
        for (arg_name, annotation) in annotated_args.items()  # type: ignore
        if arg_name not in ("self", "return", "cls")
    ]

    return annotated_arguments


def _populate_values_for_arg(arg: AnnotatedArgument) -> Any:
    annotation: str = str(arg.annotation)  # type: ignore

    if annotation == "int":
        return 0
    if annotation == "str":
        return ""

    if "Callable[[T], bool]" in annotation:
        return lambda x: True  # type: ignore # noqa: ARG005
    if "Callable[[T], S]" in annotation:
        return lambda x: x  # type: ignore
    if "Callable[[T, T], T]" in annotation:
        return lambda x, y: x  # type: ignore # noqa: ARG005
    if "Callable[[T], str]" in annotation:
        return lambda x: str(x)  # type: ignore
    if "Iter[S]" in annotation:
        return Iter([1, 2, 3])

    raise ValueError(f"Unsupported type: {annotation}")


def _annotated_args_to_mapping(annotated_args: Sequence[AnnotatedArgument]) -> Mapping[str, Any]:
    return {arg.name: _populate_values_for_arg(arg) for arg in annotated_args}


@dataclass(frozen=True)
class IterBenchmarkExample:
    iter_items: Sequence[int]
    method: Callable[[Any], Any]
    method_args: Mapping[str, Any] | None

    def call_method(self) -> Any:
        iterator = Iter(self.iter_items)
        if self.method_args:
            return self.method(iterator, **self.method_args)
        return self.method(iterator)


def _is_public(method_name: str) -> bool:
    return not method_name.startswith("_")


def _name_to_callable(name: str) -> Callable[[Any], Any]:
    return getattr(Iter, name)


def _excluded(method: Callable[[Any], Any], excluded_fns: Sequence[str]) -> bool:
    return any(substring in str(method) for substring in excluded_fns)


def _extract_public_methods_with_default_args(
    iter_benchmark_items: Sequence[Any], excluded_methods: Sequence[str]
) -> Sequence[IterBenchmarkExample]:
    # Get all public methods from Iter class
    method_names = dir(Iter)

    public_methods = (
        Iter(method_names)
        .filter(_is_public)
        .map(_name_to_callable)
        .filter(lambda method: not _excluded(method, excluded_methods))
    )

    arguments = public_methods.map(_get_callable_annotated_args).map(_annotated_args_to_mapping)

    combined = Iter(zip(public_methods, arguments)).map(  # type: ignore
        lambda x: IterBenchmarkExample(
            iter_items=iter_benchmark_items, method=x[0], method_args=x[1]
        )
    )

    return combined.to_list()


iter_example_generator = functools.partial(
    _extract_public_methods_with_default_args,
    iter_benchmark_items=list(range(1_000)),
    excluded_methods=[
        "pmap"  # pmap requires pickling a lambda, which is not supported
    ],
)

if __name__ == "__main__":
    examples = iter_example_generator()


@pytest.mark.parametrize(
    ("example"), iter_example_generator(), ids=lambda example: example.method.__name__
)
@pytest.mark.benchmark()
def test_benchmark_iter(example: IterBenchmarkExample) -> None:
    example.call_method()
