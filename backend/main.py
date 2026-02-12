from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response

from url_analyzer import (
    check_ip_url,
    check_suspicious_tld,
    check_shortener,
    check_keywords
)

from entropy import entropy_check
from similarity import check_domain_similarity
from scorer import calculate_risk
from logger import log_request


app = FastAPI(
    title="AegisAI URL Defense Engine",
    description="Enterprise-grade URL Threat Detection System",
    version="2.1"
)

# --------------------------
# CORS
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Security Headers
# --------------------------
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        return response

app.add_middleware(SecurityHeadersMiddleware)


# --------------------------
# Request Model
# --------------------------
class URLInput(BaseModel):
    url: str


# --------------------------
# Health Endpoints
# --------------------------
@app.get("/")
def root():
    return {"status": "AegisAI Backend Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}


# --------------------------
# Analyze Endpoint
# --------------------------
@app.post("/analyze")
def analyze_url(data: URLInput):

    try:
        url = data.url.strip()

        if not url:
            raise HTTPException(status_code=400, detail="URL cannot be empty.")

        log_request(url)

        score_list: List[int] = []
        threats: List[str] = []

        # 🔴 LAYER 1 – CRITICAL CHECKS
        critical_checks = [check_ip_url]

        for check in critical_checks:
            score, reason = check(url)
            score_list.append(score)
            if reason:
                threats.append(reason)

            # Early exit if very dangerous
            if score >= 80:
                total_score, risk_level = calculate_risk(score_list)
                return {
                    "input_url": url,
                    "risk_score": total_score,
                    "risk_level": risk_level,
                    "threats_detected": threats,
                    "recommendation": "🚨 Do NOT visit this URL.",
                    "engine_version": "AegisAI v2.1"
                }

        # 🟡 LAYER 2 – STRUCTURAL CHECKS
        secondary_checks = [
            check_suspicious_tld,
            check_shortener,
            check_keywords
        ]

        for check in secondary_checks:
            score, reason = check(url)
            score_list.append(score)
            if reason:
                threats.append(reason)

        partial_score, _ = calculate_risk(score_list)

        # 🟢 LAYER 3 – ADVANCED CHECKS (Only if needed)
        if partial_score < 70:
            advanced_checks = [
                entropy_check,
                check_domain_similarity
            ]

            for check in advanced_checks:
                score, reason = check(url)
                score_list.append(score)
                if reason:
                    threats.append(reason)

        total_score, risk_level = calculate_risk(score_list)

        recommendation = (
            "🚨 Do NOT visit this URL."
            if total_score >= 60
            else "✅ URL appears relatively safe."
        )

        return {
            "input_url": url,
            "risk_score": total_score,
            "risk_level": risk_level,
            "threats_detected": threats,
            "recommendation": recommendation,
            "engine_version": "AegisAI v2.1"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
