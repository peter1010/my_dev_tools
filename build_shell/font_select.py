import subprocess
import os
import platform

import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk

import config


class ConfigFont:

	def __init__(self, parent):
		dialog = tk.Toplevel(parent)
		dialog.title("Configure Font")
		inform_wm_dialog(dialog)

		listbox = tk.Listbox(dialog, selectmode=tk.SINGLE, width=80)
		for family in font.families():
			f = font.Font(family=family)
			if f.actual("size") <= 32 and f.metrics("fixed"):
				listbox.insert('end', family)

		# Bind The Listbox
		listbox.bind('<<ListboxSelect>>', self.on_font_choice)
		listbox.grid(row=0, column=0, sticky=tk.W + tk.E)
		self.listbox = listbox

		spinbox = tk.Spinbox(dialog, from_=8, to=32, width=2, command=self.on_font_size)
		spinbox.grid(row=0, column=1, sticky=tk.W + tk.E)
		self.spinbox = spinbox

		self.font = font.Font(family="Helvetica", size=10)

		self.args = tk.Text(dialog, font=self.font, height=4, width=32)
		self.args.insert(tk.END, "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n")
		self.args.insert(tk.END, "abcdefghijklmnopqrstuvwxyz\n")
		self.args.insert(tk.END, "0123456789\n")
		self.args.insert(tk.END, "~`!@#$%^&*()_+-={}\\[]|;:'\"<>?,./\n")


		self.args.grid(row=1, column=0, rowspan=2)

		ttk.Button(dialog, text="Ok", underline=0, command=self.on_ok).grid(row=2, column=2)
		ttk.Button(dialog, text="Cancel", underline=0, command=self.on_cancel).grid(row=3, column=2)

		dialog.rowconfigure(1, weight=3)
		# Modal window.
		# Wait for visibility or grab_set doesn't seem to work.
		dialog.wait_visibility()
		dialog.grab_set()
		dialog.transient(parent)

		self.dialog = dialog


	def on_font_choice(self, event):
		self.font.config(family=self.listbox.get(self.listbox.curselection()))


	def on_font_size(self):
		self.font.config(size=self.spinbox.get())


	def on_ok(self):
		editor_path = self.path.get()
		editor_args = list(filter(lambda item: len(item) > 0, [x.strip() for x in self.args.get('1.0', tk.END).splitlines()]))

		if not os.path.exists(editor_path):
			messagebox.showerror(message="Invalid Path")
			return
		config.get_configuration().set_editor_details(editor_path, editor_args)
		self.dialog.grab_release()
		self.dialog.destroy()


	def on_cancel(self):
		self.dialog.grab_release()
		self.dialog.destroy()


def inform_wm_dialog(root):
	wm = root._windowingsystem
	if wm == "aqua":
		root.tk.call("::tk::unsupported::MacWindowStyle", "style", root, "moveableModal", "")
	elif wm == "x11":
		# Set _NET_WM_WINDOW_TYPE_DIALOG, Sway uses this to know to float the window
		root.wm_attributes('-type', 'dialog')
		# for py >= 3.13 this will work! root.wm_attributes(type="dialog")


