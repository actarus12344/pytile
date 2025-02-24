import os
import asyncio
from fastapi import FastAPI, HTTPException
from aiohttp import ClientSession
from pytile import async_login

app = FastAPI()

# Retrieve credentials from environment variables
TILE_EMAIL = os.environ.get("TILE_EMAIL")
TILE_PASSWORD = os.environ.get("TILE_PASSWORD")

if not TILE_EMAIL or not TILE_PASSWORD:
    raise Exception("Please set TILE_EMAIL and TILE_PASSWORD environment variables.")

@app.get("/tile-locations")
async def get_tile_locations():
    try:
        async with ClientSession() as session:
            # Log in using credentials from environment variables
            api = await async_login(TILE_EMAIL, TILE_PASSWORD, session)
            tiles = await api.async_get_tiles()
            locations = {}
            for tile in tiles.values():
                await tile.async_update()  # get the latest location data
                locations[tile.name] = {
                    "latitude": tile.latitude,
                    "longitude": tile.longitude
                }
            return locations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
