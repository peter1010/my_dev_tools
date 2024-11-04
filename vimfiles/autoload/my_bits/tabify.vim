
function! Tabify_line(ident, spaces)
    let spaces_in_tab = repeat(' ', &tabstop)
    let result = substitute(a:ident, spaces_in_tab, '\t', 'g')
    let result = substitute(result, ' \+\ze\t', '', 'g')
    if a:spaces == 1
        let result = substitute(result, '\t', spaces_in_tab, 'g')
    endif
    return result
endfunc


function! my_bits#tabify#Tabify()
    let savepos = getpos('.')
    execute '%s/^\s\+/\=Tabify_line(submatch(0),0)/e'
    call setpos('.', savepos)
endfunc


function! my_bits#tabify#Spacify()
    let savepos = getpos('.')
    execute '%s/^\s\+/\=Tabify_line(submatch(0),1)/e'
    call setpos('.', savepos)
endfunc

