import sys
import tkinter as tk
import socket
import os
import time

class OutputWindow:

	def __init__(self):
		pass

	def open(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		for i in range(3):
			sock.connect(("127.0.0.1", 5000))
			sock.sendall('hello')
			try:
				data = sock.recv(1024)
			except socket.error:
				self.spawn()
				continue
			if data != "hello":
				self.spawn()
				continue
			break
		self.sock = sock

	def spawn(self):
		try:
			pid = os.fork()
		except AttributeError:
			import subprocess
			# fork not supported so like a windows box.
			DETACHED_PROCESS = 0x0008
			CREATE_NEW_CONSOLE = 0x0010
			script_name = __file__
			if script_name.endswith(".pyc"):
				script_name = script_name[:-1]
			args = [sys.executable, script_name, "spawn"]
			proc = subprocess.Popen(args, creationflags=CREATE_NEW_CONSOLE, close_fds=True)
		time.sleep(1)

	def run(self):
		print("Started")
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(("127.0.0.1", 5000))
		while True:
			data, addr = sock.recvfrom(1024)
			if data == "hello":
				sock.sendto(data, addr)
			else:
				data = data.rstrip()
				if len(data) > 0:
					print(data)

	def write(self, text):
		self.sock.sendall(text)

#        app = tk.root()

if __name__ == "__main__":
	app = OutputWindow()
	if len(sys.argv) > 1:
		if sys.argv[1] == "spawn":
			app.run()
		else:
			app.open()
