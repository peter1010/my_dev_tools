#!/usr/bin/env python3

from subprocess import Popen, PIPE
import json
import os
import socket
import argparse

class LanguageServer:

    def __init__(self, lsp_server_path):
        args = [lsp_server_path]
        self.proc = Popen(args, stdin=PIPE, stdout=PIPE, bufsize=0);
        os.set_blocking(self.proc.stdout.fileno(), False)
        self.Id = 0
        self.prev_data = None

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
        print(msg)
        self.proc.stdin.write(msg)
        self.proc.stdin.flush()

        return msg

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
        self.send_msg("initialize", params)
        result = self.recv_msg()

    def send_shutdown(self):
        self.send_msg("shutdown", None)
        result = self.recv_msg()

    def send_exit(self):
        self.send_msg("exit", None)
        result = self.recv_msg()

    def send_goto_declaration(self, file_path, row, col):
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
                "line" : row,
                "character" : col
            },
        }
        self.send_msg("textDocument/definition", params)
        result = self.recv_msg()

    def send_goto_implementation(self, file_path, row, col):
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
        self.send_msg("textDocument/implementation", params)
        result = self.recv_msg()

    def send_find_references(self, file_path, row, col):
        uri = "file:///" + file_path
        params = {
            "textDocument" : {
                "uri" : uri
            },
            "position" : {
                "line" : row,
                "character" : col
            },
            "context" : {
                "includeDeclaration" : True
            }
        }
        self.send_msg("textDocument/implementation", params)
        result = self.recv_msg()

    def send_hover(self, file_path, row, col):
        uri = "file:///" + file_path
        params = {
            "textDocument" : {
                "uri" : uri
            },
            "position" : {
                "line" : row,
                "character" : col
            },
            "context" : {
                "includeDeclaration" : True
            }
        }
        self.send_msg("textDocument/hover", params)
        result = self.recv_msg()


def listen(ls):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.bind("/tmp/lsp")

    while True:
        msg, addr = sock.recvfrom(2048)

        contents = json.loads(msg.decode("utf-8"))
        print(contents)


def get_ls(language):
    language = language.upper()
    if language == "C":
        return "clangd"
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
