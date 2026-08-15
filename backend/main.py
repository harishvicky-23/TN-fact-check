from datetime import date

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
        "http://127.0.0.1:5173"
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
# Fact-check endpoint
# --------------------------------------------------

@app.post("/fact-check")
def fact_check(request: FactCheckRequest):

    current_date = date.today().isoformat()

    result = run_fact_check(
        user_query=request.user_query,
        time_period=request.time_period,
        current_date=current_date
    )

    return {
        "query": request.user_query,
        "time_period": request.time_period,
        "current_date": current_date,
        "result": result.raw
    }