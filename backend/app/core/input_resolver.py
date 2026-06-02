import re
from typing import Any

_STATE_PATTERN = re.compile(r"\{\{\s*state\.(\w+)\s*\}\}")
_INPUTS_PATTERN = re.compile(r"\{\{\s*inputs\.(\w+)\s*\}\}")


def resolve_value(template: Any, state: dict, inputs: dict) -> Any:
    if isinstance(template, str):
        result = template

        def state_repl(match: re.Match) -> str:
            key = match.group(1)
            val = state.get(key, inputs.get(key, ""))
            if isinstance(val, list):
                return str(val)
            return str(val) if val is not None else ""

        def inputs_repl(match: re.Match) -> str:
            key = match.group(1)
            val = inputs.get(key, state.get(key, ""))
            if isinstance(val, list):
                return str(val)
            return str(val) if val is not None else ""

        result = _STATE_PATTERN.sub(state_repl, result)
        result = _INPUTS_PATTERN.sub(inputs_repl, result)
        return result

    if isinstance(template, dict):
        return {k: resolve_value(v, state, inputs) for k, v in template.items()}

    if isinstance(template, list):
        return [resolve_value(item, state, inputs) for item in template]

    return template


def merge_step_inputs(step: dict, state: dict, input_data: dict) -> dict:
    """Apply step.inputs templates onto state for agent consumption."""
    step_inputs = step.get("inputs") or {}
    resolved = resolve_value(step_inputs, state, input_data)
    merged = dict(state)
    if isinstance(resolved, dict):
        merged.update(resolved)
    return merged
