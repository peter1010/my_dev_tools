" If already done, exit early
" g: means global namespace

if exists('g:did_my_bits')
    finish
endif

let g:did_my_bits = 1

function! Trim()
    " find whitespace at end of line and replace with nothing (/e means don't
    " erro if nothing found
    execute '%s/\s\+$//e'
endfunc

command! TABIFY call my_bits#tabify#Tabify()
command! SPACIFY call my_bits#tabify#Spacify()
command! TRIM call Trim()

function! DetectIndentation(language)
    call my_bits#tabify#DetectIndent(a:language)
endfunc


if !has('pythonx')
    finish
endif

" Expand source script file to full path
" The s: put the variable in the script's namespace
let s:path = fnamemodify(resolve(expand('<sfile>:p')), ":h:h") . '/pythonx'

" echom "path is " . s:path

function! LspGet(type)
    execute 'pythonx import sys'
    execute 'pythonx sys.argv = [r"' . s:path . '/lsp/client.py", r"' . a:type . '"]'
    execute 'pyxfile ' . s:path . '/lsp/client.py'
endfunc

"function! my_bits#lsp#Lookup(keyword)

command! LSPxDCL call my_bits#lsp#Lookup("find_declaration")
command! LSPxDEF call LspGet("find_definition")
command! LSPxIMP call LspGet("find_implementation")
command! LSPxREF call LspGet("find_references")
command! LSPxHOV call LspGet("hover")
