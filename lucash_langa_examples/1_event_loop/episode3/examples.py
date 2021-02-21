import asyncio
from datetime import datetime


def print_name(name: str = '') -> None:
	print(datetime.now())


async def keep_printing(name: str = '') -> None:
	while True:
		print(name, end=' ')
		print_name(name)
		try:
			await asyncio.sleep(0.5)  # cancellation will raise CancellError in await line
		except asyncio.CancelledError:
			print(f'{name} was cancelled')
			break


async def async_main(timeout: int = 2) -> None:
	try:
		await asyncio.wait_for(
			asyncio.gather(
				keep_printing('First'),
				keep_printing('Second'),
				keep_printing('Third'),
			), timeout)
	except asyncio.TimeoutError:
		print('oops, time is up')


asyncio.run(async_main())
