#!/usr/bin/env python3

from subprocess import Popen, PIPE
import json
import os
import socket
import argparse
from urllib.parse import urlparse

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
		request = {}
		request['jsonrpc'] = '2.0'
		request['method'] = method
		if params:
			request['params'] = params
	#    if Id is not None:
		self.Id += 1
		request['id'] = self.Id
	#        self._requests[Id] = r
		request = json.dumps(request, separators=(',',':'), sort_keys=True).encode("ascii")
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


	def send_goto_declaration(self, file_path, row, col):
		if not self.has_declarations:
			return self.send_goto_definition(file_path, row, col)
		uri = "file:///" + file_path
		params = {
			"textDocument" : {
				"uri" : uri
			},
			"position" : {
				"line" : row,
				"character" : col
			},
		}
		self.send_msg("textDocument/declaration", params)
		result = self.recv_msg()

	def send_goto_definition(self, file_path, row, col):
		uri = "file:///" + file_path
		params = {
			"textDocument" : {
				"uri" : uri
			},
			"position" : {
				"line" : row - 1,
				"character" : col - 1
			},
		}
		result, error = self.do_transaction("textDocument/definition", params)
		processed_result = []
		for entry in result:
			# print(result)
			name = urlparse(entry['uri']).path
			location = entry["range"]["start"]
			print(name, location)
			processed_result.append({"name" : name, "row" : location["line"] + 1, "col" : location["character"] + 1})
		return processed_result


	def send_goto_implementation(self, file_path, row, col):
		uri = "file:///" + file_path
		params = {
			"textDocument" : {
				"uri" : uri
			},
			"position" : {
				"line" : row - 1,
				"character" : col - 1
			},
		}
		result, error = self.do_transaction("textDocument/implementation", params)
		print(result, error)

	def send_find_references(self, file_path, row, col):
		uri = "file:///" + file_path
		params = {
			"textDocument" : {
				"uri" : uri
			},
			"position" : {
				"line" : row - 1,
				"character" : col - 1
			},
			"context" : {
				"includeDeclaration" : True
			}
		}
		result, error = self.do_transaction("textDocument/implementation", params)
		print(result, error)

	def send_hover(self, file_path, row, col):
		uri = "file:///" + file_path
		params = {
			"textDocument" : {
				"uri" : uri
			},
			"position" : {
				"line" : row - 1,
				"character" : col - 1
			},
			"context" : {
				"includeDeclaration" : True
			}
		}
		result, error = self.do_transaction("textDocument/hover", params)
		print(result, error)


def listen(ls):
	sockname = "/tmp/lsp"
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
	if os.path.exists(sockname):
		os.unlink(sockname)
	sock.bind(sockname)

	while True:
		msg, addr = sock.recvfrom(2048)
		print(addr)
		contents = json.loads(msg.decode("utf-8"))
		print(contents)
		func = getattr(ls, "send_" + contents["method"])
		result = func(**contents["args"])
		response = json.dumps(result).encode("utf-8")
		sock.sendto(response, addr)


def get_ls(language):
	language = language.upper()
	if language == "C":
		return ["clangd"]
	if language == "PY":
		return ["pylsp"]
	return None


def main():
	parser = argparse.ArgumentParser(
		prog='Language Server',
		description='Wrapper for a language server',
	)
	parser.add_argument('-l', '--language', help='Programing language', default='C')
	parser.add_argument('-s', '--source_dir', help='Directory where all source files can be found', default='.')

	args = parser.parse_args()

	executable = get_ls(args.language)
	source_dir = args.source_dir
	os.chdir(source_dir)

	if executable:
		ls = LanguageServer(executable)

	ls.send_initialize()
	listen(ls)

	ls.send_shutdown()
	input("Press Return to exit")

if __name__ == "__main__":
	main()
