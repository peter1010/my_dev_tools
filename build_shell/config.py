import platform
import os
from configparser import ConfigParser

G_Config = None

class Config:
	def __init__(self):
		system = platform.system()
		if system == 'Linux':
			config_dir = os.getenv('XDG_CONFIG_HOME', None)
			if config_dir is None:
				config_dir = os.path.join(os.getenv('HOME'), '.config')
			config_file = os.path.join(config_dir, 'dev_tools', 'build_shell.ini')
		elif system == 'Windows':
			config_dir = os.getenv('APPDATA', None)
			if config_dir is None:
				config_dir = os.path.join(os.getenv('HOME'), 'AppData', 'Local')
			config_file = os.path.join(config_dir, 'dev_tools', 'build_shell.ini')
		else:
			raise RuntimeError("Support for %s is TODO" % system)
		config_object = ConfigParser(interpolation=None)
		if os.path.exists(config_file):
			config_object.read(config_file)
		self.config_object = config_object
		self.config_file = config_file


	def save(self):
		if not os.path.exists(self.config_file):
			os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
		self.config_object.write(open(self.config_file, 'w'))


	def get_editor_details(self):
		try:
			editor_path = self.config_object['Editor']['path']
			flatten_args = self.config_object['Editor']['args']
			editor_args = [x.strip() for x in flatten_args.splitlines()]
		except KeyError:
			system = platform.system()
			if system == 'Linux':
				editor_path = os.getenv('EDITOR', '/usr/bin/vim')
				editor_args = ["+%l", "%f"]
			elif system == 'Windows':
				editor_path = self.find_gvim_on_windows()
				editor_args = ["+%l", "%f"]
			else:
				raise RuntimeError("Support for %s is TODO" % system)
			self.set_editor_details(editor_path, editor_args)
		return editor_path, editor_args


	def set_editor_details(self, new_path, new_args):
		flatten_args = "".join(["%s\n" % x.strip() for x in new_args])
		try:
			prev_path = self.config_object['Editor']['path']
			prev_flatten_args = self.config_object['Editor']['args']
		except KeyError:
			prev_path = None
			prev_flatten_args = None

		if prev_path != new_path or prev_args != new_args:
			self.config_object['Editor'] = {'path' : new_path, 'args' : flatten_args}
			self.save()
		return


	def find_gvim_on_windows(self):
		import winreg
		# Check registry, local user first, then globally
		install_path = None
		for hive in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
			print(hive)
			try:
				key = winreg.OpenKey(hive, "Software\\Vim\\Gvim")
				data = winreg.QueryValueEx(key, "path")
				if data[1] == 1:
					install_path = data[0]
				print(install_path)
				winreg.CloseKey(key)
				break
			except OSError:
				pass
		return install_path



def get_configuration():
	global G_Config
	if G_Config is None:
		G_Config = Config()
	return G_Config


