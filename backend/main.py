import asyncio
import requests
import pandas as pd
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from tenacity import retry, wait_fixed, stop_after_attempt, after_log
from utils.dlq import add_to_dlq
from utils.redis_cache import cache_data, get_cached_data
from utils.notifications import send_email, send_slack_message
from prometheus_client import start_http_server, Summary, Counter, Histogram
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
FAILED_REQUESTS = Counter('failed_requests_total', 'Total number of failed requests')
PIPELINE_EXECUTION_TIME = Histogram('pipeline_execution_seconds', 'Pipeline execution time')

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline_status = []
pipeline_logs = []
connected_clients: List[WebSocket] = []

@retry(wait=wait_fixed(5), stop=stop_after_attempt(3), after=after_log(logger, logging.ERROR))
def fetch_data(api_url: str):
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

@app.get("/api/pipeline-status")
def get_pipeline_status():
    return pipeline_status

@app.get("/api/pipeline-logs")
def get_pipeline_logs():
    return pipeline_logs

@app.get("/api/transformed-data")
def get_transformed_data():
    # Replace with actual logic to fetch transformed data
    return [
        {"timestamp": "2025-03-24T13:00:00Z", "value": 10},
        {"timestamp": "2025-03-24T14:00:00Z", "value": 15},
        {"timestamp": "2025-03-24T15:00:00Z", "value": 20},
    ]

@app.get("/api/raw-data")
def get_raw_data():
    # Replace with actual logic to fetch raw data
    return [
        {"timestamp": "2025-03-24T13:00:00Z", "value": 5},
        {"timestamp": "2025-03-24T14:00:00Z", "value": 10},
        {"timestamp": "2025-03-24T15:00:00Z", "value": 15},
    ]

@REQUEST_TIME.time()
@app.post("/etl/api")
async def etl_api(api_url: str):
    try:
        pipeline_status.append('Task Started: Extract from API')
        await broadcast_status('Task Started: Extract from API')
        data = fetch_data(api_url)
        pipeline_status.append('Task Completed: Extract from API')
        await broadcast_status('Task Completed: Extract from API')
    except Exception as e:
        FAILED_REQUESTS.inc()
        add_to_dlq(api_url, str(e))
        pipeline_status.append('Task Failed: Extract from API')
        await broadcast_status('Task Failed: Extract from API')
        logger.error(f"Error extracting data from API: {e}")
        send_email('ETL Pipeline Error', f'Error extracting data from API: {e}', 'admin@example.com')
        send_slack_message('#etl-alerts', f'Error extracting data from API: {e}')
        raise HTTPException(status_code=500, detail=str(e))

    # Simulate other tasks and logging
    pipeline_logs.append('Data extracted successfully.')
    await broadcast_status('Data extracted successfully.')
    return {"status": "success", "data": data}

@app.websocket("/ws/etl_status")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)

async def broadcast_status(message: str):
    for client in connected_clients:
        await client.send_text(message)

if __name__ == "__main__":
    start_http_server(8001)  # Expose Prometheus metrics
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)