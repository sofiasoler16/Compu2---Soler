
# ==============================
# File: client.py
# ==============================
import asyncio
import aiohttp
import sys


async def main():
    if len(sys.argv) < 3:
        print("Uso: python client.py <host:port> <url>")
        sys.exit(1)
    hostport = sys.argv[1]
    url = sys.argv[2]
    base = f"http://{hostport}"

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base}/scrape", params={"url": url}) as resp:
            print("Status:", resp.status)
            print(await resp.text())


if __name__ == "__main__":
    asyncio.run(main())