# Build Code
import os
import subprocess
import re

class GHS:

	def __init__(self):
		# "ParameterManager\GT8Common\CParMan.h", line 23: warning #64-D: declaration
		self.warn_match = re.compile(r'^"([^"]+)",\s*line\s*(\d+):\s*(warning|error|fatal error)\s*#([^:]+):(.*)$')
		self.col_match = re.compile(r'^(\s+)\^$')


	def can_build(self, dirname, ext):
		if ext in (".c", ".h", ".cpp", ".hpp"):
			build_file = os.path.join(dirname, "default.gpj")
			if os.path.exists(build_file):
				self.root = dirname
				self.build_file = build_file
				return True
		return False

	def find_ghs(self):
		return os.path.join("C:\\", "ghs", "mips524", "gbuild.exe");

	def run(self, action, output):
		args = [self.find_ghs()]
		if action:
			args.append("-" + action)
		args += ["-top", self.build_file]
		proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		errorLines = []
		err_comment = None
		while True:
			line = proc.stdout.readline().decode("utf-8")
			if len(line) == 0:
				break
			line = line.rstrip()
			if len(line) == 0:
				continue

			output.write(line)
			result = self.warn_match.match(line)
			if result:
				err_filename = os.path.join(self.root, result.group(1))
				err_line_num = result.group(2)
				err_type = {
					"warning" : "W",
					"fatal error" : "E",
					"error" : "E" }[result.group(3)] # warning or fatal error
				err_code = result.group(4)
				err_comment = result.group(5)
			elif err_comment is not None:
				result = self.col_match.match(line)
				if result:
					err_col = len(result.group(1)) -1
					errorLine = '"%s", line %s:%s %s: %s %s' % (err_filename, err_line_num, err_col, err_type, err_code, err_comment)
					if errorLine not in errorLines:
						errorLines.append(errorLine)
				elif line.startswith('   '):
					err_comment += ' ' + line[1:].strip()
		return errorLines

def get_plugin():
	return GHS()
