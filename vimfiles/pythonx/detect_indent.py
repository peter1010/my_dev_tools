import vim

# find the first line that has indent and discovery what it is

def checked(buf, line):
	trimmed = len(line.lstrip())
	if trimmed <= 0:
		return False
	indent = line[:len(line) - trimmed]
	space_idx = indent.find(" ")
	tab_idx = indent.find("\t")
	if space_idx >= 0:
		if tab_idx >= 0:
			return False
		buf.options["expandtab"] = True
		buf.options["tabstop"] = len(indent)
		buf.options["shiftwidth"] = len(indent)
		return True
	buf.options["expandtab"] = False
	buf.options["tabstop"] = 4
	buf.options["shiftwidth"] = 4
	return True

g_in_comment_block = False

def skip_cpp_comment_block(line):
	global g_in_comment_block

	if line.startswith("/*"):
		g_in_comment_block = True
	if line.endswith("*/"):
		g_in_comment_block = False;
		return True
	return g_in_comment_block


def dummy(line):
	return False


def main():
	language = sys.argv[1]
	if language == "cpp":
		skip_comment_block = skip_cpp_comment_block
	else:
		skip_comment_block = dummy
	buf = vim.current.buffer
	for line in buf:
		if skip_comment_block(line):
			continue
		if line.startswith("\t") or line.startswith(" "):
			if checked(buf, line):
				return
	# Empty file
	buf.options["expandtab"] = False
	buf.options["tabstop"] = 4
	buf.options["shiftwidth"] = 4

if __name__ == "__main__":
	main()
