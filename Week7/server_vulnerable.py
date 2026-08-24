"""Coupon server with an intentional race condition (no lock)."""

import asyncio
from collections import Counter

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Week 7 - Vulnerable Coupon Server")

GROUP_SIZE = 5
TOTAL_COUPONS = (GROUP_SIZE * 2) - 1
coupons = [f"COUPON-{number:02d}" for number in range(1, TOTAL_COUPONS + 1)]
next_coupon_index = 0
student_claims: dict[str, list[str]] = {}


class ClaimRequest(BaseModel):
    student_id: str


@app.get("/")
async def home():
    return {"server": "vulnerable", "lock_enabled": False}


@app.post("/claim")
async def claim_coupon(request: ClaimRequest):
    """Intentionally unsafe: shared state is read across an await."""
    global next_coupon_index

    owned = student_claims.setdefault(request.student_id, [])
    if len(owned) >= 2:
        return {"status": "LIMIT_REACHED", "message": "Maximum 2 coupons"}
    if next_coupon_index >= len(coupons):
        return {"status": "OUT_OF_STOCK", "message": "No coupons remaining"}

    # Several requests can read the same index before any request updates it.
    index_to_claim = next_coupon_index
    await asyncio.sleep(0.1)
    coupon = coupons[index_to_claim]
    owned.append(coupon)
    next_coupon_index = index_to_claim + 1

    return {
        "status": "SUCCESS",
        "student_id": request.student_id,
        "claimed_coupon": coupon,
        "total_owned": len(owned),
    }


@app.get("/summary")
async def summary():
    issued = [coupon for owned in student_claims.values() for coupon in owned]
    counts = Counter(issued)
    return {
        "server": "vulnerable",
        "total_stock": TOTAL_COUPONS,
        "logical_remaining": TOTAL_COUPONS - next_coupon_index,
        "total_responses_issued": len(issued),
        "duplicated_coupons": sorted(c for c, count in counts.items() if count > 1),
        "student_claims": student_claims,
    }
