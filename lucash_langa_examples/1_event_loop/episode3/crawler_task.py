import asyncio
import sys
import time
from typing import Callable, Callable

import httpx

todo = set()


async def progress(url: str, algo: Callable[..., Callable]) -> None:
	task = asyncio.create_task(algo(url))
	todo.add(task)
	start = time.time()
	while len(todo):  # repeatedly check if there is something todo 
		done, pending = await asyncio.wait(todo, timeout=0.5)  # wait for half of 500 ms for task to be done
		todo.difference_update(done)  # remove done from todo

		print(f'Task TODO: {len(todo)}')
	end = time.time()
	print(f'Took: {int(end - start)} seconds')


async def crawl2(prefix: str, url: str = '') -> None:
	url = prefix or url
	client = httpx.AsyncClient()

	try:
		res = await client.get(url)
	finally:
		await client.aclose()
	for line in res.text.splitlines():
		if line.startswith(prefix):
			print(line)
			task = asyncio.create_task(crawl2(line))
			todo.add(task)




async def async_main_wait_for(timeout=3):
	addr = 'https://langa.pl/crawl'
	try:
		await asyncio.wait_for(progress(addr, crawl2), timeout=timeout)
	except asyncio.TimeoutError:
		print('was cancelled')
		for task in todo:
			print(f'Cancelling task: {task}')
			task.cancel()
		done, pending  = await asyncio.wait(todo, timeout=1.0)
		todo.difference_update(done)  # on cancell: remove done
		todo.difference_update(pending)  # on cancell: remove pending
		if todo:
			print('some task still not cancelled')
		print('cancelled all tasks')


async def async_main_cancell(timeout=3):
	addr = 'https://langa.pl/crawl'
	try:
		await progress(addr, crawl2)
	except asyncio.CancelledError:
		print('was cancelled')
		for task in todo:
			print(f'Cancelling task: {task}')
			task.cancel()
		done, pending  = await asyncio.wait(todo, timeout=1.0)
		todo.difference_update(done)  # on cancell: remove done
		todo.difference_update(pending)  # on cancell: remove pending
		if todo:
			print('some task still not cancelled')
		print('cancelled all tasks')

loop = asyncio.get_event_loop()
task = loop.create_task(async_main_cancell())
loop.call_later(4, task.cancel)
loop.run_until_complete(task)
