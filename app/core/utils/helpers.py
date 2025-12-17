from typing import Any


def to_dict(obj: Any) -> dict[str, Any]:
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in vars(obj).items() if not k.startswith("_")}
    return dict(obj)
