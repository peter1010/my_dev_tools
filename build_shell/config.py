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
		else:
			raise RuntimeError("Support for %s is TODO" % system)
		config_object = ConfigParser()
		if os.path.exists(config_file):
			config_object.read(config_file)
		self.config_object = config_object
		self.config_file = config_file

	def save(self):
		if not os.path.exists(self.config_file):
			os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
		self.config_object.write(open(self.config_file, 'w'))

	def get_editor_path(self):
		try:
			editor_path = self.config_object['Editor']['path']
		except KeyError:
			if platform.system() == 'Linux':
				editor_path = os.getenv('EDITOR', '/usr/bin/vim')
		else:
			raise RuntimeError("Support for %s is TODO" % system)
		self.config_object['Editor'] = { 'path' : editor_path, 'args' : '' }
		self.save()
		return editor_path


def get_configuration():
	global G_Config
	if G_Config is None:
		G_Config = Config()
	return G_Config


