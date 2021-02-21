import asyncio
from aiohttp import ClientSession
import time

async def fetch(url, session):
		async with session.post(url) as resp:
			resp = await resp.read()
			print(resp)


# asyncio.run(fetch("http://httpbin.org/headers"))


async def run(n):
	url = "http://httpbin.org/headers"
	tasks = []
	async with ClientSession() as session:
		for i in range(n):
			task = asyncio.ensure_future(fetch(url, session))
			tasks.append(task)

		await asyncio.gather(*tasks)

# asyncio.run(run(4))
async def bound_fetch(sem, url, session):
	async with sem:
		await fetch(url, session)

#-------------------------------
#   high performance client
#-------------------------------
async def run_fast(n):
	url = 'http://127.0.0.1:8080/api/introspect'
	tasks = []
	sem = asyncio.Semaphore(1000)
	async with ClientSession() as session:
		for i in range(n):
			task = asyncio.ensure_future(bound_fetch(sem, url, session))
			tasks.append(task)
		await asyncio.gather(*tasks)

start = time.time()
asyncio.run(run_fast(1000))
print(f'\nTook: {time.time() - start}')
