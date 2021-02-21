"""
Episode 2
URL: https://www.youtube.com/watch?v=Xbl7XjFYsN4&app=desktop

"""
import asyncio
from datetime import datetime as dt


def sooner(name):
	print(f'{name} inside sooner, time: {dt.now()}')


loop = asyncio.get_event_loop()

loop.call_soon(sooner, 'first')
loop.call_soon(sooner, 'second')

print('>>>>go')
loop.run_until_complete(asyncio.sleep(2))
print('DONE')