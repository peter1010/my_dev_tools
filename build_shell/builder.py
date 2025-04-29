

class Builder:
	def __init__(self, build_dir):
		self.build_dir = build_dir

	def get_output(self, gui):
		self.gui = gui
		return self.get_child_output()


	def get_child_output(self):
		if self.child:
			data = self.child.stdout.read()
			if data:
				data = self.leftover_data + data
			else:
				data = self.leftover_data
				exitcode = self.child.poll()
				if exitcode is not None:
					data += b'\n Child terminated\n'
					self.child = None
		else:
			data = self.leftover_data
			if len(data) > 0 and not data.endswith(b'\n'):
				data += b'\n'

		while True:
			idx = data.find(b'\n')
			if idx >= 0:
				line = data[:idx]
				data = data[idx+1:]

				line = line.decode("utf-8").rstrip()
				if len(line) > 0:
					self.send_output(line)
			else:
				break
		self.leftover_data = data
		return len(self.leftover_data) > 0 or self.child is not None


	def kill(self):
		if self.child:
			self.child.kill()
			self.child = None
