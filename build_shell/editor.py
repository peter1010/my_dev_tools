import subprocess
import os

def get_vim():
	return os.path.join("C:\\", "Program Files", "Vim", "vim91", "gvim.exe")

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


