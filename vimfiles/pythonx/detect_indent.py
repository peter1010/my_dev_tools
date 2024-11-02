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


def main():
	buf = vim.current.buffer
	for line in buf:
		if line.startswith("\t") or line.startswith(" "):
			if checked(buf, line):
				return

if __name__ == "__main__":
	main()
