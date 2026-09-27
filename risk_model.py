from __future__ import annotations
import os
import pandas as pd
from typing import Any, Dict, List

DATASET_FILENAME = "ai_applicability_scores.csv"

FALLBACK_CATALOG: Dict[str, float] = {
    "Data Analyst": 0.75,
    "Customer Support Representative": 0.82,
    "Software Engineer": 0.68,
    "Graphic Designer": 0.64,
    "Legal Assistant": 0.71,
}

def load_applicability_dataset() -> pd.DataFrame | None:
    if os.path.exists(DATASET_FILENAME):
        try:
            df = pd.read_csv(DATASET_FILENAME)
            return df
        except Exception:
            return None
    return None

def list_jobs() -> List[str]:
    df = load_applicability_dataset()
    if df is not None:
        title_col = [c for c in df.columns if "title" in c.lower() or "occupation" in c.lower() or "name" in c.lower()]
        if title_col:
            return sorted(df[title_col[0]].dropna().unique().tolist())
    return list(FALLBACK_CATALOG.keys())

def calculate_job_risk(job_title: str) -> Dict[str, Any]:
    df = load_applicability_dataset()
    score = None

    if df is not None:
        title_col = [c for c in df.columns if "title" in c.lower() or "occupation" in c.lower() or "name" in c.lower()]
        score_col = [c for c in df.columns if "score" in c.lower() or "applicability" in c.lower()]
        if title_col and score_col:
            match = df[df[title_col[0]].str.lower() == job_title.lower()]
            if not match.empty:
                score = float(match.iloc[0][score_col[0]])

    if score is None:
        score = FALLBACK_CATALOG.get(job_title, 0.50)

    # Normalize score to percentage (0 - 100)
    percentage = score * 100 if score <= 1.0 else score
    percentage = round(percentage, 1)

    if percentage >= 70:
        risk_level = "High"
        recommendation = "High applicability to generative AI. Pivot focus toward strategic direction, cross-domain coordination, and human oversight."
    elif percentage >= 45:
        risk_level = "Moderate"
        recommendation = "Substantial task exposure. Adoption of human-in-the-loop AI workflows is recommended."
    else:
        risk_level = "Low"
        recommendation = "Low direct AI applicability. Core work remains predominantly dependent on physical presence or complex human nuance."

    return {
        "job_title": job_title,
        "job_risk": risk_level,
        "overall_probability": percentage,
        "recommendation": recommendation,
    }