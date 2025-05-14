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

		ttk.Label(dialog, text="Path:").grid(row=0, column=0)
		self.path = tk.Entry(dialog, width=20)
		self.path.grid(row=0, column=1, sticky=tk.W + tk.E)
		ttk.Button(dialog, text="Choose", command=self.on_choose).grid(row=0, column=2)

		ttk.Label(dialog, text="Args:").grid(row=1, column=0)
		self.args = tk.Text(dialog, height=10, width=20)
		self.args.grid(row=1, column=1, rowspan=3)

		path, args = config.get_configuration().get_editor_details()
		self.path.insert(tk.END, path)
		for arg in args:
			self.args.insert(tk.END, arg + '\n')

		ttk.Button(dialog, text="Ok", underline=0, command=self.on_ok).grid(row=2, column=2)
		ttk.Button(dialog, text="Cancel", underline=0, command=self.on_cancel).grid(row=3, column=2)

		dialog.rowconfigure(1, weight=3)
		# Modal window.
		# Wait for visibility or grab_set doesn't seem to work.
		dialog.wait_visibility()
		dialog.grab_set()
		dialog.transient(parent)

		self.dialog = dialog


	def on_choose(self):
		filedialog.askopenfilename()


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


