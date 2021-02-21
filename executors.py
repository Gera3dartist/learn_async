"""
Reference: https://pymotw.com/3/asyncio/executors.html

"""
import asyncio
import concurrent.futures
import logging
import sys
import time


def blocking_function(n):
    log = logging.getLogger(f'bloblocking_function({n}')
    log.info('running')
    time.sleep(0.1)
    log.info('done')
    return n ** 2

async def run_blocking_task(executor, loop, n):
    log = logging.getLogger('run_blocking_task')
    log.info('starting')

    log.info('creating executor tasks')
    blocking_tasks = [
        loop.run_in_executor(executor, blocking_function, i) for i in range(n)
    ]

    log.info('waiting for executor tasks')
    for res in await asyncio.gather(*blocking_tasks):
        log.info(f'Blocking res: {res}')
    log.info('exiting')


if __name__ == '__main__':
    def get_thread_pool():
        logging.basicConfig(
            level=logging.INFO,
            format='%(threadName)10s %(name)18s: %(message)s',
            stream=sys.stderr
        )
        return concurrent.futures.ThreadPoolExecutor(max_workers=5)


    def get_process_pool():
        logging.basicConfig(
            level=logging.INFO,
            format='PID %(process)5s %(name)18s: %(message)s',
            stream=sys.stderr,
        )
        return concurrent.futures.ProcessPoolExecutor(max_workers=3)


    executor = get_process_pool()
    # executor = get_thread_pool()
    loop = asyncio.get_event_loop()
    start = time.time()
    try:
        loop.run_until_complete(run_blocking_task(executor, loop, 10))
    finally:
        loop.close()
    print(f'\n Took: {time.time() - start}')


