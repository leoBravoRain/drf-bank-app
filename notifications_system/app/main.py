import asyncio

from app.consumer import consume
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Start the RabbitMQ consumer in the background
    loop = asyncio.get_event_loop()
    app.state.rabbitmq_connection = await consume()


@app.on_event("shutdown")
async def shutdown_event():
    # Gracefully close RabbitMQ connection
    await app.state.rabbitmq_connection.close()


@app.get("/")
def hello():
    print('GET on "/"')
    return {"message": "Hello from Docker + FastAPI!"}
