import subprocess
import os
import platform

import tkinter as tk

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
		dialog = tk.Toplevel(parent)
		dialog.title("Configure Editor")
		# Set _NET_WM_WINDOW_TYPE_DIALOG, Sway uses this to know to float the window
		dialog.attributes('-type', 'dialog')
		self.entry = tk.Entry(dialog)
		self.entry.pack()
		ok_btn = tk.Button(dialog, text="Ok", underline=0, command=self.ok)
		ok_btn.pack(side=tk.LEFT)

		cancel_btn = tk.Button(dialog, text="Cancel", underline=0, command=self.cancel)
		cancel_btn.pack(side=tk.LEFT)

        # Modal window.
        # Wait for visibility or grab_set doesn't seem to work.
		dialog.wait_visibility()   # <<< NOTE
		dialog.grab_set()          # <<< NOTE
		dialog.transient(parent)   # <<< NOTE

		self.dialog = dialog

		cfg = config.get_configuration()
		print(cfg.get_editor_path())


	def ok(self):
#        self.data = self.entry.get()
		self.dialog.grab_release()      # <<< NOTE
		self.dialog.destroy()

	def cancel(self):
		self.dialog.grab_release()      # <<< NOTE
		self.dialog.destroy()
