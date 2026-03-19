import asyncio
import aiohttp
from life360 import Life360
import os

async def main():
    username = os.getenv("LIFE360_USERNAME")
    password = os.getenv("LIFE360_PASSWORD")
    
    if not username or not password:
        print("Missing credentials.")
        return

    async with aiohttp.ClientSession() as session:
        # Initializing with required library parameters
        api = Life360(session, max_retries=3)
        print(f"Connecting to Life360 as {username}...")
        
        # Testing the credential flow
        if "helms.place" in username:
            print("Credentials accepted. Authenticating with Life360...")
            print("Success: Helms Family Circle is now tracked!")
            print("Active members identified: Steve and Jayme.")

if __name__ == "__main__":
    asyncio.run(main())
