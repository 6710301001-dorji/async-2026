# Week 7: Solo Client-Server Race Condition Simulation

This project adapts the original group activity so that one student can perform
the experiment on a single computer. The program transparently simulates five
Client Hunters; it does not claim that five real group members participated.

## Files

- `server_vulnerable.py` - Server Machine 1 has no lock and intentionally
  demonstrates a race condition.
- `server.py` - Server Machine 2 protects its critical section with
  `asyncio.Lock`.
- `client.py` - Simulates five Client Hunters, with each hunter sending two
  requests concurrently.
- `run_demo.py` - Starts each server and runs both experiments automatically.

The coupon inventory follows the assignment formula:
`(5 x 2) - 1 = 9 coupons`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install fastapi uvicorn httpx
```

## Run the complete solo demonstration

```bash
python run_demo.py
```

Expected observations:

- The vulnerable server may issue the same coupon code to multiple requests.
  This happens because requests read the shared index before an `await` without
  holding a lock.
- The safe server issues no more than nine unique coupons. The tenth request is
  rejected because the inventory is empty.

## Run manually using three terminals

Terminal 1:

```bash
uvicorn server_vulnerable:app --port 8088
```

Terminal 2:

```bash
uvicorn server:app --port 8089
```

Terminal 3:

```bash
python client.py --server http://127.0.0.1:8088
python client.py --server http://127.0.0.1:8089
```

Restart both servers before repeating the experiment to reset their in-memory
state. Screenshots of both results can be included in the submission to explain
the difference between the vulnerable and protected critical sections.
