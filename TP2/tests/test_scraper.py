# Ejemplo de test
import asyncio
import aiohttp

async def test_scraper():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/scrape?url=https://example.com') as resp:
            data = await resp.json()
            assert 'scraping_data' in data
            assert data['status'] == 'success'

asyncio.run(test_scraper())