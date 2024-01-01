from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TypeMarker:
    replacement_str: str


if __name__ == "__main__":
    base_message_template = """
    # TYPE[S]   # noqa: ERA001
    @overload
    def flatten(self: Seq[TYPE[S]]) -> Seq[S]: ...
    @overload
    def flatten(self: Seq[TYPE[S] | S]) -> Seq[S]: ...
    """

    heterogenous_overload = """@overload
    def flatten(self: Seq[TYPE[S] | T]) -> Seq[S]: ..."""

    combined_interface = f"    # Code for generating the following is in {Path(__file__).name}"
    for mark in [
        TypeMarker("Iterable[S]"),
        TypeMarker("Iterator[S]"),
        TypeMarker("tuple[S, ...]"),
        TypeMarker("Sequence[S]"),
        TypeMarker("list[S]"),
        TypeMarker("Mapping[S, U]"),
        TypeMarker("set[S]"),
        TypeMarker("frozenset[S]"),
    ]:
        message = (
            base_message_template.replace(
                "TYPE[S]", mark.replacement_str
            )
            + "\n"
        )
        combined_interface += message

    combined_interface += """
    # str
    @overload
    def flatten(self: Seq[str]) -> Seq[str]: ...
    @overload
    def flatten(self: Seq[str | S]) -> Seq[S]: ...
    """

    combined_interface += """
    # Generic
    @overload
    def flatten(self: Seq[S]) -> Seq[S]: ...
    """

    print(combined_interface)
