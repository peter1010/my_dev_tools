
function! Request(language, keyword, filename, row, col)
"		if hasattr(socket, "AF_UNIX"):
"			sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
"			self.servername = b"/tmp/lsp"
"			# AF_UNIX Datagram doesn't automatically create the client sockname
"			self.sockname = b"/tmp/lsp_client"
"			sock.bind(self.sockname)
"		else:
	let chan = ch_open("127.0.0.1:8702", { "mode" : "json", "timeout" : 10000})

	let data = {
		\ "lng" : a:language,
		\ "mtd" : a:keyword,
		\ "arg" : {
		\ 	"pth" : a:filename,
		\ 	"row" : a:row,
		\ 	"col" : a:col
		\ }}
	let response = ch_evalexpr(chan, data)
	
	echo "|" response "|"
	if response[0] == "Ok"
		edit response[1]["name"]
		call cursor(response[1]["row"], response[1]["col"])
	endif
endfunc


function! my_bits#lsp#Lookup(keyword)
" 1,1 is top left
	let row = line(".")
	let col = col(".")
	let language = &filetype
	let filename = expand("%:p")
	echo language a:keyword filename row col
	call Request(language, a:keyword, filename, row, col)
endfunc

