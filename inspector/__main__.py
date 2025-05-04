try:
	import build_shell.main as shell
except ImportError:
	import main as shell

if __name__ == "__main__":
	try:
		shell.main()
	except KeyboardInterrupt:
		print("\nScript terminated via Ctrl-C")
	except Exception as err:
		print(str(err))
		input("Press 'Enter' to close script")
