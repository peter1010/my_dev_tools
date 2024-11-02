" If already done, exit early
" g: means global namespace

if exists('g:did_my_bits')
    finish
endif

let g:did_my_bits = 1


function! Tabify_line(ident, spaces)
    let spaces_in_tab = repeat(' ', &tabstop)
    let result = substitute(a:ident, spaces_in_tab, '\t', 'g')
    let result = substitute(result, ' \+\ze\t', '', 'g')
    if a:spaces == 1
        let result = substitute(result, '\t', spaces_in_tab, 'g')
    endif
    return result
endfunc


function! Tabify()
    let savepos = getpos('.')
    execute '%s/^\s\+/\=Tabify_line(submatch(0),0)/e'
    call setpos('.', savepos)
endfunc


function! Spacify()
    let savepos = getpos('.')
    execute '%s/^\s\+/\=Tabify_line(submatch(0),1)/e'
    call setpos('.', savepos)
endfunc


function! Trim()
    " find whitespace at end of line and replace with nothing (/e means don't
    " erro if nothing found
    execute '%s/\s\+$//e'
endfunc

command! TABIFY call Tabify()
command! SPACIFY call Spacify()
command! TRIM call Trim()


if !has('pythonx')
    finish
endif

" Expand source script file to full path
" The s: put the variable in the script's namespace
let s:path = fnamemodify(resolve(expand('<sfile>:p')), ":h:h") . '/pythonx'

" echom "path is " . s:path

"& in from of a option means treat the option as a variable
"This means the option is set to the evaluation of the expression
let &makeprg = 'python "' . s:path . '/build.py" %:p'

" -> "filename", line y:x E:comment
set efm=\"%f\"\\,\ line\ %l:%c\ %t:%m

execute 'pythonx import sys'

function! Gtag()
    execute 'pythonx sys.argv = [r"' . s:path . '/gtags.py", "b"]'
    execute 'pyxfile ' . s:path . '/gtags.py'
endfunc


function! SetCScope()
    execute 'pythonx sys.argv = [r"' . s:path . '/gtags.py", "c"]'
    execute 'pyxfile ' . s:path . '/gtags.py'
endfunc


command! GTAG call Gtag()

function! DetectIndentation()
    execute 'pythonx sys.argv = [r"' . s:path . '/gtags.py", "b"]'
    execute 'pyxfile ' . s:path . '/detect_indent.py'
endfunc

"call SetCScope()
" vim: shiftwidth=4 expandtab tabstop=4 :
