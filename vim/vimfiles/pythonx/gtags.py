import vim
import os
import sys
import imp

TYPES_DIR = "tag_types"

def find_tag_plugin(plugin_dir, dirname, ext):
	"""Give a list of plugins, find which (if any) can do the tag function from the working directory dirname, given the file
		extension ext of the file in the current vim buffer"""
	for script in os.listdir(plugin_dir):
		if script.endswith(".py"):
			name = script[:-3]
			details = imp.find_module(name, [plugin_dir])
			mod = imp.load_module(name, *details)
			if hasattr(mod, "get_plugin"):
				plugin = mod.get_plugin()
				maybe, definite = plugin.has_tags(dirname, ext)
				if definite:
					return plugin
				elif not maybe:
					return None

	# Go up to the next level in the build tree and try again..
	dirname, removedPath = os.path.split(dirname)
	if dirname and removedPath:
		return find_tag_plugin(plugin_dir, dirname, ext)
	else:
		return None

def setup_cscope():
	options = vim.options
	options["cscopeprg"] = "C:\\msys64\\usr\\bin\\gtags-cscope.exe"
	pass

def main():
	if sys.argv[1] == 'b':

		print("|", sys.argv[0], "|")
		try:
			plugin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), TYPES_DIR))
		except NameError:
			plugin_dir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), TYPES_DIR))
		filepath = vim.current.buffer.name
		dirname, filename = os.path.split(filepath)
		filename, ext = os.path.splitext(filename)
		plugin = find_tag_plugin(plugin_dir, dirname, ext)
		if plugin:
			plugin.run()
	elif sys.argv[1] == 'c':
		setup_cscope()

main()
