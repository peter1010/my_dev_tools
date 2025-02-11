function! Checked(line)
    let length = len(a:line)
    if length <= 0
        return 0
    endif
    let trimmed = len(trim(a:line, " \t", 1))
    if trimmed <= 0 || trimmed >= length
        return 0
    endif
    let indent = a:line[0:length - trimmed - 1]
    let spaces = len(trim(indent, "\t"))
    let tabs = len(trim(indent, " "))
    if spaces > 0
        if tabs > 0
            return 0
        endif
        set expandtab
        let &tabstop = spaces
        let &shiftwidth = spaces
        return 1
    endif
    set noexpandtab
    set tabstop=4
    set shiftwidth=4
    return 1
endfunc


function! SkipCppCommentBlock(line)
    if a:line[0:1] == "/*"
        let s:in_comment_block = 1
    endif
    let length = len(a:line)
    if a:line[length-2:length-1] == "/*"
        let s:in_comment_block = 0
        return 1
    endif
    return s:in_comment_block
endfunc


function! Dummy(line)
    return 0
endfunc


function! my_bits#tabify#DetectIndent(language)
    if a:language == "cpp"
        let SkipCommentBlock = function("SkipCppCommentBlock")
    else
        let SkipCommentBlock = function("Dummy")
    endif
    let s:in_comment_block = 0
    let line_num = 1
    let last_line = line('$')
    while line_num <= last_line
        let line = getline(line_num)
        if !SkipCommentBlock(line)
            if Checked(line)
                return
            endif
        endif
        let line_num += 1
    endwhile
" Empty file
    set noexpandtab
    set tabstop=4
    set shiftwidth=4
endfunc


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

