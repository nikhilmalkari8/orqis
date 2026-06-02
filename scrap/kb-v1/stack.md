# Orqis — Stack

| Concern | Package / service | Notes |
|---------|-------------------|--------|
| API | fastapi, uvicorn | Port 8000 |
| Validation | pydantic v2 | schemas + Settings |
| DB driver | python-arango | Sync client in repos |
| Auth | python-jose, passlib | HS256 JWT |
| Queue | celery[redis] | Worker required for runs |
| Broker | redis:7 | DB 0 broker, DB 1 results |
| DB | arangodb:3.11 | Port 8529, db `orqis` |
| Graph runtime | langgraph | Sequential MVP |
| Tracing | langsmith | Optional; `LANGSMITH_TRACING` |
| LLM (real agents) | litellm, instructor, openai | When `MOCK_AGENTS=false` |
| Browser (real) | browser-use, langchain-openai | Optional |
| UI | react 19, vite, axios | Port 5173 |

**Not in MVP:** MongoDB, form builder, Vercel hosting layer.
