from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TypeMarker:
    replacement_str: str


if __name__ == "__main__":
    base_message_template = """
    # TYPE[S]   # noqa: ERA001
    @overload
    def flatten(self: Iter[TYPE[S]]) -> Iter[S]: ...
    @overload
    def flatten(self: Iter[TYPE[S] , S]) -> Iter[S]: ...
    """

    heterogenous_overload = """@overload
    def flatten(self: Iter[TYPE[S] , T]) -> Iter[S]: ..."""

    combined_interface = f"    # Code for generating the following is in {Path(__file__).name}"
    for mark in [
        TypeMarker("iterpyator[S]"),
        TypeMarker("tuple[S, ...]"),
        TypeMarker("Sequence[S]"),
        TypeMarker("list[S]"),
        TypeMarker("set[S]"),
        TypeMarker("frozenset[S]"),
        TypeMarker("Iter[S]"),
    ]:
        message = base_message_template.replace("TYPE[S]", mark.replacement_str) + "\n"
        combined_interface += message

    combined_interface += """
    # str
    @overload
    def flatten(self: Iter[str]) -> Iter[str]: ...
    @overload
    def flatten(self: Iter[str , S]) -> Iter[S]: ...
    """

    combined_interface += """
    # Generic
    @overload
    def flatten(self: Iter[S]) -> Iter[S]: ...
    """

    print(combined_interface)
