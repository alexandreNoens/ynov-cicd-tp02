from fastapi import FastAPI

from app.routes.orders import router as orders_router
from app.routes.promo import router as promo_router

app = FastAPI(title="TP02 API")

app.include_router(orders_router)
app.include_router(promo_router)
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
