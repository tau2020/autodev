from typing import Any

def debug_print(debug: bool, *args: Any) -> None:
    if debug:
        print(*args)
