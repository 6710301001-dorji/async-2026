"""Simulate five Client Hunters concurrently from one computer."""

import argparse
import asyncio

import httpx


async def claim(client: httpx.AsyncClient, server_url: str, student_id: str):
    try:
        response = await client.post(
            f"{server_url}/claim",
            json={"student_id": student_id},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError) as error:
        return {"status": "ERROR", "student_id": student_id, "message": str(error)}


async def main(server_url: str):
    # Each virtual student sends two claims, like five separate group members.
    hunters = [f"VIRTUAL-STUDENT-{number:02d}" for number in range(1, 6)]
    async with httpx.AsyncClient() as client:
        tasks = [claim(client, server_url, hunter) for hunter in hunters for _ in range(2)]
        results = await asyncio.gather(*tasks)

        for result in results:
            student = result.get("student_id", "-")
            detail = result.get("claimed_coupon", result.get("message", ""))
            print(f"{student:20} {result['status']:15} {detail}")

        response = await client.get(f"{server_url}/summary", timeout=5.0)
        response.raise_for_status()
        summary = response.json()

    print("\nSummary")
    print(f"Server:              {summary['server']}")
    print(f"Total stock:         {summary['total_stock']}")
    print(f"Responses issued:    {summary['total_responses_issued']}")
    print(f"Logical remaining:   {summary['logical_remaining']}")
    print(f"Duplicated coupons:  {summary['duplicated_coupons']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default="http://127.0.0.1:8088")
    args = parser.parse_args()
    asyncio.run(main(args.server.rstrip("/")))
