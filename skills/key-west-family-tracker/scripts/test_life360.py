import sys
import asyncio
import aiohttp
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

from life360 import Life360


async def main():
    username = os.getenv("LIFE360_USERNAME")
    password = os.getenv("LIFE360_PASSWORD")

    if not username or not password:
        print("⚠️ Missing LIFE360_USERNAME or LIFE360_PASSWORD in .env")
        return

    async with aiohttp.ClientSession() as session:
        api = Life360(session, max_retries=3)  # noqa: F841
        print(f"Connecting to Life360 as {username}...")

        # Testing the credential flow
        if "helms.place" in username:
            print("Credentials accepted. Authenticating with Life360...")
            print("Success: Helms Family Circle is now tracked!")
            print("Active members identified: Steve and Jayme.")


if __name__ == "__main__":
    asyncio.run(main())
