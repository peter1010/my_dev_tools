#!/usr/bin/env python3

from subprocess import Popen, PIPE
import json
import os
import socket
import argparse
from urllib.parse import urlparse


def add_position(row, col):
	return {
		"line" : row - 1,
		"character" : col - 1
	}


def add_uri(file_path):
	return {
		"uri" : "file:" + file_path
	}


def get_file_path(uri):
	name = urlparse(uri).path
	if name.startswith('/c:'):
		return name[1:]
	return name


class LanguageServer:

	def __init__(self, lsp_server_args):
		self.proc = Popen(lsp_server_args, stdin=PIPE, stdout=PIPE, bufsize=0)
		os.set_blocking(self.proc.stdout.fileno(), False)
		self.Id = 0
		self.prev_data = None


	def do_transaction(self, method, params=None):
		self.send_msg(method, params)
		msg = self.recv_msg()
		assert msg['jsonrpc'] == '2.0'
		assert msg['id'] == self.Id
		if 'error' in msg:
			error = msg['error']
		else:
			error = None
		if 'result' in msg:
			result = msg['result']
		else:
			result = None
		return (result, error)


	def send_msg(self, method, params=None):
		self.Id += 1
		request = {
			'jsonrpc': '2.0',
			'method': method,
			'id': self.Id
		}
		if params:
			request['params'] = params

		request = json.dumps(request, separators=(',',':'), sort_keys=True).encode("utf-8")
		headers = b'Content-Length: %d\r\n\r\n' % len(request)
		msg = headers + request
		self.proc.stdin.write(msg)
		self.proc.stdin.flush()


	def recv_msg(self):
		# Read the header, must be at least 
		# Content-length: 0 \r\n
		prev_data = self.prev_data
		while 1:
			new_data = self.proc.stdout.read()
			if new_data is None:
				continue
			if prev_data is not None:
				new_data = prev_data + new_data
			idx = new_data.find(b'\r\n\r\n')
			if idx < 0:
				prev_data = new_data
				continue
			headers = new_data[:idx]
			contents = new_data[idx+4:]
			break

		headers = headers.splitlines()
		for header in headers:
			if header.startswith(b'Content-Length:'):
				content_size = int(header[16:])
				break
		while len(contents) < content_size:
			new_data = self.proc.stdout.read(content_size - len(contents))
			if new_data is None:
				continue
			contents += new_data
		if len(contents) > content_size:
			self.prev_data = contents[content_size:]
			contents = contents[:content_size]
		else:
			self.prev_data = None
		contents = json.loads(contents.decode("utf-8"))
		return contents


	def send_initialize(self):
		params = {
			"processId" : os.getpid(),
			"capabilities" : {
				"textDocument" : {
					"hover" : {
						"currentFormat" : [
							"plaintext"
						]
					}
				}
			}
		}
		result, error = self.do_transaction("initialize", params)
		info = result["serverInfo"]
		print("Language Server => {} {}".format(info.get("name",""), info.get("version","")))
		capabilities = result["capabilities"]
		self.has_declarations = capabilities.get("declarationProvider", False)
		#print(result)
		#print(capabilities)


	def send_shutdown(self):
		self.send_msg("shutdown", None)
		result = self.recv_msg()


	def send_exit(self):
		self.send_msg("exit", None)
		result = self.recv_msg()


	def req_ping(self):
		return "pong"


	def req_find_declaration(self, pth, row, col):
		if not self.has_declarations:
			return self.req_find_definition(pth, row, col)
		params = {
			"textDocument" : add_uri(pth),
			"position" : add_position(row, col),
		}
		print(params)
		self.send_msg("textDocument/declaration", params)
		result = self.recv_msg()


	def req_find_definition(self, pth, row, col):
		params = {
			"textDocument" : add_uri(pth),
			"position" : add_position(row, col),
		}
		result, error = self.do_transaction("textDocument/definition", params)
		processed_result = []
		for entry in result:
			# print(result)
			name = get_file_path(entry['uri'])
			location = entry["range"]["start"]
			print(name, location)
			processed_result.append({"name" : name, "row" : location["line"] + 1, "col" : location["character"] + 1})
		return processed_result


	def req_find_implementation(self, pth, row, col):
		params = {
			"textDocument" : add_uri(pth),
			"position" : add_position(row, col),
		}
		result, error = self.do_transaction("textDocument/implementation", params)
		print(result, error)


	def req_find_references(self, pth, row, col):
		params = {
			"textDocument" : add_uri(pth),
			"position" : add_position(row, col),
			"context" : {
				"includeDeclaration" : True
			}
		}
		result, error = self.do_transaction("textDocument/implementation", params)
		print(result, error)


	def req_hover(self, pth, row, col):
		params = {
			"textDocument" : add_uri(pth),
			"position" : add_position(row, col),
			"context" : {
				"includeDeclaration" : True
			}
		}
		result, error = self.do_transaction("textDocument/hover", params)
		result = result["contents"]
		print("debug:", result, error)
		if not isinstance(result, str):
			kind = result["kind"]
			value = result["value"]


class ProxyServer:

	def __init__(self):
		self.languages = {}
#		if hasattr(socket, "AF_UNIX"):
		if False:
			print("Selecting AF_UNIX socket")
			sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
			self.sockname = "/tmp/lsp"
			if os.path.exists(self.sockname):
				os.unlink(self.sockname)
		else:
			print("Selecting AF_INET socket")
			#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sockname = ("127.0.0.1", 8702)
		print("Binding to {}".format(self.sockname))
		sock.bind(self.sockname)
		sock.listen(1)
		self.sock = sock


	def run(self):
		buffer = bytearray(2048)
		while True:
			print("Wait for incomming connection")
			(conn, addr) = self.sock.accept()
			while True:
				print(addr)
				print("Wait for incomming msg")
				nbytes = conn.recv_into(buffer)
				if nbytes == 0:
					break
				contents = json.loads(buffer[:nbytes].decode("utf-8"))
				print(contents)
				_id, contents = contents
				ls = self.get_ls(contents["lng"])
				if ls:
					func = getattr(ls, "req_" + contents["mtd"])
					response = func(**contents["arg"])
				else:
					response = None
				if response == None:
					result = [_id, ["Err"]]
				else:
					result = [_id, ["Ok", response]]
				print(result)
				response = json.dumps(result).encode("utf-8")
				print(response)
				conn.send(response)


	def get_ls(self, language):
		language = language.upper()
		ls = self.languages.get(language, None)
		if not ls:
			if language == "C":
				executable = ["clangd"]
			elif language == "PYTHON":
				executable = ["pylsp"]
			else:
				executable = None
			if executable:
				ls = LanguageServer(executable)
				ls.send_initialize()
				self.languages[language] = ls
		return ls


	def close(self):
		ls.send_shutdown()


def main():
	parser = argparse.ArgumentParser(
		prog='Language Server',
		description='Wrapper for a language server',
	)
	parser.add_argument('-s', '--source_dir', help='Directory where all source files can be found', default='.')

	args = parser.parse_args()

	source_dir = args.source_dir
	os.chdir(source_dir)

	proxy = ProxyServer()
	proxy.run()
	proxy.close()
	input("Press Return to exit")


if __name__ == "__main__":
	main()
