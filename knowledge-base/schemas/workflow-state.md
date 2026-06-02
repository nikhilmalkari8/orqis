# Schemas — Workflow state (LangGraph)

**Type:** `app.core.workflow_state.WorkflowState` (TypedDict)

Passed through all nodes; grows as steps run.

## User / run inputs

| Key | Set by | Used by |
|-----|--------|---------|
| `urls` | `input_data` | browser-agent |
| `email` | `input_data` | optional downstream |
| `browser_task` | step inputs | browser-agent |
| `target_url`, `scenario` | `input_data` | qa-tester |

## Step outputs

| Key | Producer | Consumer |
|-----|----------|----------|
| `raw_content` | browser-agent | extractor |
| `structured_data` | extractor | analyzer |
| `analysis` | analyzer | reporter |
| `report` | reporter | — |
| `qa_result` | qa-tester | — |

## Internal (Orqis-injected)

| Key | Set by |
|-----|--------|
| `_execution_id` | worker |
| `_workflow_id` | worker |
| `_current_step_id` | compiler wrapper |
| `_step_config` | compiler from `step.config` |

## Rules

- Adding a new agent: document new keys here + in agent seed `output_schema`.
- Compiler merges `step.inputs` into state before each node.
