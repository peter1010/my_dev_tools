import subprocess
import os

from builder import Builder as Base

class Builder(Base):
	def __init__(self, build_dir):
		super().__init__(build_dir)

	def __str__(self):
		return "-- GHS BUILDER --"

	def launch(self, clean):
		raise RuntimeError("TODO")

	def send_output(self, line):
		raise RuntimeError("TODO")

	def get_location(self, line):
		# "ParameterManager\GT8Common\CParMan.h", line 23: warning #64-D: declaration
		parts = line.split(",")
		if len(parts) < 2:
			return None, None
		subparts = parts[1].split(":")
		try:
			line_num = int(subparts[1].strip()[5:])
		except ValueError:
			return None, None
		filename = parts[0].strip()
		return filename, line_num
