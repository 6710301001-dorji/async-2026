# Program 1: The First Coroutine Function
# Concept: Understanding async def and how it differs from a normal function.
import asyncio

async def greet():
    print("Hello!")

coro_object = greet()

print(type(coro_object))

coro_object.close()
