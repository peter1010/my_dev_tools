import subprocess
import os
import platform

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import config


def substitute(args, filename, line_num):
	table = (
		("{fname}", filename),
		("{line}", line_num)
	)
	new_args = []
	for arg in args:
		for name, value in table:
			idx = arg.find(name)
			if idx >= 0:
				arg = arg[:idx] + str(value) + arg[idx+len(name):]
		new_args.append(arg)
	return new_args


def spawn(filename, line_num, working_dir):
		execute, args =  config.get_configuration().get_editor_details()
		args = [execute] + substitute(args, filename, line_num)
		print(args)
		proc = subprocess.Popen(args, cwd=working_dir, start_new_session=True, close_fds=True)

#		try:
#			pid = os.fork()
#		except AttributeError:
#			import subprocess
#			# fork not supported so like a windows box.
#			DETACHED_PROCESS = 0x0008
#			CREATE_NEW_CONSOLE = 0x0010
#			script_name = __file__
#			if script_name.endswith(".pyc"):
#				script_name = script_name[:-1]
#			args = [sys.executable, script_name, "spawn"]
#		proc = subprocess.Popen(args, creationflags=CREATE_NEW_CONSOLE, close_fds=True)
#		time.sleep(1)

class ConfigDialog:

	def __init__(self, parent):
		dialog = tk.Toplevel(parent)
		dialog.title("Configure Editor")
		inform_wm_dialog(dialog)

		tk.Label(dialog, text="Path:").grid(row=0, column=0)
		self.path = tk.Entry(dialog)
		self.path.grid(row=0, column=1)
		tk.Button(dialog, text="Choose", command=self.on_choose).grid(row=0, column=2)

		tk.Label(dialog, text="Args:").grid(row=1, column=0)
		self.args = tk.Listbox(dialog, height=10)
		self.args.grid(row=1, column=1)

		path, args = config.get_configuration().get_editor_details()
		self.path.insert(tk.END, path)
		for arg in args:
			self.args.insert(tk.END, arg)

		ttk.Button(dialog, text="Ok", underline=0, command=self.on_ok).grid(row=3, column=0)

		cancel_btn = tk.Button(dialog, text="Cancel", underline=0, command=self.cancel)
		cancel_btn.grid(row=3, column=1)

		# Modal window.
		# Wait for visibility or grab_set doesn't seem to work.
		dialog.wait_visibility()
		dialog.grab_set()
		dialog.transient(parent)

		self.dialog = dialog
		self.args.bind("<Double-1>", self.on_click_edit_arg)
		self.args.bind("<Return>", self.on_key_edit_arg)

	def on_click_edit_arg(self, event):
		index = self.args.index(f"@{event.x},{event.y}")
		self.on_start_edit_arg(index)
		return "break"

	def on_key_edit_arg(self, event):
		index = self.args.curselection()
		self.on_start_edit_arg(index)
		return "break"

	def on_start_edit_arg(self, index):
		self.edit_arg_index = index
		text = self.args.get(index)
		y0 = self.args.bbox(index)[1]
		entry = tk.Entry(self.args, borderwidth=0, highlightthickness=1)
		entry.bind("<Return>", self.on_accept_edit_arg)
		entry.bind("<Escape>", self.on_cancel_edit_arg)

		entry.insert(0, text)
		entry.selection_from(0)
		entry.selection_to("end")
		entry.place(relx=0, y=y0, relwidth=1, width=-1)
		entry.focus_set()
		entry.wait_visibility()
		entry.grab_set()

	def on_cancel_edit_arg(self, event):
		event.widget.destroy()
		self.dialog.grab_set()

	def on_accept_edit_arg(self, event):
		new_data = event.widget.get()
		self.args.delete(self.edit_arg_index)
		self.args.insert(self.edit_arg_index, new_data)
		event.widget.destroy()

	def on_choose(self):
		#filedialog.FileDialog(self.dialog).go()
		filedialog.askopenfilename()


	def on_ok(self):
		editor_path = self.path.get()
		editor_args = self.args.get()
		if not os.path.exists(editor_path):
			messagebox.showerror(message="Invalid Path")
			return
		config.get_configuration().set_editor_details(editor_path, editor_args)
		self.dialog.grab_release()
		self.dialog.destroy()


	def cancel(self):
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


