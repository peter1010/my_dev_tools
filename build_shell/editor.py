import subprocess
import os
import platform

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import config

def get_vim():
	return config.get_configuration().get_editor_path()

def spawn(filename, lineNum):
		args = [get_vim(), "--remote-silent", "+" + str(lineNum), filename]
		print(args)
		proc = subprocess.Popen(args, start_new_session=True, close_fds=True)

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
		path, args = config.get_configuration().get_editor_details()
		editor_path = tk.StringVar()
		editor_args = tk.StringVar()
		editor_path.set(path)
		editor_args.set(args)

		dialog = tk.Toplevel(parent)
		dialog.title("Configure Editor")
		# Set _NET_WM_WINDOW_TYPE_DIALOG, Sway uses this to know to float the window
		dialog.attributes('-type', 'dialog')

		tk.Label(dialog, text="Path:").grid(row=0, column=0)
		tk.Entry(dialog, textvariable=editor_path).grid(row=0, column=1)
		
		tk.Button(dialog, text="Choose", command=self.on_choose).grid(row=0, column=2)

		tk.Label(dialog, text="Args:").grid(row=1, column=0)
		tk.Entry(dialog, textvariable=editor_args).grid(row=1, column=1)
		

		tk.Button(dialog, text="Ok", underline=0, command=self.on_ok).grid(row=2, column=0)

		cancel_btn = tk.Button(dialog, text="Cancel", underline=0, command=self.cancel)
		cancel_btn.grid(row=2, column=1)

        # Modal window.
        # Wait for visibility or grab_set doesn't seem to work.
		dialog.wait_visibility()   # <<< NOTE
		dialog.grab_set()          # <<< NOTE
		dialog.transient(parent)   # <<< NOTE

		self.dialog = dialog
		self.editor_path = editor_path
		self.editor_args = editor_args


	def on_choose(self):
		#filedialog.FileDialog(self.dialog).go()
		filedialog.askopenfilename()


	def on_ok(self):
		editor_path = self.editor_path.get()
		editor_args = self.editor_args.get()
		if not os.path.exists(editor_path):
			messagebox.showerror(message="Invalid Path")
			return
		config.get_configuration().set_editor_details(editor_path, editor_args)
		self.dialog.grab_release()      # <<< NOTE
		self.dialog.destroy()


	def cancel(self):
		self.dialog.grab_release()      # <<< NOTE
		self.dialog.destroy()
