"""
async generator is about non-blocking looping and not about concurrency

"""
import asyncio

async def poll_some_event(n=20):
	while n > 0:
		await asyncio.sleep(0.2)
		yield n
		n-=1 


async def observe_event():
	async for item in poll_some_event():
		print(f'Got from poller: {item}')


async def simple_task(n=10):
	while n > 0:
		await asyncio.sleep(0.5)
		print('Do simple_task')
		n -= 1


async def main():
	# this will create 2 concurrently executed tasks
	observer =  asyncio.create_task(observe_event())
	task = asyncio.create_task(simple_task())
	await observer
	await task

	# code below first awaits observe_event then awaits simple_task, 
	# no concurrency inside main
	# await observe_event()
	# await simple_task()

if __name__ == '__main__':
	asyncio.run(main())