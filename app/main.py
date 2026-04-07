from fastapi import FastAPI

app = FastAPI(title="TP02 API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
