" My menus

" Note that ":an" (short for ":anoremenu") is often used to make a menu work
" in all modes and avoid side effects from mappings defined by the user.

" Make sure the '<' and 'C' flags are not included in 'cpoptions', otherwise
" <CR> would not be recognized.  See ":help 'cpoptions'".
let s:cpo_save = &cpo
set cpo&vim

" Avoid installing the menus twice
if !exists("did_install_default_menus")
let did_install_default_menus = 1

" File menu
an 10.310 &File.&Open\.\.\.<Tab>:e		:browse confirm e<CR>
an 10.320 &File.Sp&lit-Open\.\.\.<Tab>:sp	:browse sp<CR>
an 10.320 &File.Open\ Tab\.\.\.<Tab>:tabnew	:browse tabnew<CR>
an 10.325 &File.&New<Tab>:enew			:confirm enew<CR>
an <silent> 10.330 &File.&Close<Tab>:close
	\ :if winheight(2) < 0 && tabpagewinnr(2) == 0 <Bar>
	\   confirm enew <Bar>
	\ else <Bar>
	\   confirm close <Bar>
	\ endif<CR>
an 10.335 &File.-SEP1-				<Nop>
an <silent> 10.340 &File.&Save<Tab>:w		:if expand("%") == ""<Bar>browse confirm w<Bar>else<Bar>confirm w<Bar>endif<CR>
an 10.350 &File.Save\ &As\.\.\.<Tab>:sav	:browse confirm saveas<CR>

if has("diff")
  an 10.400 &File.-SEP2-			<Nop>
  an 10.410 &File.Split\ &Diff\ With\.\.\.	:browse vert diffsplit<CR>
  an 10.420 &File.Split\ Patched\ &By\.\.\.	:browse vert diffpatch<CR>
endif

an 10.600 &File.-SEP4-				<Nop>
an 10.610 &File.Sa&ve-Exit<Tab>:wqa		:confirm wqa<CR>
an 10.620 &File.E&xit<Tab>:qa			:confirm qa<CR>

func! <SID>SelectAll()
  exe "norm! gg" . (&slm == "" ? "VG" : "gH\<C-O>G")
endfunc

func! s:FnameEscape(fname)
  if exists('*fnameescape')
    return fnameescape(a:fname)
  endif
  return escape(a:fname, " \t\n*?[{`$\\%#'\"|!<")
endfunc

" Edit menu
an 20.310 &Edit.&Undo<Tab>u			u
an 20.320 &Edit.&Redo<Tab>^R			<C-R>
an 20.330 &Edit.Rep&eat<Tab>\.			.

an 20.335 &Edit.-SEP1-				<Nop>
vnoremenu 20.340 &Edit.Cu&t<Tab>"+x		"+x
vnoremenu 20.350 &Edit.&Copy<Tab>"+y		"+y
cnoremenu 20.350 &Edit.&Copy<Tab>"+y		<C-Y>
nnoremenu 20.360 &Edit.&Paste<Tab>"+gP		"+gP
cnoremenu	 &Edit.&Paste<Tab>"+gP		<C-R>+
exe 'vnoremenu <script> &Edit.&Paste<Tab>"+gP	' . paste#paste_cmd['v']
exe 'inoremenu <script> &Edit.&Paste<Tab>"+gP	' . paste#paste_cmd['i']
nnoremenu 20.370 &Edit.Put\ &Before<Tab>[p	[p
inoremenu	 &Edit.Put\ &Before<Tab>[p	<C-O>[p
nnoremenu 20.380 &Edit.Put\ &After<Tab>]p	]p
inoremenu	 &Edit.Put\ &After<Tab>]p	<C-O>]p
noremenu  <script> <silent> 20.400 &Edit.&Select\ All<Tab>ggVG	:<C-U>call <SID>SelectAll()<CR>
inoremenu <script> <silent> 20.400 &Edit.&Select\ All<Tab>ggVG	<C-O>:call <SID>SelectAll()<CR>
cnoremenu <script> <silent> 20.400 &Edit.&Select\ All<Tab>ggVG	<C-U>call <SID>SelectAll()<CR>

an 20.405	 &Edit.-SEP2-				<Nop>
an 20.410	 &Edit.&Find<Tab>/			/
an 20.420	 &Edit.Find\ and\ Rep&lace<Tab>:%s	:%s/
vunmenu	 	 &Edit.Find\ and\ Rep&lace<Tab>:%s
vnoremenu	 &Edit.Find\ and\ Rep&lace<Tab>:s	:s/

an 20.425	 &Edit.-SEP3-		<Nop>
an 20.435	 &Edit.vimrc		:call <SID>EditVimrc()<CR>
an 20.436    &Edit.gvimrc       :call <SID>EditGvimrc()<CR>

fun! s:EditVimrc()
  let fname = $VIMFILES . "/vimrc"
  let fname = s:FnameEscape(fname)
  if &mod
    exe "split " . fname
  else
    exe "edit " . fname
  endif
endfun

fun! s:EditGvimrc()
  let fname = $VIMFILES . "/gvimrc"
  let fname = s:FnameEscape(fname)
  if &mod
    exe "split " . fname
  else
    exe "edit " . fname
  endif
endfun


fun! s:FixFText()
  " Fix text in nameless register to be used with :promptfind.
  return substitute(@", "[\r\n]", '\\n', 'g')
endfun

" Edit/Global Settings
an 20.440.100 &Edit.&Global\ Settings.Toggle\ Pattern\ &Highlight<Tab>:set\ hls!	:set hls! hls?<CR>
an 20.440.110 &Edit.&Global\ Settings.Toggle\ &Ignoring\ Case<Tab>:set\ ic!	:set ic! ic?<CR>
an 20.440.110 &Edit.&Global\ Settings.Toggle\ &Showing\ Matched\ Pairs<Tab>:set\ sm!	:set sm! sm?<CR>

"
" GUI options
an <silent> 20.440.310 &View.Tuggle\ &Toolbar		:call <SID>ToggleGuiOption("T")<CR>
an <silent> 20.440.320 &View.Toggle\ &Bottom\ Scrollbar :call <SID>ToggleGuiOption("b")<CR>
an <silent> 20.440.330 &View.Toggle\ &Left\ Scrollbar	:call <SID>ToggleGuiOption("l")<CR>
an <silent> 20.440.340 &View.Toggle\ &Right\ Scrollbar :call <SID>ToggleGuiOption("r")<CR>

fun! s:ToggleGuiOption(option)
    " If a:option is already set in guioptions, then we want to remove it
    if match(&guioptions, "\\C" . a:option) > -1
	exec "set go-=" . a:option
    else
	exec "set go+=" . a:option
    endif
endfun

" Edit/File Settings
an <silent> 20.440.640 &Edit.F&ile\ Settings.&File\ Format\.\.\.  :call <SID>FileFormat()<CR>

fun! s:FileFormat()
  if !exists("g:menutrans_fileformat_dialog")
    let g:menutrans_fileformat_dialog = "Select format for writing the file"
  endif
  if !exists("g:menutrans_fileformat_choices")
    let g:menutrans_fileformat_choices = "&Unix\n&Dos\n&Mac\n&Cancel"
  endif
  if &ff == "dos"
    let def = 2
  elseif &ff == "mac"
    let def = 3
  else
    let def = 1
  endif
  let n = confirm(g:menutrans_fileformat_dialog, g:menutrans_fileformat_choices, def, "Question")
  if n == 1
    set ff=unix
  elseif n == 2
    set ff=dos
  elseif n == 3
    set ff=mac
  endif
endfun

if has("win32") || has("gui_motif") || has("gui_gtk") || has("gui_kde") || has("gui_photon") || has("gui_mac")
  an 20.470 &Edit.Select\ Fo&nt\.\.\.	:set guifont=*<CR>
endif

" Programming menu
if !exists("g:ctags_command")
  if has("vms")
    let g:ctags_command = "mc vim:ctags *.*"
  else
    let g:ctags_command = "ctags -R ."
  endif
endif

an 40.300 &Tools.&Jump\ to\ This\ Tag<Tab>g^]	g<C-]>
vunmenu &Tools.&Jump\ to\ This\ Tag<Tab>g^]
vnoremenu &Tools.&Jump\ to\ This\ Tag<Tab>g^]	g<C-]>
an 40.310 &Tools.Jump\ &Back<Tab>^T		<C-T>
an 40.320 &Tools.Build\ &Tags\ File		:exe "!" . g:ctags_command<CR>

if has("diff")
  an 40.350.100 &Tools.&Diff.&Update		:diffupdate<CR>
  an 40.350.110 &Tools.&Diff.&Get\ Block	:diffget<CR>
  vunmenu &Tools.&Diff.&Get\ Block
  vnoremenu &Tools.&Diff.&Get\ Block		:diffget<CR>
  an 40.350.120 &Tools.&Diff.&Put\ Block	:diffput<CR>
  vunmenu &Tools.&Diff.&Put\ Block
  vnoremenu &Tools.&Diff.&Put\ Block		:diffput<CR>
endif

an 40.358 &Tools.-SEP2-					<Nop>
an 40.360 &Tools.&Make<Tab>:make			:make<CR>
an 40.370 &Tools.&List\ Errors<Tab>:cl			:cl<CR>
an 40.380 &Tools.L&ist\ Messages<Tab>:cl!		:cl!<CR>
an 40.390 &Tools.&Next\ Error<Tab>:cn			:cn<CR>
an 40.400 &Tools.&Previous\ Error<Tab>:cp		:cp<CR>
an 40.410 &Tools.&Older\ List<Tab>:cold			:colder<CR>
an 40.420 &Tools.N&ewer\ List<Tab>:cnew			:cnewer<CR>
an 40.430.50 &Tools.Error\ &Window.&Update<Tab>:cwin	:cwin<CR>
an 40.430.60 &Tools.Error\ &Window.&Open<Tab>:copen	:copen<CR>
an 40.430.70 &Tools.Error\ &Window.&Close<Tab>:cclose	:cclose<CR>

an 40.520 &Tools.-SEP3-					<Nop>
an <silent> 40.530 &Tools.&Convert\ to\ HEX<Tab>:%!xxd
	\ :call <SID>XxdConv()<CR>
an <silent> 40.540 &Tools.Conve&rt\ Back<Tab>:%!xxd\ -r
	\ :call <SID>XxdBack()<CR>

" Use a function to do the conversion, so that it also works with 'insertmode'
" set.
func! s:XxdConv()
  let mod = &mod
  if has("vms")
    %!mc vim:xxd
  else
    call s:XxdFind()
    exe '%!"' . g:xxdprogram . '"'
  endif
  if getline(1) =~ "^0000000:"		" only if it worked
    set ft=xxd
  endif
  let &mod = mod
endfun

func! s:XxdBack()
  let mod = &mod
  if has("vms")
    %!mc vim:xxd -r
  else
    call s:XxdFind()
    exe '%!"' . g:xxdprogram . '" -r'
  endif
  set ft=
  doautocmd filetypedetect BufReadPost
  let &mod = mod
endfun

func! s:XxdFind()
  if !exists("g:xxdprogram")
    " On the PC xxd may not be in the path but in the install directory
    if (has("win32") || has("dos32")) && !executable("xxd")
      let g:xxdprogram = $VIMRUNTIME . (&shellslash ? '/' : '\') . "xxd.exe"
    else
      let g:xxdprogram = "xxd"
    endif
  endif
endfun

if !exists("no_buffers_menu")

" Buffer list menu -- Setup functions & actions

" wait with building the menu until after loading 'session' files. Makes
" startup faster.
let s:bmenu_wait = 1

if !exists("bmenu_priority")
  let bmenu_priority = 60
endif

func! s:BMAdd()
  if s:bmenu_wait == 0
    " when adding too many buffers, redraw in short format
    if s:bmenu_count == &menuitems && s:bmenu_short == 0
      call s:BMShow()
    else
      call <SID>BMFilename(expand("<afile>"), expand("<abuf>"))
      let s:bmenu_count = s:bmenu_count + 1
    endif
  endif
endfunc

func! s:BMRemove()
  if s:bmenu_wait == 0
    let name = expand("<afile>")
    if isdirectory(name)
      return
    endif
    let munge = <SID>BMMunge(name, expand("<abuf>"))

    if s:bmenu_short == 0
      exe 'silent! aun &Buffers.' . munge
    else
      exe 'silent! aun &Buffers.' . <SID>BMHash2(munge) . munge
    endif
    let s:bmenu_count = s:bmenu_count - 1
  endif
endfunc

" Create the buffer menu (delete an existing one first).
func! s:BMShow(...)
  let s:bmenu_wait = 1
  let s:bmenu_short = 1
  let s:bmenu_count = 0
  "
  " get new priority, if exists
  if a:0 == 1
    let g:bmenu_priority = a:1
  endif

  " remove old menu, if exists; keep one entry to avoid a torn off menu to
  " disappear.
  silent! unmenu &Buffers
  exe 'noremenu ' . g:bmenu_priority . ".1 &Buffers.Dummy l"
  silent! unmenu! &Buffers

  " create new menu; set 'cpo' to include the <CR>
  let cpo_save = &cpo
  set cpo&vim
  exe 'an <silent> ' . g:bmenu_priority . ".2 &Buffers.&Refresh\\ menu :call <SID>BMShow()<CR>"
  exe 'an ' . g:bmenu_priority . ".4 &Buffers.&Delete :confirm bd<CR>"
  exe 'an ' . g:bmenu_priority . ".6 &Buffers.&Alternate :confirm b #<CR>"
  exe 'an ' . g:bmenu_priority . ".7 &Buffers.&Next :confirm bnext<CR>"
  exe 'an ' . g:bmenu_priority . ".8 &Buffers.&Previous :confirm bprev<CR>"
  exe 'an ' . g:bmenu_priority . ".9 &Buffers.-SEP- :"
  let &cpo = cpo_save
  unmenu &Buffers.Dummy

  " figure out how many buffers there are
  let buf = 1
  while buf <= bufnr('$')
    if bufexists(buf) && !isdirectory(bufname(buf)) && buflisted(buf)
      let s:bmenu_count = s:bmenu_count + 1
    endif
    let buf = buf + 1
  endwhile
  if s:bmenu_count <= &menuitems
    let s:bmenu_short = 0
  endif

  " iterate through buffer list, adding each buffer to the menu:
  let buf = 1
  while buf <= bufnr('$')
    if bufexists(buf) && !isdirectory(bufname(buf)) && buflisted(buf)
      call <SID>BMFilename(bufname(buf), buf)
    endif
    let buf = buf + 1
  endwhile
  let s:bmenu_wait = 0
  aug buffer_list
  au!
  au BufCreate,BufFilePost * call <SID>BMAdd()
  au BufDelete,BufFilePre * call <SID>BMRemove()
  aug END
endfunc

func! s:BMHash(name)
  " Make name all upper case, so that chars are between 32 and 96
  let nm = substitute(a:name, ".*", '\U\0', "")
  if has("ebcdic")
    " HACK: Replace all non alphabetics with 'Z'
    "       Just to make it work for now.
    let nm = substitute(nm, "[^A-Z]", 'Z', "g")
    let sp = char2nr('A') - 1
  else
    let sp = char2nr(' ')
  endif
  " convert first six chars into a number for sorting:
  return (char2nr(nm[0]) - sp) * 0x800000 + (char2nr(nm[1]) - sp) * 0x20000 + (char2nr(nm[2]) - sp) * 0x1000 + (char2nr(nm[3]) - sp) * 0x80 + (char2nr(nm[4]) - sp) * 0x20 + (char2nr(nm[5]) - sp)
endfunc

func! s:BMHash2(name)
  let nm = substitute(a:name, ".", '\L\0', "")
  " Not exactly right for EBCDIC...
  if nm[0] < 'a' || nm[0] > 'z'
    return '&others.'
  elseif nm[0] <= 'd'
    return '&abcd.'
  elseif nm[0] <= 'h'
    return '&efgh.'
  elseif nm[0] <= 'l'
    return '&ijkl.'
  elseif nm[0] <= 'p'
    return '&mnop.'
  elseif nm[0] <= 't'
    return '&qrst.'
  else
    return '&u-z.'
  endif
endfunc

" insert a buffer name into the buffer menu:
func! s:BMFilename(name, num)
  if isdirectory(a:name)
    return
  endif
  let munge = <SID>BMMunge(a:name, a:num)
  let hash = <SID>BMHash(munge)
  if s:bmenu_short == 0
    let name = 'an ' . g:bmenu_priority . '.' . hash . ' &Buffers.' . munge
  else
    let name = 'an ' . g:bmenu_priority . '.' . hash . '.' . hash . ' &Buffers.' . <SID>BMHash2(munge) . munge
  endif
  " set 'cpo' to include the <CR>
  let cpo_save = &cpo
  set cpo&vim
  exe name . ' :confirm b' . a:num . '<CR>'
  let &cpo = cpo_save
endfunc

" Truncate a long path to fit it in a menu item.
if !exists("g:bmenu_max_pathlen")
  let g:bmenu_max_pathlen = 35
endif
func! s:BMTruncName(fname)
  let name = a:fname
  if g:bmenu_max_pathlen < 5
    let name = ""
  else
    let len = strlen(name)
    if len > g:bmenu_max_pathlen
      let amountl = (g:bmenu_max_pathlen / 2) - 2
      let amountr = g:bmenu_max_pathlen - amountl - 3
      let pattern = '^\(.\{,' . amountl . '}\).\{-}\(.\{,' . amountr . '}\)$'
      let left = substitute(name, pattern, '\1', '')
      let right = substitute(name, pattern, '\2', '')
      if strlen(left) + strlen(right) < len
	let name = left . '...' . right
      endif
    endif
  endif
  return name
endfunc

func! s:BMMunge(fname, bnum)
  let name = a:fname
  if name == ''
    if !exists("g:menutrans_no_file")
      let g:menutrans_no_file = "[No file]"
    endif
    let name = g:menutrans_no_file
  else
    let name = fnamemodify(name, ':p:~')
  endif
  " detach file name and separate it out:
  let name2 = fnamemodify(name, ':t')
  if a:bnum >= 0
    let name2 = name2 . ' (' . a:bnum . ')'
  endif
  let name = name2 . "\t" . <SID>BMTruncName(fnamemodify(name,':h'))
  let name = escape(name, "\\. \t|")
  let name = substitute(name, "&", "&&", "g")
  let name = substitute(name, "\n", "^@", "g")
  return name
endfunc

" When just starting Vim, load the buffer menu later
if has("vim_starting")
  augroup LoadBufferMenu
    au! VimEnter * if !exists("no_buffers_menu") | call <SID>BMShow() | endif
    au  VimEnter * au! LoadBufferMenu
  augroup END
else
  call <SID>BMShow()
endif

endif " !exists("no_buffers_menu")

" Window menu
an 70.300 &Window.&New<Tab>^Wn			<C-W>n
an 70.310 &Window.S&plit<Tab>^Ws		<C-W>s
an 70.320 &Window.Sp&lit\ To\ #<Tab>^W^^	<C-W><C-^>
an 70.330 &Window.Split\ &Vertically<Tab>^Wv	<C-W>v
an 70.335 &Window.-SEP1-				<Nop>
an 70.340 &Window.&Close<Tab>^Wc			:confirm close<CR>
an 70.345 &Window.Close\ &Other(s)<Tab>^Wo		:confirm only<CR>
an 70.350 &Window.-SEP2-				<Nop>
an 70.355 &Window.Move\ &To.&Top<Tab>^WK		<C-W>K
an 70.355 &Window.Move\ &To.&Bottom<Tab>^WJ		<C-W>J
an 70.355 &Window.Move\ &To.&Left\ Side<Tab>^WH		<C-W>H
an 70.355 &Window.Move\ &To.&Right\ Side<Tab>^WL	<C-W>L
an 70.360 &Window.Rotate\ &Up<Tab>^WR			<C-W>R
an 70.362 &Window.Rotate\ &Down<Tab>^Wr			<C-W>r
an 70.365 &Window.-SEP3-				<Nop>
an 70.370 &Window.&Equal\ Size<Tab>^W=			<C-W>=
an 70.380 &Window.&Max\ Height<Tab>^W_			<C-W>_
an 70.390 &Window.M&in\ Height<Tab>^W1_			<C-W>1_
an 70.400 &Window.Max\ &Width<Tab>^W\|			<C-W>\|
an 70.410 &Window.Min\ Widt&h<Tab>^W1\|			<C-W>1\|

" The popup menu
an 1.10 PopUp.&Undo			u
an 1.15 PopUp.-SEP1-			<Nop>
an 1.16 PopUp.Lookup			f
vnoremenu 1.20 PopUp.Cu&t		"+x
vnoremenu 1.30 PopUp.&Copy		"+y
cnoremenu 1.30 PopUp.&Copy		<C-Y>
nnoremenu 1.40 PopUp.&Paste		"+gP
cnoremenu 1.40 PopUp.&Paste		<C-R>+
exe 'vnoremenu <script> 1.40 PopUp.&Paste	' . paste#paste_cmd['v']
exe 'inoremenu <script> 1.40 PopUp.&Paste	' . paste#paste_cmd['i']
vnoremenu 1.50 PopUp.&Delete		x
an 1.55 PopUp.-SEP2-			<Nop>
vnoremenu 1.60 PopUp.Select\ Blockwise	<C-V>

nnoremenu 1.70 PopUp.Select\ &Word	vaw
onoremenu 1.70 PopUp.Select\ &Word	aw
vnoremenu 1.70 PopUp.Select\ &Word	<C-C>vaw
inoremenu 1.70 PopUp.Select\ &Word	<C-O>vaw
cnoremenu 1.70 PopUp.Select\ &Word	<C-C>vaw

nnoremenu 1.73 PopUp.Select\ &Sentence	vas
onoremenu 1.73 PopUp.Select\ &Sentence	as
vnoremenu 1.73 PopUp.Select\ &Sentence	<C-C>vas
inoremenu 1.73 PopUp.Select\ &Sentence	<C-O>vas
cnoremenu 1.73 PopUp.Select\ &Sentence	<C-C>vas

nnoremenu 1.77 PopUp.Select\ Pa&ragraph	vap
onoremenu 1.77 PopUp.Select\ Pa&ragraph	ap
vnoremenu 1.77 PopUp.Select\ Pa&ragraph	<C-C>vap
inoremenu 1.77 PopUp.Select\ Pa&ragraph	<C-O>vap
cnoremenu 1.77 PopUp.Select\ Pa&ragraph	<C-C>vap

nnoremenu 1.80 PopUp.Select\ &Line	V
onoremenu 1.80 PopUp.Select\ &Line	<C-C>V
vnoremenu 1.80 PopUp.Select\ &Line	<C-C>V
inoremenu 1.80 PopUp.Select\ &Line	<C-O>V
cnoremenu 1.80 PopUp.Select\ &Line	<C-C>V

nnoremenu 1.90 PopUp.Select\ &Block	<C-V>
onoremenu 1.90 PopUp.Select\ &Block	<C-C><C-V>
vnoremenu 1.90 PopUp.Select\ &Block	<C-C><C-V>
inoremenu 1.90 PopUp.Select\ &Block	<C-O><C-V>
cnoremenu 1.90 PopUp.Select\ &Block	<C-C><C-V>

noremenu  <script> <silent> 1.100 PopUp.Select\ &All	:<C-U>call <SID>SelectAll()<CR>
inoremenu <script> <silent> 1.100 PopUp.Select\ &All	<C-O>:call <SID>SelectAll()<CR>
cnoremenu <script> <silent> 1.100 PopUp.Select\ &All	<C-U>call <SID>SelectAll()<CR>


" The GUI toolbar (for MS-Windows and GTK)
if has("toolbar")
  an 1.10 ToolBar.Open			:browse confirm e<CR>
  an <silent> 1.20 ToolBar.Save		:if expand("%") == ""<Bar>browse confirm w<Bar>else<Bar>confirm w<Bar>endif<CR>
  an 1.30 ToolBar.SaveAll		:browse confirm wa<CR>

  an 1.45 ToolBar.-sep1-		<Nop>
  an 1.50 ToolBar.Undo			u
  an 1.60 ToolBar.Redo			<C-R>

  an 1.65 ToolBar.-sep2-		<Nop>
  vnoremenu 1.70 ToolBar.Cut		"+x
  vnoremenu 1.80 ToolBar.Copy		"+y
  cnoremenu 1.80 ToolBar.Copy		<C-Y>
  nnoremenu 1.90 ToolBar.Paste		"+gP
  cnoremenu	 ToolBar.Paste		<C-R>+
  exe 'vnoremenu <script>	 ToolBar.Paste	' . paste#paste_cmd['v']
  exe 'inoremenu <script>	 ToolBar.Paste	' . paste#paste_cmd['i']

  if !has("gui_athena")
    an 1.95   ToolBar.-sep3-		<Nop>
    an 1.100  ToolBar.Replace		:promptrepl<CR>
    vunmenu   ToolBar.Replace
    vnoremenu ToolBar.Replace		y:promptrepl <C-R>=<SID>FixFText()<CR><CR>
    an 1.110  ToolBar.FindNext		n
    an 1.120  ToolBar.FindPrev		N
  endif

  an 1.245 ToolBar.-sep6-		<Nop>
  an 1.250 ToolBar.Make			:make<CR>
  an 1.270 ToolBar.RunCtags		:exe "!" . g:ctags_command<CR>
  an 1.280 ToolBar.TagJump		g<C-]>


" Only set the tooltips here if not done in a language menu file
if exists("*Do_toolbar_tmenu")
  call Do_toolbar_tmenu()
else
  let did_toolbar_tmenu = 1
  tmenu ToolBar.Open		Open file
  tmenu ToolBar.Save		Save current file
  tmenu ToolBar.SaveAll		Save all files
  tmenu ToolBar.Undo		Undo
  tmenu ToolBar.Redo		Redo
  tmenu ToolBar.Cut		Cut to clipboard
  tmenu ToolBar.Copy		Copy to clipboard
  tmenu ToolBar.Paste		Paste from Clipboard
  if !has("gui_athena")
    tmenu ToolBar.Replace	Find / Replace...
    tmenu ToolBar.FindNext	Find Next
    tmenu ToolBar.FindPrev	Find Previous
  endif
  tmenu ToolBar.Make		Make current project (:make)
  tmenu ToolBar.RunCtags	Build tags in current directory tree (!ctags -R .)
  tmenu ToolBar.TagJump		Jump to tag under cursor
endif

endif

endif " !exists("did_install_default_menus")

" Install the Syntax menu only when filetype.vim has been loaded or when
" manual syntax highlighting is enabled.
" Avoid installing the Syntax menu twice.
if (exists("did_load_filetypes") || exists("syntax_on"))
	\ && !exists("did_install_syntax_menu")
  let did_install_syntax_menu = 1

an 50.710 &Syntax.Co&lor\ Test		:sp $VIMRUNTIME/syntax/colortest.vim<Bar>so %<CR>
an 50.720 &Syntax.&Highlight\ Test	:runtime syntax/hitest.vim<CR>
an 50.730 &Syntax.&Convert\ to\ HTML	:runtime syntax/2html.vim<CR>

endif " !exists("did_install_syntax_menu")

" Restore the previous value of 'cpoptions'.
let &cpo = s:cpo_save
unlet s:cpo_save

" vim: set sw=2 :
