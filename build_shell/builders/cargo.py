import subprocess
import os

from builder import Builder as Base

class Builder(Base):
	def __init__(self, build_dir):
		super().__init__(build_dir)
		self.prev_line = ""

	def __str__(self):
		return "-- CARGO BUILDER --"

	def launch(self, clean):
		os.chdir(self.build_dir)
		args = ["cargo"]
		if clean:
			args += ["clean"]
		else:
			args += ["build"]

		child = subprocess.Popen(args, cwd=self.build_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
		os.set_blocking(child.stdout.fileno(), False)

		self.child = child
		self.leftover_data = b""


	def send_output(self, line):
		if line.find("-->") < 0:
			self.gui.output_text(line)
		elif self.prev_line.startswith("warning:"):
			self.gui.output_warning(line)
		elif self.prev_line.startswith("error:"):
			self.gui.output_error(line)
		else:
			self.gui.output_text(line)
		self.prev_line = line

	def get_location(self, line):
		parts = line.split(":")
		if len(parts) < 2:
			return None, None, None
		try:
			line_num = int(parts[1])
		except ValueError:
			return None, None, None
		filename = parts[0].strip()[3:]
		return filename, line_num, self.build_dir
