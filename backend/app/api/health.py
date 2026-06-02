from fastapi import APIRouter
import redis
from app.config import get_settings
from app.db.arango import get_arango_client

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    settings = get_settings()
    arango_status = "ok"
    redis_status = "ok"
    try:
        client = get_arango_client()
        client.db("_system", username=settings.arango_user, password=settings.arango_password).version()
    except Exception:
        arango_status = "error"
    try:
        r = redis.from_url(settings.redis_url)
        r.ping()
    except Exception:
        redis_status = "error"
    status = "ok" if arango_status == "ok" and redis_status == "ok" else "degraded"
    return {"status": status, "arango": arango_status, "redis": redis_status}
