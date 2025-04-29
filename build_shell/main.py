#!/usr/bin/env python3

import os
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
		self.lstOutput.bind("<Return>", self.edit)

		self.lstOutput.bind("<<ListboxSelect>>", self.edit)

		self.status = Label(parent, text="")
		self.status.grid(row=1, column=0, columnspan=4, sticky=N+S+E+W)

		self.frame = parent
		parent.after_idle(self.launch)


	def output_warning(self, NewText):
		self.lstOutput.insert(END, NewText)
		self.warning_count += 1
		self.lstOutput.itemconfig(END, {'bg' : 'yellow'})
		self.lstInfo.append("W")
		self.lstOutput.see(END)


	def output_error(self, NewText):
		self.lstOutput.insert(END, NewText)
		self.error_count += 1
		self.lstOutput.itemconfig(END, {'bg' : 'red'})
		self.lstInfo.append("E")
		self.lstOutput.see(END)


	def output_status(self, NewText):
		self.status.config(text=NewText)


	def output_text(self, NewText):
		self.lstOutput.insert(END, NewText)
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
		self.launch(clean=True)


	def build(self):
		self.kill()
		self.clearOutput()
		self.launch()


	def find_build_type(self, root_dir=None):
		if root_dir is None:
			root_dir = os.getcwd()
		files = os.listdir(root_dir)
		if "Cargo.toml" in files:
			import cargo
			return cargo.Builder(root_dir)
		if "build.ninja" in files:
			import ninja
			return ninja.Builder(root_dir)
		if "makefile" in files:
			import make
			return  make.Builder(root_dir)
		for f in files:
			new_root = os.path.join(root_dir, f)
			if os.is_dir(new_root):
				return self.find_build_type(new_root)
		return None


	def launch(self, clean=False):
		builder = self.find_build_type()
		
		if builder:
			builder.launch(clean)
			self.builder = builder
			self.warning_count = 0;
			self.error_count = 0;
			self.frame.after(500, self.check)


	def check(self):
		if self.builder:
			more = self.builder.get_output(self)
		if more:
			self.frame.after(10, self.check)


	def kill(self):
		if self.builder:
			self.builder.kill()
			self.builder = None


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
		lstOutput.select_clear(0, END)
		lstOutput.select_set(index)
		lstOutput.activate(index)
		return "break"


	def edit(self, event):
		selection = event.widget.curselection()
		if selection:
			index = selection[0]
			data = event.widget.get(index)
			filename, line_num = self.builder.get_location(data)
			print(filename, line_num)

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

