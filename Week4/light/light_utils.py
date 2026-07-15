import httpx


# This is the teacher's light server.
BASE_URL = "http://172.16.2.117:8088"


async def get_lights(student_id):
    url = f"{BASE_URL}/api/{student_id}/lights"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


async def control_light(student_id, light_id, status):
    url = f"{BASE_URL}/api/{student_id}/lights/{light_id}"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"status": status})
        return response.json()


async def reset_lights(student_id):
    url = f"{BASE_URL}/api/{student_id}/lights/reset"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url)
        return response.json()
