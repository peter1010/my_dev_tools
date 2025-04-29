import subprocess
import os

from builder import Builder as Base

class Builder(Base):
	def __init__(self, build_dir):
		super().__init__(build_dir)

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
			self.gui.output_status(NewText)
			return
		if NewText.find("warning:") >= 0:
			self.gui.output_warning(NewText)
			return
		if NewText.find("error:") >= 0:
			self.gui.output_error(NewText)
			return
		self.gui.output_text(NewText)

