from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd

app = FastAPI()

# -----------------------------
# 1. LOAD YOUR KEYWORD DATA
# -----------------------------

data = [
    # Google Trends Based
    {"keyword": "Hair Loss", "type": "Problem", "growth": 600, "source": "Google"},
    {"keyword": "Low Estrogen Symptoms", "type": "Problem", "growth": 450, "source": "Google"},
    {"keyword": "What is oxidative stress", "type": "Problem", "growth": 300, "source": "Google"},
    {"keyword": "fatty liver symptoms", "type": "Problem", "growth": 200, "source": "Google"},
    {"keyword": "endometriosis symptoms", "type": "Problem", "growth": 400, "source": "Google"},
    {"keyword": "menopause symptoms", "type": "Problem", "growth": 250, "source": "Google"},
    {"keyword": "what is insulin resistance", "type": "Problem", "growth": 300, "source": "Google"},

    # Reddit Supplements
    {"keyword": "magnesium glycinate", "type": "Ingredient", "growth": 180, "source": "Reddit"},
    {"keyword": "creatine gummies", "type": "Format", "growth": 220, "source": "Reddit"},
    {"keyword": "lab-tested supplements", "type": "Science", "growth": 260, "source": "Reddit"},
    {"keyword": "biohacking protocols", "type": "Science", "growth": 240, "source": "Reddit"},
    {"keyword": "anti-aging supplements 30s", "type": "Problem", "growth": 210, "source": "Reddit"},
    {"keyword": "psyllium husk", "type": "Ingredient", "growth": 170, "source": "Reddit"},
    {"keyword": "NAC supplement", "type": "Ingredient", "growth": 190, "source": "Reddit"},

    # Indian Skincare
    {"keyword": "Sunscreen confusion", "type": "Problem", "growth": 230, "source": "Reddit"},
    {"keyword": "Minimal skincare routines", "type": "Trend Shift", "growth": 260, "source": "Reddit"},
    {"keyword": "PCOD-related skin issues", "type": "Problem", "growth": 280, "source": "Reddit"},
]

df = pd.DataFrame(data)

# -----------------------------
# 2. SCORING LOGIC
# -----------------------------

def score_trends(df):

    # Normalize growth
    df["growth_score"] = df["growth"] / df["growth"].max() * 100

    # Problem-led demand gets boost
    df["demand_score"] = df["type"].apply(
        lambda x: 90 if x == "Problem" else 70
    )

    # Science & format are early-stage
    df["early_signal_score"] = df["type"].apply(
        lambda x: 85 if x in ["Science", "Format"] else 70
    )

    # Saturation proxy (Google more mainstream than Reddit)
    df["saturation_score"] = df["source"].apply(
        lambda x: 60 if x == "Google" else 40
    )

    # Final weighted score
    df["final_score"] = (
        df["growth_score"] * 0.4 +
        df["demand_score"] * 0.25 +
        df["early_signal_score"] * 0.2 -
        df["saturation_score"] * 0.15
    )

    return df.sort_values(by="final_score", ascending=False)

# -----------------------------
# 3. OPPORTUNITY BRIEF GENERATOR
# -----------------------------

def generate_brief(row):

    return {
        "trend": row["keyword"],
        "why_now": f"{int(row['growth'])}% growth signal in India-backed data.",
        "startup_angle": f"Build a D2C product targeting '{row['keyword']}' for Indian consumers.",
        "product_idea": f"Launch evidence-backed, affordable version focused on Indian market gap.",
        "risk": "Regulatory scrutiny or fast competition entry.",
        "score": round(row["final_score"], 2)
    }

# -----------------------------
# 4. API ENDPOINT
# -----------------------------

@app.get("/scan")
def scan_trends():

    scored = score_trends(df)
    top_trends = scored.head(8)

    results = [generate_brief(row) for _, row in top_trends.iterrows()]

    return {
        "total_keywords_scanned": len(df),
        "top_trends_identified": len(results),
        "trends": results
    }

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
