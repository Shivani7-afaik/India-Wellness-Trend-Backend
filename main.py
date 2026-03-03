from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scan")
def scan_trends():

    # Placeholder example trends (we replace with real data next)
    trends = [
        {
            "name": "Magnesium Glycinate",
            "search_growth": 420,
            "reddit_mentions": 88,
            "youtube_videos": 120,
            "competition_score": 35,
            "trend_score": 84,
            "stage": "Pre-Mainstream",
            "opportunity_brief": "Launch India-focused sleep supplement brand targeting urban women 25-40."
        },
        {
            "name": "Cold Plunge Therapy",
            "search_growth": 300,
            "reddit_mentions": 120,
            "youtube_videos": 220,
            "competition_score": 60,
            "trend_score": 70,
            "stage": "Emerging",
            "opportunity_brief": "Build affordable home cold plunge tubs for Indian apartments."
        }
    ]

    return {
        "scan_date": datetime.today().strftime('%Y-%m-%d'),
        "trends": trends
    }
