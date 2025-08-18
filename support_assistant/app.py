import asyncio
import json

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

from .shopify_service import service_from_env

app = FastAPI()
templates = Jinja2Templates(directory="templates")
service = service_from_env()


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def sales_event_generator():
    while True:
        new_sales = service.sync_orders()
        for sale in new_sales:
            payload = {"sale": sale, "total": service.get_total_sales()}
            yield f"data: {json.dumps(payload)}\n\n"
        await asyncio.sleep(5)


@app.get("/sales/stream")
async def sales_stream():
    return StreamingResponse(sales_event_generator(), media_type="text/event-stream")


