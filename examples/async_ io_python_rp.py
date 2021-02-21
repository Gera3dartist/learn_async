"""
https://realpython.com/async-io-python/#a-full-program-asynchronous-requests

"""
import asyncio
import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse

import aiofiles
import aiohttp
from aiohttp import ClientSession

logging.basicConfig(
	format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
	level=logging.DEBUG,
	datefmt="%H:%M:%S"
	stream=sys.stderr,
)