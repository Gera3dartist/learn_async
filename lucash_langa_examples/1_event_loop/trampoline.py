import asyncio
from datetime import datetime as dt



def trampoline(loop, name):
	print(f'[{name}] time: {dt.now()}')
	loop.call_later(0.5, trampoline, loop, name)


def long_running_cpu_task():
	sum = 0
	for i in range(1000):
		for j in range(10000):
			sum += (i+j)
	print(f'>>SUM: {sum}')
	return sum


def main():
	loop = asyncio.get_event_loop()
	loop.set_debug(True)

	loop.call_soon(trampoline, loop, 'First')	
	loop.call_soon(trampoline, loop, 'Second')
	loop.call_soon(trampoline, loop, 'Third')
	loop.call_soon(long_running_cpu_task)
	loop.call_later(2, loop.stop)



	loop.run_forever()

if __name__ == '__main__':
	main()