from collections.abc import Sequence
from typing import reveal_type, overload


@overload
def double(input_: int) -> int: ...


@overload
def double(input_: Sequence[int]) -> list[int]: ...


def double(input_: int | Sequence[int]) -> int | list[int]:
    if isinstance(input_, Sequence):
        return [i * 2 for i in input_]
    return input_ * 2




if __name__ == "__main__":
    x = double(12)
    z = x / 12 # Will be error raise by type checker without overloading signatures
    print(isinstance(x, int))
    print(reveal_type(x))
