import socket
import vim
import json

class LanguageServer:
	def __init__(self):
		sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		self.sockname = b"/tmp/lsp"
		self.sock = sock


	def request(self, keyword, filename, row, col):
		print(keyword, filename, row, col)
		data = {
			"key" : keyword,
			"name" : filename,
			"row" : row,
			"col" : col
		}
		request = json.dumps(data, separators=(',',':')).encode("ascii")
		self.sock.sendto(request, self.sockname)
		msg = self.recvfrom()
		print(msg)


def main():
	keyword = sys.argv[1]
	# 1,1 is top left
	col = vim.eval('line(".")')
	row = vim.eval('col(".")')
	buf = vim.current.buffer
	ls = LanguageServer()
	ls.request(keyword, buf.name, row, col)


if __name__ == "__main__":
	main()

