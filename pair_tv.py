import asyncio
import aiopylgtv
import json
import os

TV_IP = "192.168.0.17"
KEY_FILE = "tv_key.json"

async def get_tv_key():
    """Pair with the TV and store the key."""
    client = aiopylgtv.WebOsClient(TV_IP)

    try:
        await client.connect()
        tv_key = client.client_key

        # Save key to file
        with open(KEY_FILE, "w") as f:
            json.dump({"TV_KEY": tv_key}, f)

        print(f"✅ Connected! Your Persistent TV Key is: {tv_key}")
        print("🎯 Key saved in tv_key.json")

    except Exception as e:
        print(f"❌ Connection failed: {e}")

asyncio.run(get_tv_key())
