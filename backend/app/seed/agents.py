AGENT_SEED_DATA = [
    {
        "slug": "browser-agent",
        "name": "Browser Agent",
        "version": "1.0.0",
        "description": "Navigates websites and extracts raw content via Browser Use.",
        "status": "active",
        "owner": "system",
        "implementation": {
            "type": "python",
            "entrypoint": "app.agents.browser:run",
            "framework": "browser-use",
            "module": "browser_use",
        },
        "category": "automation",
        "tags": ["web", "scrape"],
        "input_schema": {
            "type": "object",
            "properties": {
                "urls": {"type": "array", "items": {"type": "string"}},
                "browser_task": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {"raw_content": {"type": "string"}},
            "required": ["raw_content"],
        },
        "config_schema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "default": "gpt-4o"},
                "timeout_seconds": {"type": "integer", "default": 300},
            },
        },
        "default_config": {"model": "gpt-4o", "timeout_seconds": 300},
    },
    {
        "slug": "extractor",
        "name": "Extractor Agent",
        "version": "1.0.0",
        "description": "Structures raw content into JSON via Instructor.",
        "status": "active",
        "owner": "system",
        "implementation": {
            "type": "python",
            "entrypoint": "app.agents.extractor:run",
            "framework": "instructor",
            "module": "instructor",
        },
        "category": "extraction",
        "tags": ["structured", "llm"],
        "input_schema": {
            "type": "object",
            "properties": {"raw_content": {"type": "string"}},
        },
        "output_schema": {
            "type": "object",
            "properties": {"structured_data": {"type": "object"}},
        },
        "config_schema": {"type": "object", "properties": {"model": {"type": "string"}}},
        "default_config": {"model": "gpt-4o"},
    },
    {
        "slug": "analyzer",
        "name": "Analyzer Agent",
        "version": "1.0.0",
        "description": "Analyzes structured data and produces insights via LiteLLM.",
        "status": "active",
        "owner": "system",
        "implementation": {
            "type": "python",
            "entrypoint": "app.agents.analyzer:run",
            "framework": "litellm",
            "module": "litellm",
        },
        "category": "analysis",
        "tags": ["llm", "insights"],
        "input_schema": {
            "type": "object",
            "properties": {"structured_data": {"type": "object"}},
        },
        "output_schema": {
            "type": "object",
            "properties": {"analysis": {"type": "string"}},
        },
        "config_schema": {"type": "object", "properties": {"model": {"type": "string"}}},
        "default_config": {"model": "gpt-4o"},
    },
    {
        "slug": "reporter",
        "name": "Reporter Agent",
        "version": "1.0.0",
        "description": "Formats analysis into a markdown report.",
        "status": "active",
        "owner": "system",
        "implementation": {
            "type": "python",
            "entrypoint": "app.agents.reporter:run",
            "framework": "litellm",
            "module": "litellm",
        },
        "category": "delivery",
        "tags": ["report"],
        "input_schema": {
            "type": "object",
            "properties": {"analysis": {"type": "string"}},
        },
        "output_schema": {
            "type": "object",
            "properties": {"report": {"type": "string"}},
        },
        "config_schema": {"type": "object"},
        "default_config": {},
    },
    {
        "slug": "qa-tester",
        "name": "QA Tester Agent",
        "version": "1.0.0",
        "description": "Runs browser-based QA scenarios via Browser Use.",
        "status": "active",
        "owner": "system",
        "implementation": {
            "type": "python",
            "entrypoint": "app.agents.qa_tester:run",
            "framework": "browser-use",
            "module": "browser_use",
        },
        "category": "automation",
        "tags": ["qa", "browser"],
        "input_schema": {
            "type": "object",
            "properties": {
                "target_url": {"type": "string"},
                "scenario": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {"qa_result": {"type": "object"}},
        },
        "config_schema": {"type": "object", "properties": {"model": {"type": "string"}}},
        "default_config": {"model": "gpt-4o"},
    },
]

WORKFLOW_SEED_TEMPLATES = [
    {
        "slug": "competitor-intel",
        "name": "Competitor Intelligence",
        "description": "Scrape → extract → analyze competitor pages.",
        "is_template": True,
        "definition": {
            "schema_version": "1.0",
            "inputs": {
                "urls": {"type": "array", "items": "string", "required": True},
                "email": {"type": "string", "required": False},
            },
            "state_keys": ["urls", "email", "raw_content", "structured_data", "analysis"],
            "steps": [
                {
                    "id": "scrape",
                    "agent": "browser-agent",
                    "config": {"model": "gpt-4o"},
                    "inputs": {
                        "urls": "{{ inputs.urls }}",
                        "browser_task": "Extract pricing and plan names from each URL.",
                    },
                    "on_error": "fail",
                },
                {
                    "id": "extract",
                    "agent": "extractor",
                    "config": {},
                    "inputs": {},
                    "on_error": "fail",
                },
                {
                    "id": "analyze",
                    "agent": "analyzer",
                    "config": {"model": "gpt-4o"},
                    "inputs": {},
                    "on_error": "fail",
                },
            ],
        },
    },
    {
        "slug": "qa-smoke",
        "name": "QA Smoke Test",
        "description": "Reuses browser stack for a simple QA scenario.",
        "is_template": True,
        "definition": {
            "schema_version": "1.0",
            "inputs": {
                "target_url": {"type": "string", "required": True},
                "scenario": {"type": "string", "required": False},
            },
            "state_keys": ["target_url", "scenario", "qa_result"],
            "steps": [
                {
                    "id": "qa-run",
                    "agent": "qa-tester",
                    "config": {"model": "gpt-4o"},
                    "inputs": {
                        "target_url": "{{ inputs.target_url }}",
                        "scenario": "{{ inputs.scenario }}",
                    },
                    "on_error": "fail",
                },
            ],
        },
    },
]
