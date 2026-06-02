import json

from app.config import get_settings


def truncate_output(data: dict) -> dict:
    settings = get_settings()
    encoded = json.dumps(data, default=str).encode("utf-8")
    if len(encoded) <= settings.execution_output_max_bytes:
        return data
    # Keep only safe summary keys when too large
    return {
        "truncated": True,
        "message": "Output exceeded size limit; see LangSmith trace for full data.",
        "keys": list(data.keys())[:20],
    }
