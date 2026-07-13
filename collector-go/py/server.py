from fastapi import FastAPI
import uvicorn

app = FastAPI()
POOL_LAST_PRICE = {}
MIN_SPREAD = 0.005

@app.post("/strategy")
async def strategy(data: dict):
    pool = data["pool"]
    price = data["price"]

    if pool not in POOL_LAST_PRICE:
        POOL_LAST_PRICE[pool] = price
        return {"trade": False}

    last = POOL_LAST_PRICE[pool]
    spread = abs(price - last) / last

    print(f"[{pool}] 价差: {spread:.2%}")

    if spread > MIN_SPREAD:
        POOL_LAST_PRICE[pool] = price
        return {"trade": True}

    return {"trade": False}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)