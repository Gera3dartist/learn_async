import requests
import time
from concurrent import futures




def timer(f):
    def inner(*args, **kwargs):
        print('starting')
        start = time.time()
        res = f(*args, **kwargs)
        print(f'Took: {time.time() - start}')
        return res
    return inner

@timer
def with_session():
    session = requests.Session()
    for _ in range(1000):
        session.get("https://jsonplaceholder.typicode.com/todos/1")


@timer
def with_session_optimized():
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=100,
        pool_maxsize=100)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session = requests.Session()
    for _ in range(1000):
        session.get("https://jsonplaceholder.typicode.com/todos/1")


@timer
def with_future():
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        future = [
            executor.submit(
                lambda: requests.get("https://jsonplaceholder.typicode.com/todos/1"))
            for _ in range(1000)
        ]

        for f in futures.as_completed(future):
            continue


def main():
    print('just with session')
    with_session()

    print('\nwith adapter')
    with_session_optimized()

    # print('\nwith futures')
    # with_future()




if __name__ == '__main__':
    main()
