#!/usr/bin/env python3

#
# TKtinter application that creates a shell to capture build output, it parses the output for warnings (which are shown in yellow)
# and errors (which are shown oin red)
# Clicking on the error opens vim
# The app tries to find either a cargo, ninja, makefile or greenhills build file in the current directory or sub directories and
# if found runs that build and captures the output.
#

import os
import sys

import tkinter as tk
from tkinter import font
from tkinter import messagebox

import editor

WIDGET_PADDING = 3

class App:

	# Update if necessary with any new build types...
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
		if "default.gpj" in files:
			import ghs
			return  ghs.Builder(root_dir)
		for f in files:
			new_root = os.path.join(root_dir, f)
			if os.path.isdir(new_root):
				builder = self.find_build_type(new_root)
				if builder:
					return builder
		return None


	def __init__(self, parent):
		
		parent.protocol("WM_DELETE_WINDOW", self.on_quit)
		parent.title("build shell")
		# Set the minimum width & height
		parent.minsize(600, 400)
		root.option_add('*tearOff', False)

		self.create_menubar(parent)

		btn = tk.Button(parent, text="Clean", command=self.on_clean)
		btn.grid(row=0, column=0)

		btn = tk.Button(parent, text="Rebuild", command=self.on_build)
		btn.grid(row=0, column=1)

		btn = tk.Button(parent, text="Stop", command=self.on_stop)
		btn.grid(row=0, column=2)

		btn = tk.Button(parent, text="Exit", command=self.on_quit)
		btn.grid(row=0, column=3)

		self.scrllOutput = tk.Scrollbar(parent, orient=tk.VERTICAL)
		self.scrllOutput.grid(row=2, column=4, sticky=tk.N+tk.S+tk.W)

		self.lstOutput = tk.Listbox(parent, font=('Terminus', 8), selectmode=tk.SINGLE, yscrollcommand=self.scrllOutput.set, width=132, height=40)
		self.lstOutput.grid(row=2, column=0, columnspan=4, sticky=tk.N+tk.S+tk.E+tk.W)
		self.lstInfo = []

		self.scrllOutput.config(command=self.lstOutput.yview)

		parent.bind("<Up>", self.previous_error)
		self.lstOutput.bind("<Up>", self.previous_error)
		parent.bind("<Down>", self.next_error)
		self.lstOutput.bind("<Down>", self.next_error)
		self.lstOutput.bind("<Return>", self.edit)

		self.lstOutput.bind("<<ListboxSelect>>", self.edit)

		self.status = tk.Label(parent, text="")
		self.status.grid(row=1, column=0, columnspan=4, sticky=tk.N+tk.S+tk.E+tk.W)

		self.parent = parent
		parent.after_idle(self.launch)

	def create_menubar(self, parent):
#        menubar = tk.Frame(parent, bd=1, relief=tk.RAISED)
#		menubar.grid(row=0, column=0)		
#        file_btn = tk.Menubutton(menubar, text='File')

#        menu_file = tk.Menu(file_btn, tearoff=False)
#        menu_file.add_command(label='save', command=lambda: log('save'))
#        menu_file.add_command(label='open', command=lambda: log('open'))
#        file_btn.config(menu=menu_file)
#        file_btn.pack(side=tk.LEFT)
#        master.bind('f', lambda e: file_btn.event_generate('<<Invoke>>'))

#        edit_btn = tk.Menubutton(self, text='Edit')
#        menu_edit = tk.Menu(edit_btn, tearoff=False)
#        menu_edit.add_command(label='add', command=lambda: log('add'))
#        menu_edit.add_command(label='remove', command=lambda: log('remove'))
#        edit_btn.config(menu=menu_edit)
#        edit_btn.pack(side=tk.LEFT)
#        master.bind('e', lambda e: edit_btn.event_generate('<<Invoke>>'))

		menubar = tk.Menu(parent)
		root['menu'] = menubar
		self.menubar = menubar

		filemenu = tk.Menu(menubar)
		# filemenu.add_command(label="Open folder", command=self.on_open)
		filemenu.add_command(label="Quit", underline=0, command=self.on_quit)
		menubar.add_cascade(menu=filemenu, label="File", underline=0)
		self.filemenu = filemenu

		debugmenu = tk.Menu(menubar)
		debugmenu.add_command(label="Build", underline=0, command=self.on_build)
		debugmenu.add_command(label="Clean", underline=0, command=self.on_clean)
		debugmenu.add_command(label="Stop", underline=0, command=self.on_stop)
		menubar.add_cascade(menu=debugmenu, label="Build")

		parent.bind('<Key-f>', self.open_filemenu)
		#toolsmenu = tk.Menu(menubar)
		#toolsmenu.add_command(label="GDB Config", command=self.on_gdb)
		#menubar.add_cascade(menu=toolsmenu, label="Tools")
	
	def open_filemenu(self, event):
		self.menubar.postcascade(0)

	def output_warning(self, NewText):
		self.lstOutput.insert(tk.END, NewText)
		self.warning_count += 1
		self.lstOutput.itemconfig(END, {'bg' : 'yellow'})
		self.lstInfo.append("W")
		self.lstOutput.see(tk.END)


	def output_error(self, NewText):
		self.lstOutput.insert(tk.END, NewText)
		self.error_count += 1
		self.lstOutput.itemconfig(tk.END, {'bg' : 'red'})
		self.lstInfo.append("E")
		self.lstOutput.see(tk.END)


	def output_status(self, NewText):
		self.status.config(text=NewText)


	def output_text(self, NewText):
		self.lstOutput.insert(tk.END, NewText)
		self.lstInfo.append(" ")
		self.lstOutput.see(tk.END)


	def clearOutput(self):
		self.lstOutput.delete(0, tk.END)
		self.warning_count = 0
		self.error_count = 0
		self.lstInfo = []


	def on_clean(self):
		self.kill()
		self.clearOutput()
		self.launch(clean=True)


	def on_build(self):
		self.kill()
		self.clearOutput()
		self.launch()

	def on_stop(self):
		if self.builder:
			self.builder.kill()

	def on_quit(self):
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			self.parent.destroy()

	def launch(self, clean=False):
		builder = self.find_build_type()
		
		if builder:
			self.output_text(str(builder))
			builder.launch(clean)
			self.builder = builder
			self.warning_count = 0;
			self.error_count = 0;
			self.parent.after(500, self.check)
		else:
			self.builder = None
			self.output_text("-- NO BUILDER FOUND --")

	def check(self):
		if self.builder:
			more = self.builder.get_output(self)
		else:
			more = false
		if more:
			self.parent.after(10, self.check)


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
		lstOutput.select_clear(0, tk.END)
		lstOutput.select_set(index)
		lstOutput.activate(index)
		self.lstOutput.see(index)
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
		lstOutput.select_clear(0, tk.END)
		lstOutput.select_set(index)
		lstOutput.activate(index)
		self.lstOutput.see(index)
		return "break"


	def edit(self, event):
		lstOutput = self.lstOutput
		selection = lstOutput.curselection()
		print(selection)
		if selection and self.builder:
			index = selection[0]
			data = event.widget.get(index)
			filename, line_num = self.builder.get_location(data)
			editor.spawn(filename, line_num)

def Exit():
	root.destroy()
	sys.exit()


def main():
	global root

	root = tk.Tk()
	for family in font.families():
		f = font.Font(family=family)
		if f.metrics("fixed"):
			print(family)

	app = App(root)

	root.mainloop()

