# Build Code
import sys
import os
import importlib

import output_window

TYPES_DIR = "build_types"

def load_plugins(plugin_dir):
	plugins = []
	for script in os.listdir(plugin_dir):
		if script.endswith(".py"):
			name = script[:-3]
			mod = importlib.import_module("{}.{}".format(TYPES_DIR, name))
			if hasattr(mod, "get_plugin"):
				plugins.append(mod.get_plugin())
	return plugins


def find_build_plugin(plugins, dirname, ext):
	"""Give a list of plugins, find which (if any) can do the build from the working directory dirname, given the file
		extension ext of the file in the current vim buffer"""
	for plugin in plugins:
		if plugin.can_build(dirname, ext):
			return plugin

	# Go up to the next level in the build tree and try again..
	dirname, removedPath = os.path.split(dirname)
	if dirname and removedPath:
		return find_build_plugin(plugins, dirname, ext)
	else:
		return None


def main():
	plugin_dir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), TYPES_DIR))
	plugins = load_plugins(plugin_dir)

	filepath = sys.argv[1]
	if len(sys.argv) > 2:
		action = sys.argv[2]
	else:
		action = None
	dirname, filename = os.path.split(filepath)
	filename, ext = os.path.splitext(filename)
	plugin = find_build_plugin(plugins, dirname, ext)
	if plugin:
		output = output_window.OutputWindow()
		output.open()
		error_list = plugin.run(action, output)
		for err in error_list:
			print(err)
	else:
		print("No Make plugin found for {}".format(filepath))


if __name__ == "__main__":
	main()
