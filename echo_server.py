"""
Reference: http://hoad.io/blog/playing-with-asyncio/

"""
import asyncio

loop = asyncio.get_event_loop()

class EchoProtocol(asyncio.Protocol):
	def connection_made(self, transport):
		self.transport = transport
		print('connection made')

	def data_received(self, data):
		self.transport.write(b'your data: ' + data)

	def connection_lost(self, exc):
		server.close()


server = loop.run_until_complete(loop.create_server(EchoProtocol, '127.0.0.1', 4444))
loop.run_until_complete(server.wait_closed())