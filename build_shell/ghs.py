import subprocess
import os

from builder import Builder as Base

class Builder(Base):
	def __init__(self, build_dir):
		super().__init__(build_dir)

	def __str__(self):
		return "-- GHS BUILDER --"

	def find_ghs(self):
		ghs_dir = os.path.join("C:\\", "ghs")
		folders = os.listdir(ghs_dir)
		for folder in folders:
			folder_path = os.path.join(ghs_dir, folder)
			if os.path.isdir(folder_path):
				gbuild = os.path.join(folder_path, "gbuild.exe")
				if os.path.exists(gbuild):
					return gbuild
		return None

	def launch(self, clean):
		args = [self.find_ghs(), "-top", "default.gpj"]
		if clean:
			args.append("-clean")
		child = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
		os.set_blocking(child.stdout.fileno(), False)

		self.child = child
		self.leftover_data = b""


	def send_output(self, line):
		if line.find(": warning #") >= 0:
			self.gui.output_warning(line)
			return
		if line.startswith(": error #"):
			self.gui.output_error(line)
			return
		self.gui.output_text(line)


	def get_location(self, line):
		# "ParameterManager\GT8Common\CParMan.h", line 23: warning #64-D: declaration
		parts = line.split(",")
		if len(parts) < 2:
			print("No comma separator in %s" % line)
			return None, None
		subparts = parts[1].split(":")
		try:
			line_num = int(subparts[0].strip()[5:])
		except ValueError:
			print("%s contains invalid line number" % subparts[0])
			return None, None
		filename = parts[0][1:-1]
		return filename, line_num
