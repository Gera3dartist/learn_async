import asyncio
from functools import partial



async def call_soon():
	loop = asyncio.get_running_loop()
	loop.call_soon(partial(print, 'Hello wolrd', flush=True))
	await asyncio.sleep(0.1)
	loop.call_soon(partial(print, 'second call', flush=True))

async def call_later():
	loop = asyncio.get_running_loop()
	loop.call_soon(partial(print, f'starting time: {loop.time()}', flush=True))
	loop.call_later(0.1, partial(print, 'second in 1 second', flush=True))
	loop.call_later(0.4, partial(print, 'second in 3 second', flush=True))
	loop.call_soon(partial(print, 'this is call soon', flush=True))
	loop.call_soon(partial(print, f'final time: {loop.time()}', flush=True))
	await asyncio.sleep(0.5)


async def slow_operation():
	"""
	ref: http://masnun.com/2015/11/20/python-asyncio-future-task-and-the-event-loop.html
	"""
	await asyncio.sleep(1)
	return 'FUTURE IS DONE'


def got_result(future):
	print(future.result())
	loop.stop()


# async def main():
loop = asyncio.get_event_loop()
task = loop.create_task(slow_operation())
task.add_done_callback(got_result)
try:
	loop.run_forever()
finally:
	loop.close()


# asyncio.run(main())
