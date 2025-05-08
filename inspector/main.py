#!/usr/bin/env python3

#
# TKtinter application that is a wrapper for GNU global
#

import os
import sys

import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

#import editor

class App:

	def __init__(self, parent):
		
		parent.protocol("WM_DELETE_WINDOW", self.on_quit)
		parent.title("Inspector")
		# Set the minimum width & height
#		parent.minsize(600, 400)
		root.option_add('*tearOff', False)

		menubar = self.create_menubar(parent)
		menubar.pack(side=tk.TOP, fill=tk.X)

		frame = self.create_panel(parent)
		frame.pack(fill=tk.BOTH, expand=True)

		self.status = tk.Label(parent, text="")
		self.status.pack(side=tk.BOTTOM, fill=tk.X)

		self.parent = parent
		parent.after_idle(self.launch)


	def create_panel(self, parent):
		frame = tk.Frame(parent)

		scroll_bar = tk.Scrollbar(frame, orient=tk.VERTICAL)
		scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

		fixed_font = font.nametofont("TkFixedFont")
		fixed_font.configure(size=10)
		code_view = tk.Listbox(frame, font=fixed_font, selectmode=tk.SINGLE, yscrollcommand=scroll_bar.set,
			height=30
		)

		code_view.pack(expand=True, fill="both", side=tk.LEFT)

		scroll_bar.config(command=code_view.yview)
		self.code_view = code_view
		return frame


	def create_menubar(self, parent):
		menubar = tk.Frame(parent, bd=1, relief=tk.RAISED)

		file_menu_btn = tk.Menubutton(menubar, text='File', underline=0)
		file_menu = tk.Menu(file_menu_btn)
		file_menu.add_command(label='Open File...', underline=0, accelerator="Ctrl+O", command=self.on_open)
		file_menu.add_command(label='Quit', underline=0, accelerator="Ctrl+Q", command=self.on_quit)
		file_menu_btn.config(menu=file_menu)
		file_menu_btn.pack(side=tk.LEFT)

		parent.bind('f', lambda evt: file_menu_btn.event_generate('<<Invoke>>'))
		parent.bind('<Control-q>', self.on_quit)
		parent.bind('<Control-o>', self.on_open)

		view_menu_btn = tk.Menubutton(menubar, text='View', underline=0)
		view_menu = tk.Menu(view_menu_btn)
		view_menu.add_command(label="Foward", underline=0)
		view_menu.add_command(label="Backwards", underline=0)
		view_menu.add_command(label="Edit", underline=0)
		view_menu_btn.config(menu=view_menu)
		view_menu_btn.pack(side=tk.LEFT)
		parent.bind('f', lambda evt: view_menu_btn.event_generate('<<Invoke>>'))
		parent.bind('b', lambda evt: view_menu_btn.event_generate('<<Invoke>>'))
		parent.bind('e', lambda evt: view_menu_btn.event_generate('<<Invoke>>'))

		helpmenu_btn = tk.Menubutton(menubar, text='Help', underline=0)
		menu_help = tk.Menu(helpmenu_btn, tearoff=False)
		menu_help.add_command(label='About', underline=0)
		helpmenu_btn.config(menu=menu_help)
		helpmenu_btn.pack(side=tk.LEFT)
		parent.bind('h', lambda evt: helpmenu_btn.event_generate('<<Invoke>>'))
		return menubar

	def on_clean(self):
		self.kill()
		self.clearOutput()
		self.launch(clean=True)

	def on_open(self, event=None):
		file_path = filedialog.askopenfilename()
		
		print(file_path)
		with open(file_path, "r") as in_fp:
			for line in in_fp:
				line = line.rstrip().expandtabs(4)
				print(line)
				self.code_view.insert(tk.END, line)

	def on_quit(self, event=None):
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


	def edit(self, event):
		lstOutput = self.lstOutput
		selection = lstOutput.curselection()
		print(selection)
		if selection and self.builder:
			index = selection[0]
			data = event.widget.get(index)
			filename, line_num = self.builder.get_location(data)
			editor.spawn(filename, line_num)


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

