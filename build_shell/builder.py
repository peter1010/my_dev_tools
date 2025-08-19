import os

class Builder:


	def __init__(self, build_dir, source_dir=None):
		self.build_dir = build_dir
		if source_dir:
			self.source_dir = source_dir
		else:
			self.source_dir = build_dir


	def fixup_paths(self, filename):
		"""Update the filename to be relative to the source directory"""
		full_path = os.path.join(self.build_dir, filename)
		return os.path.relpath(full_path, self.source_dir)


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
				if (exitcode is not None) and (exitcode != 0):
					data += b'\n-- Build terminated (%i) --\n' % exitcode
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
