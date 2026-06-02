# Schemas — Workflow definition

Stored in `workflows.definition` and accepted by `POST/PUT /api/workflows`.

## Root

```yaml
schema_version: "1.0"   # required
inputs: {}              # param metadata for UI/run
state_keys: []          # optional documentation
steps: []               # required, non-empty
```

## `inputs` entry

```yaml
urls:
  type: array
  items: string
  required: true
```

## `steps[]` entry

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Unique in workflow; LangGraph node name |
| `agent` | yes | Must match `agents.slug` in registry |
| `config` | no | Passed to agent as `state._step_config` |
| `inputs` | no | Template map; see templating |
| `on_error` | no | MVP: `fail` only |

## Templating (`core/input_resolver.py`)

| Pattern | Resolves from |
|---------|----------------|
| `{{ state.key }}` | Current workflow state |
| `{{ inputs.key }}` | Run `input_data` |

## Validation (`WorkflowCompiler.validate`)

- `schema_version == "1.0"`
- Non-empty `steps`
- Unique `step.id`
- Each `step.agent` ∈ `AgentRegistry.slugs()`

## Example

```yaml
steps:
  - id: scrape
    agent: browser-agent
    config: { model: gpt-4o }
    inputs:
      urls: "{{ inputs.urls }}"
  - id: extract
    agent: extractor
```
