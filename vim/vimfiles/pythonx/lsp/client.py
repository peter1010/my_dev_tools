import socket
import json
import os

try:
	import vim
except ImportError:
	import sys
	class vim:

		@staticmethod
		def eval(x):
			return 10

	sys.argv = ["","test"]


class LanguageServer:

	def __init__(self):
		if hasattr(socket, "AF_UNIX"):
			sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
			self.servername = b"/tmp/lsp"
			# AF_UNIX Datagram doesn't automatically create the client sockname
			self.sockname = b"/tmp/lsp_client"
			sock.bind(self.sockname)
		else:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.servername = ("127.0.0.1", 8702)
		sock.connect(self.servername)
		self.sock = sock


	def __del__(self):
		if hasattr(self, "sockname"):
			os.unlink(self.sockname)


	def request(self, language, keyword, filename, row, col):
#		print(language, keyword, filename, row, col)
		data = {
			"lng" : language,
			"mtd" : keyword,
			"arg" : {
				"pth" : filename,
				"row" : row,
				"col" : col
			}
		}
		request = json.dumps(data, separators=(',',':')).encode("utf-8")
		try:
			# print("Sending to {}".format(self.servername))
			self.sock.sendall(request)
		except (FileNotFoundError, ConnectionRefusedError):
			print("Language Server not running")
			return
		self.sock.settimeout(2)
		buffer = bytearray(2048)
		try:
			nbytes = self.sock.recv_into(buffer)
		except TimeoutError:
			print("Language Server not responding")
			return
		contents = json.loads(buffer[:nbytes].decode('utf-8'))
#		print(contents)
		vim.command('edit {}'.format(contents[0]["name"]))
		vim.command('call cursor({},{})'.format(contents[0]["row"], contents[0]["col"]))


def main():
	keyword = sys.argv[1]
	# 1,1 is top left
	row = int(vim.eval('line(".")'))
	col = int(vim.eval('col(".")'))
	language = vim.eval('&filetype')
	filename = vim.current.buffer.name
	ls = LanguageServer()
	ls.request(language, keyword, filename, row, col)


if __name__ == "__main__":
	main()

