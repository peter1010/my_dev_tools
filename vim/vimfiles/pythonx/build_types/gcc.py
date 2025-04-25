# Build Code
import os
import subprocess
import re

class GCC:

	def __init__(self):
		self.enter_match = re.compile(r'Entering directory')
		self.leave_match = re.compile(r'Leaving directory')


	def can_build(self, dirname, ext):
		if ext in (".c", ".h", ".cpp", ".hpp"):
			files = [f.lower() for f in os.listdir(dirname)]
			if "makefile" in files:
				self.makefile_dir = dirname
				return True
		return False

	def run(self, action, output):
		args = ["make"]
		if action:
			args.append(action)
		print(args)
		proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		errorLines = []
		while True:
			line = proc.stdout.readline().decode("utf-8")
			if len(line) == 0:
				break
			output.write(line)

			if line.startswith("In file included from"):
				errorLines.append(line)
			else:
				idx = line.find("Entering directory")
				if idx >= 0:
					errorLines.append(line)
				else:
					idx = line.find("Leaving directory")
					if idx >= 0:
						errorLines.append(line)
					else:
						idx = line.find("warning:")
						if idx >= 0:
							errorLines.append(line)
			output.write(line)
		return errorLines



def get_plugin():
	return GCC()
