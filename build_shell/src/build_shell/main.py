#!/usr/bin/env python3


import subprocess
import os
import struct
import sys

from tkinter import *
from tkinter import font

WIDGET_PADDING = 3

class App:
	def __init__(self, parent):
		
		# Set the minimum width & height
		parent.minsize(600, 400)

		btn = Button(parent, text="Clean", command=self.clean)
		btn.grid(row=0, column=0)

		btn = Button(parent, text="Rebuild", command=self.build)
		btn.grid(row=0, column=1)

		btn = Button(parent, text="Exit", command=Exit)
		btn.grid(row=0, column=2)

		self.scrllOutput = Scrollbar(parent, orient=VERTICAL)
		self.scrllOutput.grid(row=2, column=3, sticky=N+S+W)

		self.lstOutput = Listbox(parent, font=('Terminus', 8), selectmode=SINGLE, yscrollcommand=self.scrllOutput.set, width=132, height=40)
		self.lstOutput.grid(row=2, column=0, columnspan=3, sticky=N+S+E+W)
		self.lstInfo = []

		self.scrllOutput.config(command=self.lstOutput.yview)

		parent.bind("<Up>", self.previous_error)
		self.lstOutput.bind("<Up>", self.previous_error)
		parent.bind("<Down>", self.next_error)
		self.lstOutput.bind("<Down>", self.next_error)

		self.lstOutput.bind("<<ListboxSelect>>", self.edit)

		self.status = Label(parent, text="")
		self.status.grid(row=1, column=0, columnspan=4, sticky=N+S+E+W)

		self.frame = parent
		parent.after_idle(self.launch)

	
	def Output(self, NewText):
		if NewText.startswith('[ninja '):
			self.status.config(text=NewText)
			return
		self.lstOutput.insert(END, NewText)
		if NewText.find("warning:") >= 0:
			self.warning_count += 1
			self.lstOutput.itemconfig(END, {'bg' : 'yellow'})
			self.lstInfo.append("W")
		elif NewText.find("error:") >= 0:
			self.error_count += 1
			self.lstOutput.itemconfig(END, {'bg' : 'red'})
			self.lstInfo.append("E")
		else:
			self.lstInfo.append(" ")
		self.lstOutput.see(END)


	def clearOutput(self):
		self.lstOutput.delete(0, END)
		self.warning_count = 0
		self.error_count = 0
		self.lstInfo = []


	def clean(self):
		self.kill()
		self.clearOutput()
		self.launch(extra=["clean"])


	def build(self):
		self.kill()
		self.clearOutput()
		self.launch()


	def launch(self, extra=[]):
		env = os.environ
		env["NINJA_STATUS"] = "[ninja %f/%t] "
#	args = ["meson", "compile", "-C", "build"]
		args = ["ninja", "-C", "build"]
		args += extra

		child = subprocess.Popen(args, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0) #pylint: disable = consider-using-with
		os.set_blocking(child.stdout.fileno(), False)

		self.child = child
		self.leftover_data = b""
		self.warning_count = 0;
		self.error_count = 0;
		self.frame.after(500, self.check)


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
					self.Output(line)
			else:
				break
		self.leftover_data = data


	def check(self):
		self.get_child_output()
		
		if self.child or len(self.leftover_data) > 0:
			self.frame.after(10, self.check)


	def kill(self):
		if self.child:
			self.child.kill()
			self.child = None

	def previous_error(self, event):
		lstOutput = self.lstOutput
		selection = lstOutput.curselection()
		if selection:
			index = selection[0]
		else:
			index = lstOutput.size()-1
		prev_index = index
		index -= 1
		while index >= 0:
			if self.lstInfo[index] != " ":
				break
			index -= 1
		else:
			index = prev_index
		print(index)
		lstOutput.select_clear(0, END)
		lstOutput.select_set(index)
		lstOutput.activate(index)
		return "break"

	def next_error(self, event):
		lstOutput = self.lstOutput
		selection = lstOutput.curselection()
		if selection:
			index = selection[0]
		else:
			index = 0
		max_index = lstOutput.size()
		prev_index = index
		index += 1
		while index < max_index:
			if self.lstInfo[index] != " ":
				break
			index += 1
		else:
			index = prev_index
		print(index)
		lstOutput.select_clear(0, END)
		lstOutput.select_set(index)
		lstOutput.activate(index)
		return "break"


	def edit(self, event):
		selection = event.widget.curselection()
		if selection:
			index = selection[0]
			data = event.widget.get(index)
			# Data format is file:line:column xxx
			parts = data.split(":")
			print(parts)

def Exit():
	root.destroy()
	sys.exit()


def main():
	global root

	root = Tk()
	for family in font.families():
		f = font.Font(family=family)
		if f.metrics("fixed"):
			print(family)
	root.protocol("WM_DELETE_WINDOW", Exit)
	root.title("build shell")

	app = App(root)

	root.mainloop()

