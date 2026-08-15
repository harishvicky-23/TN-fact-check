import json
import asyncio
from datetime import date
from typing import Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from crew.fact_check_crew import run_fact_check

# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="TN Fact Check AI",
    description="Multi-agent AI fact-checking system",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# --------------------------------------------------
# Request model
# --------------------------------------------------

class FactCheckRequest(BaseModel):
    user_query: str
    time_period: str = "not specified"


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "TN Fact Check AI backend is running"
    }


# --------------------------------------------------
# Streaming fact-check endpoint (SSE)
# --------------------------------------------------

@app.get("/api/fact-check-stream")
async def fact_check_stream(
    user_query: str,
    time_period: str = "not specified"
):
    queue = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def on_task_completed(stage: str, output: Any):
        if stage == "analyzing_done":
            loop.call_soon_threadsafe(
                queue.put_nowait,
                {
                    "status": "researching",
                    "message": "Research Investigator searching web and gathering articles..."
                }
            )
        elif stage == "gathering_done":
            loop.call_soon_threadsafe(
                queue.put_nowait,
                {
                    "status": "verifying",
                    "message": "Fact Verification Specialist cross-checking sources..."
                }
            )
        elif stage == "verifying_done":
            loop.call_soon_threadsafe(
                queue.put_nowait,
                {
                    "status": "writing",
                    "message": "Fact-Check Report Writer compiling structured report..."
                }
            )

    async def run_crew_async():
        try:
            # Initial state
            loop.call_soon_threadsafe(
                queue.put_nowait,
                {
                    "status": "analyzing",
                    "message": "Fact-Check Query Analyzer triaging query and setting time window..."
                }
            )

            current_date = date.today().isoformat()

            result = await asyncio.to_thread(
                run_fact_check,
                user_query=user_query,
                time_period=time_period,
                current_date=current_date,
                on_task_completed=on_task_completed
            )

            # Extract output data
            report_data = None
            if hasattr(result, 'pydantic') and result.pydantic:
                report_data = result.pydantic.model_dump()
            elif hasattr(result, 'raw') and result.raw:
                try:
                    report_data = json.loads(result.raw)
                except Exception:
                    report_data = {"raw": result.raw}
            else:
                report_data = {"raw": str(result)}

            loop.call_soon_threadsafe(
                queue.put_nowait,
                {
                    "status": "completed",
                    "result": report_data
                }
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            loop.call_soon_threadsafe(
                queue.put_nowait,
                {
                    "status": "error",
                    "message": str(e)
                }
            )
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    # Launch task in background
    asyncio.create_task(run_crew_async())

    async def event_generator():
        while True:
            item = await queue.get()
            if item is None:
                break
            yield {"data": json.dumps(item)}

    return EventSourceResponse(event_generator())


# --------------------------------------------------
# Standard POST fact-check endpoint
# --------------------------------------------------

@app.post("/fact-check")
def fact_check(request: FactCheckRequest):
    current_date = date.today().isoformat()

    result = run_fact_check(
        user_query=request.user_query,
        time_period=request.time_period,
        current_date=current_date
    )

    report_data = None
    if hasattr(result, 'pydantic') and result.pydantic:
        report_data = result.pydantic.model_dump()
    elif hasattr(result, 'raw') and result.raw:
        try:
            report_data = json.loads(result.raw)
        except Exception:
            report_data = {"raw": result.raw}
    else:
        report_data = {"raw": str(result)}

    return {
        "query": request.user_query,
        "time_period": request.time_period,
        "current_date": current_date,
        "result": report_data
    }