import socket
import vim
import json
import os

class LanguageServer:
	def __init__(self):
		if hasattr(socket, "AF_UNIX"):
			sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
			self.sockname = b"/tmp/lsp_client"
			self.servername = b"/tmp/lsp"
		else:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.sockname = ("127.0.0.1", 8701)
			self.servername = ("127.0.0.1", 8702)
		self.sock = sock
		self.sock.bind(self.sockname)


	def __del__(self):
		if not isinstance(self.sockname, tuple):
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
			self.sock.sendto(request, self.servername)
		except (FileNotFoundError, ConnectionRefusedError):
			print("Language Server not running")
			return
		self.sock.settimeout(2)
		try:
			msg = self.sock.recv(2048)
		except TimeoutError:
			print("Language Server not responding")
			return
		contents = json.loads(msg.decode('utf-8'))
#		print(contents)
		vim.command('edit {}'.format(contents[0]["name"]))
		vim.command('call cursor({},{})'.format(contents[0]["row"], contents[0]["col"]))


def main():
	keyword = sys.argv[1]
	# 1,1 is top left
	row = int(vim.eval('line(".")'))
	col = int(vim.eval('col(".")'))
	language = vim.eval('&filetype')
	buf = vim.current.buffer
	ls = LanguageServer()
	ls.request(language, keyword, buf.name, row, col)


if __name__ == "__main__":
	main()

