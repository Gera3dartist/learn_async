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
	datefmt="%H:%M:%S",
	stream=sys.stderr
)

logger = logging.getLogger('scraper')
logging.getLogger('chardet.charsetprober').disable = True

HREF_RE = re.compile(r'href="(.*?)"')


async def fetch_html(url: str, session: ClientSession, **kwargs):
	async with session.get(url, **kwargs) as resp:
		return await resp.text()


async def parse(url, session: ClientSession, **kwargs):
	"""
	Find href in html

	"""
	found = set()
	try:
		html = await fetch_html(url, session)
	except (
		aiohttp.ClientError,
		aiohttp.http_exceptions.HttpProcessingError,
	) as e:
		logger.exception(
			"client exception for %s [%s]: %s",
			url,
			getattr(e, 'status', None),
			getattr(e, 'message', None),
		)
		return found
	except Exception as e:
		logger.exception(
			'Non-client exception occured: %s', getattr(e, "__dict__", {})
		)
		return found
	else:
		for link in HREF_RE.findall(html):
			try:
				abslink = urllib.parse.urljoin(url, link)
			except (urllib.error.URLError, ValueError):
				logger.exception('Error parsing URL: %s', link)
				pass
			else:
				found.add(abslink)
		logger.info('Found %d links for %s', len(found), url)
		return found


async def write_one(file: IO, url: str, **kwargs) -> None:
	"""
	Write found hrefs in file

	"""
	res = await parse(url, **kwargs)
	if not res:
		return None
	async with aiofiles.open(file, "a") as f:
		for p in res:
			await f.write(f"{url}\t\t{p}\n")
		logger.info("wrote results for resource: URL: %s", url)


async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:
	"""
	Crawl and write concurrently to `file` for multiple `urls`

	"""
	async with ClientSession() as session:
		tasks = [
			write_one(file=file, url=url, session=session, **kwargs)
			for url in urls
		]
		await asyncio.gather(*tasks)


async def main():
	import pathlib
	import sys
	here = pathlib.Path(__file__).parent  # get cwd
	async with aiofiles.open(here.joinpath("urls.txt")) as infile:
		urls = set(map(str.strip, await infile.readlines()))

	outpath = here.joinpath('foundurls.txt')
	async with aiofiles.open(outpath, "w") as outfile:
		await outfile.write("source_url\tparsed_url\n")
	await bulk_crawl_and_write(outpath, urls)

if __name__ == '__main__':
	asyncio.run(main())
