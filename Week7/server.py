"""Coupon server protected by asyncio.Lock."""

import asyncio
from collections import Counter

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Week 7 - Safe Coupon Server")

GROUP_SIZE = 5
TOTAL_COUPONS = (GROUP_SIZE * 2) - 1
coupons = [f"COUPON-{number:02d}" for number in range(1, TOTAL_COUPONS + 1)]
next_coupon_index = 0
student_claims: dict[str, list[str]] = {}
coupon_lock = asyncio.Lock()


class ClaimRequest(BaseModel):
    student_id: str


@app.get("/")
async def home():
    return {"server": "safe", "lock_enabled": True}


@app.post("/claim")
async def claim_coupon(request: ClaimRequest):
    global next_coupon_index

    # Quota check, stock check, and update form one protected critical section.
    async with coupon_lock:
        owned = student_claims.setdefault(request.student_id, [])
        if len(owned) >= 2:
            return {"status": "LIMIT_REACHED", "message": "Maximum 2 coupons"}
        if next_coupon_index >= len(coupons):
            return {"status": "OUT_OF_STOCK", "message": "No coupons remaining"}

        index_to_claim = next_coupon_index
        await asyncio.sleep(0.1)
        coupon = coupons[index_to_claim]
        owned.append(coupon)
        next_coupon_index += 1

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
        "server": "safe",
        "total_stock": TOTAL_COUPONS,
        "logical_remaining": TOTAL_COUPONS - next_coupon_index,
        "total_responses_issued": len(issued),
        "duplicated_coupons": sorted(c for c, count in counts.items() if count > 1),
        "student_claims": student_claims,
    }
