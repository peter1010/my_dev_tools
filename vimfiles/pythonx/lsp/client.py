import socket
import vim
import json
import os

class LanguageServer:
	def __init__(self):
		sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		self.sockname = b"/tmp/lsp_client"
		self.servername = b"/tmp/lsp"
		self.sock = sock
		self.sock.bind(self.sockname)

	def __del__(self):
		os.unlink(self.sockname)

	def request(self, keyword, filename, row, col):
		print(keyword, filename, row, col)
		data = {
			"method" : keyword,
			"args" : {
				"file_path" : filename,
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
		print(contents)


def main():
	keyword = sys.argv[1]
	# 1,1 is top left
	row = int(vim.eval('line(".")'))
	col = int(vim.eval('col(".")'))
	buf = vim.current.buffer
	ls = LanguageServer()
	ls.request(keyword, buf.name, row, col)


if __name__ == "__main__":
	main()

