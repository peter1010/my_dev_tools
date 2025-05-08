#!/usr/bin/env python3

#
# TKinter application that creates a shell to capture build output, it parses the output for warnings (which are shown in yellow)
# and errors (which are shown in red)
# Clicking on the error opens vim
# The app tries to find either a cargo, ninja, makefile or greenhills build file in the current directory or sub directories and
# if found runs that build and captures the output.
#

import os
import sys

import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

import editor

class App:

	# Update if necessary with any new build types...
	def find_build_type(self, root_dir=None):
		if root_dir is None:
			root_dir = os.getcwd()
		self.parent.title("Build Shell for %s" % root_dir)
		files = os.listdir(root_dir)
		if "Cargo.toml" in files:
			import builders.cargo as cargo
			return cargo.Builder(root_dir)
		if "build.ninja" in files:
			import builders.ninja as ninja
			return ninja.Builder(root_dir)
		if "makefile" in files:
			import builders.make as make
			return  make.Builder(root_dir)
		if "default.gpj" in files:
			import builders.ghs as ghs
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
#		parent.minsize(600, 400)
		root.option_add('*tearOff', False)

		self.create_menubar(parent).pack(fill=tk.BOTH)

		self.create_panel(parent).pack(fill=tk.BOTH, expand=True)

		self.status = tk.Label(parent, text="")
		self.status.pack(side=tk.BOTTOM, fill=tk.X)

		self.parent = parent
		self.builder = None
		parent.after_idle(self.launch)


	def create_panel(self, parent):
		frame = tk.Frame(parent)

		scroll_bar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
		scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

		fixed_font = font.nametofont("TkFixedFont")
		fixed_font.configure(size=10)
		self.output_pane = tk.Listbox(frame, font=fixed_font, selectmode=tk.SINGLE, yscrollcommand=scroll_bar.set,
			height=30, width=132
		)

		self.output_pane.pack(expand=True, fill="both", side=tk.LEFT)
		self.output_info = []

		scroll_bar.config(command=self.output_pane.yview)

		parent.bind("<Up>", self.on_previous_error)
		self.output_pane.bind("<Up>", self.on_previous_error)
		parent.bind("<Down>", self.on_next_error)
		self.output_pane.bind("<Down>", self.on_next_error)
		self.output_pane.bind("<Return>", self.on_edit)

		self.output_pane.bind("<<ListboxSelect>>", self.on_edit)
		return frame


	def create_menubar(self, parent):
		menubar = tk.Frame(parent, bd=1, relief=tk.RAISED)

		file_menu_btn = tk.Menubutton(menubar, text='File', underline=0)
		file_menu = tk.Menu(file_menu_btn)
		file_menu.add_command(label='Browse for build..', underline=0, command=self.on_build_browse)
		file_menu.add_command(label='Quit', underline=0, accelerator="Ctrl+Q", command=self.on_quit)
		file_menu_btn.config(menu=file_menu)
		file_menu_btn.pack(side=tk.LEFT)
		parent.bind('f', lambda evt: file_menu_btn.event_generate('<<Invoke>>'))
		parent.bind('<Control-q>', self.on_quit)

		build_menu_btn = tk.Menubutton(menubar, text='Build', underline=0)
		build_menu = tk.Menu(build_menu_btn)
		build_menu.add_command(label="Build", underline=0, accelerator="Ctrl+B", command=self.on_build)
		build_menu.add_command(label="Clean", underline=0, accelerator="Ctrl+L", command=self.on_clean)
		build_menu.add_command(label="Stop", underline=0, accelerator="Ctrl+S", command=self.on_stop)
		build_menu_btn.config(menu=build_menu)
		build_menu_btn.pack(side=tk.LEFT)
		parent.bind('b', lambda evt: build_menu_btn.event_generate('<<Invoke>>'))
		parent.bind('<Control-b>', self.on_build)
		parent.bind('<Control-l>', self.on_clean)
		parent.bind('<Control-s>', self.on_stop)

		tool_menu_btn = tk.Menubutton(menubar, text='Tools', underline=0)
		tool_menu = tk.Menu(tool_menu_btn)
		tool_menu.add_command(label="Editor...", underline=0, command=self.on_editor)
		tool_menu_btn.config(menu=tool_menu)
		tool_menu_btn.pack(side=tk.LEFT)
		parent.bind('t', lambda evt: tool_menu_btn.event_generate('<<Invoke>>'))
	
		help_menu_btn = tk.Menubutton(menubar, text='Help', underline=0)
		help_menu = tk.Menu(help_menu_btn)
		help_menu.add_command(label='About', underline=0, command=self.on_about)
		help_menu_btn.config(menu=help_menu)
		help_menu_btn.pack(side=tk.LEFT)
		parent.bind('h', lambda evt: help_menu_btn.event_generate('<<Invoke>>'))
		return menubar


	def output_warning(self, NewText):
		self.output_pane.insert(tk.END, NewText)
		self.warning_count += 1
		self.output_pane.itemconfig(tk.END, {'bg' : 'yellow'})
		self.output_info.append("W")
		self.output_pane.see(tk.END)


	def output_error(self, NewText):
		self.output_pane.insert(tk.END, NewText)
		self.error_count += 1
		self.output_pane.itemconfig(tk.END, {'bg' : 'red'})
		self.output_info.append("E")
		self.output_pane.see(tk.END)


	def output_status(self, NewText):
		self.status.config(text=NewText)


	def output_text(self, NewText):
		self.output_pane.insert(tk.END, NewText)
		self.output_info.append(" ")
		self.output_pane.see(tk.END)


	def clr_output_pane(self):
		self.output_pane.delete(0, tk.END)
		self.warning_count = 0
		self.error_count = 0
		self.output_info = []


	def on_clean(self, event=None):
		self.kill_builder()
		self.clr_output_pane()
		self.launch(clean=True)


	def on_build(self, event=None):
		self.kill_builder()
		self.clr_output_pane()
		self.launch()


	def on_about(self, event=None):
		text = (
			"Application to launch and capture the build output from ninja, cargo, make or ghs.",
			"When launched the tool will look for build.ninja, cargo.toml, makefile or default.gpj in the current and subdirectories.",
			"If found, a search for a matching executable in the standard install locations to execute.",
			"The output is capture in the output pane"
		)
		messagebox.showinfo("About", "\n\n".join(text))


	def on_build_browse(self, event=None):
		root_dir = filedialog.askdirectory()
		self.kill_builder()
		self.clr_output_pane()
		self.builder = None
		self.launch(root_dir=root_dir)

	def on_stop(self, event=None):
		self.kill_builder()


	def on_quit(self, event=None):
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			self.parent.destroy()


	def launch(self, clean=False, root_dir=None):
		if not self.builder:
			self.builder = self.find_build_type(root_dir)
		
		if self.builder:
			self.output_text(str(self.builder))
			self.builder.launch(clean)
			self.warning_count = 0;
			self.error_count = 0;
			self.parent.after(500, self.check_builder)
		else:
			self.output_text("-- NO BUILDER FOUND --")


	def check_builder(self):
		if self.builder:
			more = self.builder.get_output(self)
		else:
			more = False
		if more:
			self.parent.after(10, self.check_builder)


	def kill_builder(self):
		if self.builder:
			self.builder.kill()


	def on_previous_error(self, event):
		output_pane = self.output_pane
		selection = output_pane.curselection()
		if selection:
			index = selection[0]
		else:
			index = output_pane.size()-1
		prev_index = index
		index -= 1
		while index >= 0:
			if self.output_info[index] != " ":
				break
			index -= 1
		else:
			index = prev_index
		output_pane.select_clear(0, tk.END)
		output_pane.select_set(index)
		output_pane.activate(index)
		output_pane.see(index)
		return "break"


	def on_next_error(self, event):
		output_pane = self.output_pane
		selection = output_pane.curselection()
		if selection:
			index = selection[0]
		else:
			index = 0
		max_index = output_pane.size()
		prev_index = index
		index += 1
		while index < max_index:
			if self.output_info[index] != " ":
				break
			index += 1
		else:
			index = prev_index
		output_pane.select_clear(0, tk.END)
		output_pane.select_set(index)
		output_pane.activate(index)
		output_pane.see(index)
		return "break"


	def on_edit(self, event):
		selection = self.output_pane.curselection()
		if selection and self.builder:
			index = selection[0]
			data = event.widget.get(index)
			filename, line_num, working_dir = self.builder.get_location(data)
			if filename and line_num and working_dir:
				editor.spawn(filename, line_num, working_dir)


	def on_editor(self, event=None):
		editor.ConfigDialog(self.parent)


def main():
	global root

	root = tk.Tk()

#	family = font.Font(font='TkFixedFont')["family"]

#	print(family)
#	return

#	print(font.names())
	for family in font.families():
		f = font.Font(family=family)
		if f.metrics("fixed"):
			print(family, f.measure("Help"))

	app = App(root)
	root.mainloop()

