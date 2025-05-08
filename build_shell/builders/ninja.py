import subprocess
import os

from builder import Builder as Base

class Builder(Base):
	def __init__(self, build_dir):
		super().__init__(build_dir)

	def __str__(self):
		return "-- NINJA BUILDER --"

	def launch(self, clean):

		env = os.environ
		env["NINJA_STATUS"] = "[ninja %f/%t] "
#	args = ["meson", "compile", "-C", "build"]
		args = ["ninja", "-C", self.build_dir]
		if clean:
			args += ["clean"]

		child = subprocess.Popen(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
		os.set_blocking(child.stdout.fileno(), False)

		self.child = child
		self.leftover_data = b""

	def send_output(self, line):
		if line.startswith('[ninja '):
			self.gui.output_status(line)
			return
		if line.find("warning:") >= 0:
			self.gui.output_warning(line)
			return
		if line.find("error:") >= 0:
			self.gui.output_error(line)
			return
		self.gui.output_text(line)

	def get_location(self, line):
		parts = line.split(":")
		if len(parts) < 2:
			return None, None, None
		try:
			line_num = int(parts[1])
		except ValueError:
			return None, None, None
		filename = parts[0].strip()
		return filename, line_num, self.build_dir
